import { randomUUID } from 'node:crypto';
import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as os from 'node:os';
import { spawn } from 'node:child_process';

const DEFAULT_TASKS_DIR = path.join(process.env.LOCALAPPDATA || os.homedir(), 'GrokMachineMcp', 'tasks');
const MAX_LOG_BYTES = 500000;

function tasksDir() {
  return process.env.MCP_TASKS_DIR || DEFAULT_TASKS_DIR;
}

function taskPath(id) {
  return path.join(tasksDir(), `${id}.json`);
}

function taskLogPath(id) {
  return path.join(tasksDir(), `${id}.log`);
}

function taskRuntimePath(id) {
  return path.join(tasksDir(), `${id}.runtime.json`);
}

function taskRunnerPath(id) {
  return path.join(tasksDir(), `${id}.runner.ps1`);
}

async function ensureTasksDir() {
  await fs.mkdir(tasksDir(), { recursive: true });
  return tasksDir();
}

async function loadTask(id) {
  try {
    const raw = await fs.readFile(taskPath(id), 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    if (err.code === 'ENOENT') return null;
    throw err;
  }
}

async function saveTask(task) {
  await ensureTasksDir();
  const file = taskPath(task.id);
  const tmp = `${file}.${process.pid}.${randomUUID()}.tmp`;
  await fs.writeFile(tmp, JSON.stringify(task, null, 2), 'utf8');
  await fs.rename(tmp, file);
  return task;
}

function encode(value) {
  return Buffer.from(String(value), 'utf8').toString('base64');
}

function processAlive(pid) {
  if (!Number.isInteger(Number(pid)) || Number(pid) <= 0) return false;
  try {
    process.kill(Number(pid), 0);
    return true;
  } catch {
    return false;
  }
}

async function readRuntime(task) {
  try {
    const raw = await fs.readFile(taskRuntimePath(task.id), 'utf8');
    return JSON.parse(raw.replace(/^\uFEFF/, ''));
  } catch (err) {
    if (err.code === 'ENOENT') return null;
    return { status: 'failed', error: `Invalid task runtime record: ${err.message}` };
  }
}

async function refreshTask(task) {
  if (!task || ['completed', 'failed', 'cancelled'].includes(task.status)) return task;
  const runtime = await readRuntime(task);
  if (runtime?.status) {
    task.status = runtime.status;
    task.updatedAt = runtime.completedAt || new Date().toISOString();
    task.result = runtime.result || { exitCode: runtime.exitCode ?? null };
    task.error = runtime.error || null;
    await saveTask(task);
    return task;
  }
  if (task.status === 'running' && task.pid && !processAlive(task.pid)) {
    task.status = 'failed';
    task.updatedAt = new Date().toISOString();
    task.error = 'Task process ended before writing a completion record.';
    await saveTask(task);
  }
  return task;
}

function runnerScript() {
  return `
$ErrorActionPreference = 'Stop'
$command = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:VEX_TASK_COMMAND_B64))
$logPath = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:VEX_TASK_LOG_B64))
$runtimePath = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:VEX_TASK_RUNTIME_B64))
$startedAt = (Get-Date).ToUniversalTime().ToString('o')
try {
  & ([scriptblock]::Create($command)) *>&1 | ForEach-Object {
    Add-Content -LiteralPath $logPath -Value ([string]$_) -Encoding UTF8
  }
  $exitCode = if ($null -ne $LASTEXITCODE) { [int]$LASTEXITCODE } else { 0 }
  $status = if ($exitCode -eq 0) { 'completed' } else { 'failed' }
  $record = [ordered]@{ status = $status; exitCode = $exitCode; startedAt = $startedAt; completedAt = (Get-Date).ToUniversalTime().ToString('o') }
  $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $runtimePath -Encoding UTF8
  exit $exitCode
} catch {
  Add-Content -LiteralPath $logPath -Value ($_.Exception.ToString()) -Encoding UTF8
  $record = [ordered]@{ status = 'failed'; exitCode = 1; startedAt = $startedAt; completedAt = (Get-Date).ToUniversalTime().ToString('o'); error = $_.Exception.Message }
  $record | ConvertTo-Json -Compress | Set-Content -LiteralPath $runtimePath -Encoding UTF8
  exit 1
}
`;
}

async function startTaskProcess(task) {
  if (!task.command) {
    task.status = 'pending';
    task.logs.push({ ts: new Date().toISOString(), level: 'info', message: 'Task created without a command; waiting for an execution agent.' });
    task.updatedAt = new Date().toISOString();
    return saveTask(task);
  }

  await ensureTasksDir();
  const logPath = taskLogPath(task.id);
  const runtimePath = taskRuntimePath(task.id);
  const runnerPath = taskRunnerPath(task.id);
  await fs.writeFile(logPath, '', 'utf8');
  await fs.rm(runtimePath, { force: true }).catch(() => {});
  await fs.writeFile(runnerPath, runnerScript(), 'utf8');
  const cwd = task.cwd ? path.resolve(task.cwd) : process.cwd();
  const child = spawn('powershell.exe', [
    '-NoLogo', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
    '-File', runnerPath,
  ], {
    cwd,
    windowsHide: true,
    detached: false,
    stdio: 'ignore',
    env: {
      ...process.env,
      VEX_TASK_COMMAND_B64: encode(task.command),
      VEX_TASK_LOG_B64: encode(logPath),
      VEX_TASK_RUNTIME_B64: encode(runtimePath),
    },
  });

  task.status = 'running';
  task.pid = child.pid || null;
  task.logPath = logPath;
  task.runtimePath = runtimePath;
  task.updatedAt = new Date().toISOString();
  await saveTask(task);
  child.once('error', async (error) => {
    const current = await loadTask(task.id).catch(() => null);
    if (!current || ['completed', 'failed', 'cancelled'].includes(current.status)) return;
    current.status = 'failed';
    current.updatedAt = new Date().toISOString();
    current.error = `Task process failed to start: ${error.message}`;
    await saveTask(current).catch(() => {});
  });
  child.unref();
  return task;
}

export async function taskStart({ title, objective, command, cwd, metadata = {} }) {
  const id = randomUUID();
  const now = new Date().toISOString();
  const task = {
    id,
    title: title || objective?.slice(0, 80) || 'untitled',
    objective: objective || '',
    status: 'pending',
    createdAt: now,
    updatedAt: now,
    command: command || null,
    cwd: cwd || null,
    pid: null,
    logPath: null,
    runtimePath: null,
    logs: [],
    artifacts: [],
    result: null,
    error: null,
    metadata,
  };
  await saveTask(task);
  return startTaskProcess(task);
}

export async function taskStatus(id) {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  await refreshTask(task);
  return {
    id: task.id,
    title: task.title,
    status: task.status,
    pid: task.pid || null,
    createdAt: task.createdAt,
    updatedAt: task.updatedAt,
    objective: task.objective,
    result: task.result,
    error: task.error,
    hasLogs: (task.logs?.length || 0) > 0 || Boolean(task.logPath),
    artifactCount: task.artifacts?.length || 0,
  };
}

export async function taskLogs(id, { limit = 100, offset = 0 } = {}) {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  await refreshTask(task);
  let output = '';
  if (task.logPath) {
    try {
      const stat = await fs.stat(task.logPath);
      const start = Math.max(0, stat.size - MAX_LOG_BYTES);
      const handle = await fs.open(task.logPath, 'r');
      const buffer = Buffer.alloc(Math.min(MAX_LOG_BYTES, stat.size));
      await handle.read(buffer, 0, buffer.length, start);
      await handle.close();
      output = buffer.toString('utf8').replace(/^\uFEFF/, '');
    } catch {}
  }
  const logs = task.logs || [];
  return { id, total: logs.length, offset, limit, logs: logs.slice(offset, offset + limit), output };
}

export async function taskArtifacts(id) {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  return { id, artifacts: task.artifacts || [] };
}

export async function taskCancel(id, reason = 'cancelled by user') {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  await refreshTask(task);
  if (['completed', 'failed', 'cancelled'].includes(task.status)) return task;
  if (task.pid && processAlive(task.pid)) {
    try { process.kill(task.pid); } catch {}
  }
  task.status = 'cancelled';
  task.updatedAt = new Date().toISOString();
  task.error = reason;
  task.logs = task.logs || [];
  task.logs.push({ ts: task.updatedAt, level: 'info', message: `Cancelled: ${reason}` });
  await saveTask(task);
  return task;
}

export async function taskContinue(id, note = '') {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  await refreshTask(task);
  if (['completed', 'failed', 'cancelled'].includes(task.status)) return task;
  if (note) {
    task.logs = task.logs || [];
    task.logs.push({ ts: new Date().toISOString(), level: 'info', message: `Continue: ${note}` });
  }
  if (task.status === 'pending' || task.status === 'paused') return startTaskProcess(task);
  task.updatedAt = new Date().toISOString();
  return saveTask(task);
}

export async function taskAppendLog(id, level, message) {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  const entry = { ts: new Date().toISOString(), level: level || 'info', message: String(message) };
  task.logs = task.logs || [];
  task.logs.push(entry);
  task.updatedAt = entry.ts;
  await saveTask(task);
  return entry;
}

export async function taskSetStatus(id, status, result = null, error = null) {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  task.status = status;
  task.updatedAt = new Date().toISOString();
  if (result !== null) task.result = result;
  if (error !== null) task.error = error;
  await saveTask(task);
  return task;
}

export async function taskAddArtifact(id, artifact) {
  const task = await loadTask(id);
  if (!task) throw new Error(`Task not found: ${id}`);
  task.artifacts = task.artifacts || [];
  task.artifacts.push({ ...artifact, addedAt: new Date().toISOString() });
  task.updatedAt = new Date().toISOString();
  await saveTask(task);
  return task;
}

export async function listRecentTasks({ limit = 20 } = {}) {
  await ensureTasksDir();
  const files = await fs.readdir(tasksDir());
  const recent = [];
  for (const file of files.filter((name) => name.endsWith('.json') && !name.endsWith('.runtime.json'))) {
    try {
      const task = await loadTask(path.basename(file, '.json'));
      if (!task) continue;
      await refreshTask(task);
      recent.push({ id: task.id, title: task.title, status: task.status, createdAt: task.createdAt, updatedAt: task.updatedAt });
    } catch {}
  }
  recent.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));
  return recent.slice(0, Math.max(1, Math.min(100, limit)));
}

export function getTasksDir() {
  return tasksDir();
}

export { loadTask, saveTask, runnerScript };
