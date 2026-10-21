import { createRequire } from 'node:module';
import { randomUUID, timingSafeEqual } from 'node:crypto';
import { spawn } from 'node:child_process';
import { createServer as createHttpServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import * as fs from 'node:fs/promises';
import { existsSync, createReadStream, readFileSync } from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { createOAuthService } from './oauth.mjs';
import * as tasks from './lib/tasks.mjs';
import * as verify from './lib/verify.mjs';
import * as ollama from './lib/ollama.mjs';
import * as registry from './lib/registry.mjs';

const PROJECT_ROOT = path.dirname(fileURLToPath(import.meta.url));

function findNodeModules() {
  const candidates = [
    process.env.GROK_MACHINE_NODE_MODULES,
    path.join(PROJECT_ROOT, 'node_modules'),
    process.env.LOCALAPPDATA
      ? path.join(process.env.LOCALAPPDATA, 'grok-machine-mcp-runtime', 'node_modules')
      : null,
  ].filter(Boolean);

  return candidates.find((candidate) => {
    if (!existsSync(path.join(candidate, '@modelcontextprotocol', 'sdk'))) return false;
    try {
      JSON.parse(readFileSync(path.join(candidate, 'dotenv', 'package.json'), 'utf8'));
      JSON.parse(readFileSync(path.join(candidate, 'zod', 'package.json'), 'utf8'));
      return true;
    } catch {
      return false;
    }
  });
}

const NODE_MODULES = findNodeModules();
if (!NODE_MODULES) {
  throw new Error(
    'Dependencies are not installed. Run npm install, or set GROK_MACHINE_NODE_MODULES to a node_modules directory.',
  );
}

const runtimeRequire = createRequire(path.join(NODE_MODULES, '..', 'grok-machine-mcp-loader.cjs'));
const { config: loadDotenv } = runtimeRequire('dotenv');
loadDotenv({ path: path.join(PROJECT_ROOT, '.env') });

const { McpServer } = runtimeRequire('@modelcontextprotocol/sdk/server/mcp.js');
const { StreamableHTTPServerTransport } = runtimeRequire(
  '@modelcontextprotocol/sdk/server/streamableHttp.js',
);
const { isInitializeRequest } = runtimeRequire('@modelcontextprotocol/sdk/types.js');
const z = runtimeRequire('zod');

const HOST = process.env.MCP_HOST || '127.0.0.1';
const PORT = Number.parseInt(process.env.MCP_PORT || '3001', 10);
const PUBLIC_HOST = (process.env.MCP_PUBLIC_HOST || 'mcp.heartbeatobservatory.com').toLowerCase();
const AUTH_TOKEN = process.env.MCP_AUTH_TOKEN?.trim();
const DEFAULT_CWD = process.env.MCP_DEFAULT_CWD || process.cwd();
const MAX_COMMAND_TIMEOUT_MS = clampInt(process.env.MCP_MAX_COMMAND_TIMEOUT_MS, 120000, 100, 900000);
const MAX_OUTPUT_CHARS = clampInt(process.env.MCP_MAX_OUTPUT_CHARS, 200000, 1000, 1000000);
const POWERSHELL = process.env.SystemRoot
  ? path.join(process.env.SystemRoot, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe')
  : 'powershell.exe';

if (!AUTH_TOKEN || AUTH_TOKEN.length < 32 || AUTH_TOKEN === 'replace-with-a-long-random-token') {
  throw new Error(
    'MCP_AUTH_TOKEN must be set to a random value at least 32 characters long. Run scripts\\start.ps1 to create .env.',
  );
}

if (process.platform !== 'win32') {
  throw new Error('Grok Machine MCP currently supports Windows only.');
}

const allowedOrigins = new Set(
  (process.env.MCP_ALLOWED_ORIGINS || '')
    .split(',')
    .map((value) => value.trim().replace(/\/$/, '').toLowerCase())
    .filter(Boolean),
);

const OAUTH_ISSUER = (process.env.MCP_OAUTH_ISSUER || `https://${PUBLIC_HOST}`).replace(/\/$/, '');
const MCP_RESOURCE = (process.env.MCP_RESOURCE_IDENTIFIER || `${OAUTH_ISSUER}/mcp`).replace(/\/$/, '');
const OAUTH_CLIENT_ID = process.env.MCP_OAUTH_CLIENT_ID?.trim() || 'grok-machine-ios';
const OAUTH_DATA_DIR = process.env.MCP_OAUTH_DATA_DIR?.trim()
  || path.join(process.env.LOCALAPPDATA || os.homedir(), 'GrokMachineMcp');
const OAUTH_REDIRECT_URIS = (process.env.MCP_OAUTH_REDIRECT_URIS || '')
  .split(',')
  .map((value) => value.trim())
  .filter(Boolean);

// The consent form posts back to this server, so its own HTTPS origin must be
// allowed in addition to the configured Grok/xAI browser origins.
allowedOrigins.add(OAUTH_ISSUER.toLowerCase());
allowedOrigins.add(`http://${HOST}:${PORT}`.toLowerCase());

const oauth = await createOAuthService({
  issuer: OAUTH_ISSUER,
  resource: MCP_RESOURCE,
  allowedOrigins,
  dataDir: OAUTH_DATA_DIR,
  clientId: OAUTH_CLIENT_ID,
  redirectUris: OAUTH_REDIRECT_URIS,
});

const sessions = new Map();
const startedAt = new Date().toISOString();

function clampInt(raw, fallback, min, max) {
  const value = Number.parseInt(String(raw ?? ''), 10);
  if (!Number.isFinite(value)) return fallback;
  return Math.min(Math.max(value, min), max);
}

function truncate(value, max = MAX_OUTPUT_CHARS) {
  const text = String(value ?? '');
  if (text.length <= max) return text;
  return `${text.slice(0, max)}\n...[truncated at ${max} characters]`;
}

function jsonText(value, max = MAX_OUTPUT_CHARS) {
  if (typeof value === 'string') return truncate(value, max);
  try {
    return truncate(
      JSON.stringify(value, (_key, nested) =>
        typeof nested === 'bigint' ? `${nested}n` : nested,
        2,
      ),
      max,
    );
  } catch {
    return truncate(String(value), max);
  }
}

function result(value) {
  return { content: [{ type: 'text', text: jsonText(value) }] };
}

function errorResult(error) {
  const message = error instanceof Error ? error.message : String(error);
  return {
    isError: true,
    content: [{ type: 'text', text: `Error: ${truncate(message, 20000)}` }],
  };
}

function imageResult(buffer, mimeType, description) {
  return {
    content: [
      { type: 'text', text: description },
      { type: 'image', data: buffer.toString('base64'), mimeType },
    ],
  };
}

function ensurePath(value, label = 'path') {
  if (!value || typeof value !== 'string') throw new Error(`${label} is required.`);
  return path.resolve(value);
}

function ensureCwd(value) {
  const cwd = value ? ensurePath(value, 'cwd') : path.resolve(DEFAULT_CWD);
  return cwd;
}

function safeHeaderValue(value) {
  return String(value || '').replace(/[\r\n]/g, '');
}

function psBase64(value) {
  return Buffer.from(String(value), 'utf8').toString('base64');
}

function withEnv(base, values) {
  const env = { ...process.env, ...(base || {}) };
  for (const [key, value] of Object.entries(values || {})) {
    env[key] = String(value);
  }
  return env;
}

function runChild(command, args, options = {}) {
  const cwd = ensureCwd(options.cwd);
  const timeoutMs = clampInt(options.timeoutMs, MAX_COMMAND_TIMEOUT_MS, 100, 900000);
  const maxOutput = clampInt(options.maxOutputChars, MAX_OUTPUT_CHARS, 1000, 1000000);

  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd,
      env: withEnv(null, options.env),
      windowsHide: options.windowsHide ?? true,
      shell: false,
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let stdout = '';
    let stderr = '';
    let timedOut = false;
    let settled = false;

    const append = (current, chunk) => {
      const next = current + chunk.toString('utf8');
      return next.length > maxOutput ? next.slice(0, maxOutput) : next;
    };

    child.stdout.on('data', (chunk) => {
      stdout = append(stdout, chunk);
    });
    child.stderr.on('data', (chunk) => {
      stderr = append(stderr, chunk);
    });
    child.once('error', (error) => {
      if (settled) return;
      settled = true;
      reject(error);
    });

    const timer = setTimeout(() => {
      timedOut = true;
      child.kill();
    }, timeoutMs);

    child.once('close', (code, signal) => {
      clearTimeout(timer);
      if (settled) return;
      settled = true;
      resolve({
        command,
        args,
        cwd,
        code,
        signal,
        timedOut,
        stdout: truncate(stdout, maxOutput),
        stderr: truncate(stderr, maxOutput),
      });
    });
  });
}

async function runPowerShell(script, options = {}) {
  const encoded = Buffer.from(String(script), 'utf16le').toString('base64');
  const args = [
    '-NoLogo',
    '-NoProfile',
    '-NonInteractive',
    '-ExecutionPolicy',
    'Bypass',
  ];
  if (options.sta) args.push('-STA');
  args.push('-EncodedCommand', encoded);
  return runChild(POWERSHELL, args, options);
}

async function runShell(command, options = {}) {
  const shell = options.shell || 'powershell';
  if (shell === 'cmd') {
    return runChild('cmd.exe', ['/d', '/s', '/c', command], options);
  }
  if (shell === 'wsl') {
    return runChild('wsl.exe', ['--', 'bash', '-lc', command], options);
  }
  return runPowerShell(command, options);
}

function parseJsonOutput(output, fallback = null) {
  try {
    return JSON.parse(output);
  } catch {
    return fallback;
  }
}

function formatProcessResult(processResult) {
  return {
    ...processResult,
    ok: processResult.code === 0 && !processResult.timedOut,
  };
}

async function readTextFile(filePath, encoding = 'utf8') {
  const absolute = ensurePath(filePath, 'path');
  return fs.readFile(absolute, encoding);
}

async function captureScreen() {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'grok-machine-mcp-'));
  const outputPath = path.join(tempDir, 'screen.png');
  const outputB64 = psBase64(outputPath);
  const script = `
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$path = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('${outputB64}'))
$bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bounds.Size)
$bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Write-Output ($bounds.Width.ToString() + 'x' + $bounds.Height.ToString())
`;

  try {
    const commandResult = await runPowerShell(script, { sta: true, timeoutMs: 30000 });
    if (commandResult.code !== 0 || !(await fileExists(outputPath))) {
      throw new Error(commandResult.stderr || commandResult.stdout || 'Screen capture failed.');
    }
    const buffer = await fs.readFile(outputPath);
    const dimensions = commandResult.stdout.trim() || 'screen';
    return imageResult(buffer, 'image/png', `Captured the virtual desktop (${dimensions}).`);
  } finally {
    await fs.rm(tempDir, { recursive: true, force: true }).catch(() => {});
  }
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

const NATIVE_INPUT = `
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class GrokMachineInput {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint flags, uint dx, uint dy, int data, UIntPtr extraInfo);
  [DllImport("user32.dll")] public static extern void keybd_event(byte virtualKey, byte scanCode, uint flags, UIntPtr extraInfo);
  public const uint MOUSEEVENTF_MOVE = 0x0001;
  public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
  public const uint MOUSEEVENTF_LEFTUP = 0x0004;
  public const uint MOUSEEVENTF_RIGHTDOWN = 0x0008;
  public const uint MOUSEEVENTF_RIGHTUP = 0x0010;
  public const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
  public const uint MOUSEEVENTF_MIDDLEUP = 0x0040;
  public const uint MOUSEEVENTF_WHEEL = 0x0800;
  public const uint KEYEVENTF_KEYUP = 0x0002;
}
'@
`;

function mouseFlags(button, down) {
  const map = {
    left: down ? 'GrokMachineInput::MOUSEEVENTF_LEFTDOWN' : 'GrokMachineInput::MOUSEEVENTF_LEFTUP',
    right: down ? 'GrokMachineInput::MOUSEEVENTF_RIGHTDOWN' : 'GrokMachineInput::MOUSEEVENTF_RIGHTUP',
    middle: down ? 'GrokMachineInput::MOUSEEVENTF_MIDDLEDOWN' : 'GrokMachineInput::MOUSEEVENTF_MIDDLEUP',
  };
  const value = map[button];
  if (!value) throw new Error(`Unsupported mouse button: ${button}`);
  return value;
}

async function mouseMove({ x, y }) {
  const resultValue = await runPowerShell(`${NATIVE_INPUT}\n[GrokMachineInput]::SetCursorPos(${Number(x)}, ${Number(y)})`, {
    timeoutMs: 10000,
  });
  return formatProcessResult(resultValue);
}

async function mouseClick({ x, y, button = 'left', count = 1, delayMs = 60 }) {
  const move = Number.isFinite(Number(x)) && Number.isFinite(Number(y))
    ? `[GrokMachineInput]::SetCursorPos(${Number(x)}, ${Number(y)}) | Out-Null`
    : '';
  const safeCount = clampInt(count, 1, 1, 10);
  const safeDelay = clampInt(delayMs, 60, 0, 2000);
  const down = mouseFlags(button, true);
  const up = mouseFlags(button, false);
  const script = `${NATIVE_INPUT}\n${move}\nfor ($i=0; $i -lt ${safeCount}; $i++) { [GrokMachineInput]::mouse_event(${down}, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 10; [GrokMachineInput]::mouse_event(${up}, 0, 0, 0, [UIntPtr]::Zero); if (${safeDelay} -gt 0) { Start-Sleep -Milliseconds ${safeDelay} } }`;
  return formatProcessResult(await runPowerShell(script, { timeoutMs: 30000 }));
}

async function mouseDrag({ startX, startY, endX, endY, button = 'left', durationMs = 500, steps = 20 }) {
  const safeDuration = clampInt(durationMs, 500, 0, 10000);
  const safeSteps = clampInt(steps, 20, 1, 200);
  const down = mouseFlags(button, true);
  const up = mouseFlags(button, false);
  const script = `${NATIVE_INPUT}
[GrokMachineInput]::SetCursorPos(${Number(startX)}, ${Number(startY)}) | Out-Null
[GrokMachineInput]::mouse_event(${down}, 0, 0, 0, [UIntPtr]::Zero)
for ($i=1; $i -le ${safeSteps}; $i++) {
  $x = [int](${Number(startX)} + (${Number(endX)} - ${Number(startX)}) * $i / ${safeSteps})
  $y = [int](${Number(startY)} + (${Number(endY)} - ${Number(startY)}) * $i / ${safeSteps})
  [GrokMachineInput]::SetCursorPos($x, $y) | Out-Null
  Start-Sleep -Milliseconds ${Math.max(0, Math.floor(safeDuration / safeSteps))}
}
[GrokMachineInput]::mouse_event(${up}, 0, 0, 0, [UIntPtr]::Zero)`;
  return formatProcessResult(await runPowerShell(script, { timeoutMs: Math.max(30000, safeDuration + 10000) }));
}

const SEND_KEYS = {
  ENTER: '{ENTER}',
  RETURN: '{ENTER}',
  TAB: '{TAB}',
  ESC: '{ESC}',
  ESCAPE: '{ESC}',
  BACKSPACE: '{BACKSPACE}',
  BS: '{BS}',
  DELETE: '{DELETE}',
  DEL: '{DEL}',
  INSERT: '{INSERT}',
  INS: '{INS}',
  HOME: '{HOME}',
  END: '{END}',
  PAGEUP: '{PGUP}',
  PAGEDOWN: '{PGDN}',
  PGUP: '{PGUP}',
  PGDN: '{PGDN}',
  UP: '{UP}',
  DOWN: '{DOWN}',
  LEFT: '{LEFT}',
  RIGHT: '{RIGHT}',
  SPACE: ' ',
  F1: '{F1}', F2: '{F2}', F3: '{F3}', F4: '{F4}', F5: '{F5}', F6: '{F6}',
  F7: '{F7}', F8: '{F8}', F9: '{F9}', F10: '{F10}', F11: '{F11}', F12: '{F12}',
  PRINTSCREEN: '{PRTSC}',
};

function sendKeysExpression(key) {
  const normalized = String(key || '').trim().toUpperCase();
  if (!normalized) throw new Error('key is required.');
  if (SEND_KEYS[normalized]) return SEND_KEYS[normalized];
  if (/^[A-Z0-9]$/.test(normalized)) return normalized.toLowerCase();
  if (/^F(?:1[3-9]|2[0-4])$/.test(normalized)) return `{${normalized}}`;
  throw new Error(`Unsupported key: ${key}`);
}

async function keyPress({ key, repeat = 1, delayMs = 40 }) {
  const expression = sendKeysExpression(key);
  const safeRepeat = clampInt(repeat, 1, 1, 20);
  const safeDelay = clampInt(delayMs, 40, 0, 2000);
  const script = `Add-Type -AssemblyName System.Windows.Forms\nfor ($i=0; $i -lt ${safeRepeat}; $i++) { [System.Windows.Forms.SendKeys]::SendWait(${JSON.stringify(expression)}); if (${safeDelay} -gt 0) { Start-Sleep -Milliseconds ${safeDelay} } }`;
  return formatProcessResult(await runPowerShell(script, { sta: true, timeoutMs: 30000 }));
}

function modifierExpression(modifier) {
  const normalized = String(modifier || '').trim().toUpperCase();
  const map = { CTRL: '^', CONTROL: '^', ALT: '%', SHIFT: '+', WIN: '#', WINDOWS: '#' };
  if (!map[normalized]) throw new Error(`Unsupported modifier: ${modifier}`);
  return map[normalized];
}

async function hotkey({ modifiers, key }) {
  if (!Array.isArray(modifiers) || modifiers.length === 0) throw new Error('modifiers must contain at least one key.');
  const expression = `${modifiers.map(modifierExpression).join('')}${sendKeysExpression(key)}`;
  const script = `Add-Type -AssemblyName System.Windows.Forms\n[System.Windows.Forms.SendKeys]::SendWait(${JSON.stringify(expression)})`;
  return formatProcessResult(await runPowerShell(script, { sta: true, timeoutMs: 30000 }));
}

async function typeText({ text, paste = true }) {
  if (!paste) {
    const encoded = psBase64(text);
    const script = `Add-Type -AssemblyName System.Windows.Forms\n$text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:GROK_TEXT_B64))\n[System.Windows.Forms.SendKeys]::SendWait($text)`;
    return formatProcessResult(await runPowerShell(script, {
      sta: true,
      timeoutMs: 30000,
      env: { GROK_TEXT_B64: encoded },
    }));
  }

  const encoded = psBase64(text);
  const script = `Add-Type -AssemblyName System.Windows.Forms\n$text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:GROK_TEXT_B64))\n[System.Windows.Forms.Clipboard]::SetText($text)\n[System.Windows.Forms.SendKeys]::SendWait('^v')`;
  return formatProcessResult(await runPowerShell(script, {
    sta: true,
    timeoutMs: 30000,
    env: { GROK_TEXT_B64: encoded },
  }));
}

async function getClipboard() {
  const script = `Add-Type -AssemblyName System.Windows.Forms\n[System.Windows.Forms.Clipboard]::GetText()`;
  const value = await runPowerShell(script, { sta: true, timeoutMs: 10000 });
  return { ...formatProcessResult(value), text: value.stdout };
}

async function setClipboard({ text }) {
  const script = `Add-Type -AssemblyName System.Windows.Forms\n$text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:GROK_TEXT_B64))\n[System.Windows.Forms.Clipboard]::SetText($text)`;
  return formatProcessResult(await runPowerShell(script, {
    sta: true,
    timeoutMs: 10000,
    env: { GROK_TEXT_B64: psBase64(text) },
  }));
}

const WINDOW_NATIVE = `
Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public static class GrokMachineWindows {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr extraData);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int command);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
  public static string Title(IntPtr hWnd) {
    var buffer = new StringBuilder(1024);
    GetWindowText(hWnd, buffer, buffer.Capacity);
    return buffer.ToString();
  }
}
'@
`;

async function activeWindow() {
  const script = `${WINDOW_NATIVE}
$handle = [GrokMachineWindows]::GetForegroundWindow()
$rect = New-Object GrokMachineWindows+RECT
[GrokMachineWindows]::GetWindowRect($handle, [ref]$rect) | Out-Null
[PSCustomObject]@{ handle = $handle.ToInt64(); title = [GrokMachineWindows]::Title($handle); left = $rect.Left; top = $rect.Top; right = $rect.Right; bottom = $rect.Bottom } | ConvertTo-Json -Compress`;
  const value = await runPowerShell(script, { timeoutMs: 10000 });
  return { ...formatProcessResult(value), window: parseJsonOutput(value.stdout.trim()) };
}

async function listWindows() {
  const script = `Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle } | Sort-Object ProcessName | Select-Object ProcessName, Id, MainWindowTitle, @{Name='Handle';Expression={$_.MainWindowHandle.ToInt64()}} | ConvertTo-Json -Compress`;
  const value = await runPowerShell(script, { timeoutMs: 20000 });
  return { ...formatProcessResult(value), windows: parseJsonOutput(value.stdout.trim(), []) || [] };
}

async function focusWindow({ handle, processId, title }) {
  const encodedTitle = psBase64(title || '');
  const script = `${WINDOW_NATIVE}
$target = [IntPtr]::Zero
if (${Number.isFinite(Number(handle)) ? `$target = [IntPtr]::new(${Number(handle)})` : '$false'}) { }
if ($target -eq [IntPtr]::Zero -and ${Number.isFinite(Number(processId)) ? '$true' : '$false'}) {
  $p = Get-Process -Id ${Number(processId)} -ErrorAction Stop
  $target = $p.MainWindowHandle
}
if ($target -eq [IntPtr]::Zero -and $env:GROK_TITLE_B64) {
  $wanted = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($env:GROK_TITLE_B64))
  $p = Get-Process | Where-Object { $_.MainWindowTitle -like ('*' + $wanted + '*') } | Select-Object -First 1
  if ($p) { $target = $p.MainWindowHandle }
}
if ($target -eq [IntPtr]::Zero) { throw 'No matching window found.' }
[GrokMachineWindows]::ShowWindow($target, 9) | Out-Null
[GrokMachineWindows]::SetForegroundWindow($target) | Out-Null
[PSCustomObject]@{ handle = $target.ToInt64(); title = [GrokMachineWindows]::Title($target) } | ConvertTo-Json -Compress`;
  const value = await runPowerShell(script, {
    timeoutMs: 10000,
    env: { GROK_TITLE_B64: encodedTitle },
  });
  return { ...formatProcessResult(value), window: parseJsonOutput(value.stdout.trim()) };
}

async function listProcesses({ name } = {}) {
  const script = name
    ? `Get-Process -Name $env:GROK_PROCESS_NAME -ErrorAction SilentlyContinue | Select-Object ProcessName, Id, MainWindowTitle, Path, CPU, WorkingSet64, StartTime | ConvertTo-Json -Compress`
    : `Get-Process | Sort-Object ProcessName | Select-Object ProcessName, Id, MainWindowTitle, Path, CPU, WorkingSet64, StartTime | ConvertTo-Json -Compress`;
  const value = await runPowerShell(script, {
    timeoutMs: 30000,
    env: { GROK_PROCESS_NAME: name || '' },
  });
  return { ...formatProcessResult(value), processes: parseJsonOutput(value.stdout.trim(), []) || [] };
}

async function launchProcess({ target, args = [], cwd, wait = false }) {
  if (!target) throw new Error('target is required.');
  const absoluteTarget = target.includes('\\') || target.includes('/') ? path.resolve(target) : target;
  if (/^https?:\/\//i.test(target)) {
    const value = await runPowerShell(`Start-Process -FilePath $env:GROK_TARGET`, { env: { GROK_TARGET: target }, timeoutMs: 10000 });
    return formatProcessResult(value);
  }
  const child = spawn(absoluteTarget, Array.isArray(args) ? args.map(String) : [], {
    cwd: cwd ? ensureCwd(cwd) : undefined,
    windowsHide: false,
    detached: !wait,
    stdio: wait ? ['ignore', 'pipe', 'pipe'] : 'ignore',
  });
  if (!wait) {
    child.unref();
    return { started: true, pid: child.pid, target: absoluteTarget, args };
  }
  return new Promise((resolve, reject) => {
    let stdout = '';
    let stderr = '';
    child.stdout?.on('data', (chunk) => { stdout += chunk.toString('utf8'); });
    child.stderr?.on('data', (chunk) => { stderr += chunk.toString('utf8'); });
    child.once('error', reject);
    child.once('close', (code, signal) => resolve({ started: true, pid: child.pid, code, signal, stdout: truncate(stdout), stderr: truncate(stderr) }));
  });
}

async function stopProcess({ processId, name, force = false }) {
  if (!Number.isFinite(Number(processId)) && !name) throw new Error('processId or name is required.');
  const script = `
$targets = @()
if (${Number.isFinite(Number(processId)) ? '$true' : '$false'}) { $targets += Get-Process -Id ${Number(processId)} -ErrorAction Stop }
if (${name ? '$true' : '$false'}) { $targets += Get-Process -Name $env:GROK_PROCESS_NAME -ErrorAction Stop }
$targets | Sort-Object Id -Unique | Stop-Process -Force:${force ? '$true' : '$false'} -ErrorAction Stop
$targets | Select-Object ProcessName, Id | ConvertTo-Json -Compress`;
  const value = await runPowerShell(script, {
    timeoutMs: 30000,
    env: { GROK_PROCESS_NAME: name || '' },
  });
  return { ...formatProcessResult(value), stopped: parseJsonOutput(value.stdout.trim(), []) || [] };
}

async function systemInfo() {
  const script = `
$osInfo = Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, LastBootUpTime, OSArchitecture
$computer = Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory, UserName
$gpu = Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion, AdapterRAM
[PSCustomObject]@{ os = $osInfo; computer = $computer; gpu = $gpu } | ConvertTo-Json -Depth 5 -Compress`;
  const value = await runPowerShell(script, { timeoutMs: 30000 });
  return { ...formatProcessResult(value), node: { version: process.version, platform: process.platform, arch: process.arch }, info: parseJsonOutput(value.stdout.trim()) };
}

async function listDirectory({ path: directoryPath, recursive = false, maxEntries = 500, includeHidden = false }) {
  const root = ensurePath(directoryPath || DEFAULT_CWD, 'path');
  const limit = clampInt(maxEntries, 500, 1, 10000);
  const entries = [];
  const pending = [root];
  while (pending.length && entries.length < limit) {
    const current = pending.shift();
    const children = await fs.readdir(current, { withFileTypes: true });
    for (const child of children) {
      if (!includeHidden && child.name.startsWith('.')) continue;
      const childPath = path.join(current, child.name);
      let stat = null;
      try { stat = await fs.stat(childPath); } catch { /* race or restricted entry */ }
      entries.push({
        path: childPath,
        name: child.name,
        type: child.isDirectory() ? 'directory' : child.isFile() ? 'file' : 'other',
        size: stat?.size ?? null,
        modified: stat?.mtime?.toISOString() ?? null,
      });
      if (recursive && child.isDirectory() && entries.length < limit) pending.push(childPath);
      if (entries.length >= limit) break;
    }
  }
  return { root, recursive, count: entries.length, truncated: pending.length > 0 || entries.length >= limit, entries };
}

async function searchFiles({ path: rootPath, query, regex = false, recursive = true, maxResults = 100, includeHidden = false }) {
  const root = ensurePath(rootPath || DEFAULT_CWD, 'path');
  if (!query) throw new Error('query is required.');
  const limit = clampInt(maxResults, 100, 1, 2000);
  const matcher = regex ? new RegExp(query, 'i') : null;
  const results = [];
  const pending = [root];
  while (pending.length && results.length < limit) {
    const current = pending.shift();
    const children = await fs.readdir(current, { withFileTypes: true });
    for (const child of children) {
      if (!includeHidden && child.name.startsWith('.')) continue;
      const childPath = path.join(current, child.name);
      if (child.isDirectory()) {
        if (recursive) pending.push(childPath);
        continue;
      }
      if (!child.isFile()) continue;
      if (regex ? matcher.test(child.name) : child.name.toLowerCase().includes(String(query).toLowerCase())) {
        results.push(childPath);
      }
      if (results.length >= limit) break;
    }
  }
  return { root, query, count: results.length, truncated: pending.length > 0, matches: results };
}

async function registerTools(server) {
  const readOnly = { readOnlyHint: true, openWorldHint: false };
  const destructive = { destructiveHint: true, openWorldHint: false };

  server.registerTool('shell_exec', {
    title: 'Run Shell Command',
    description: 'Run an arbitrary PowerShell, cmd.exe, or WSL command as the current Windows user and return stdout, stderr, and exit status.',
    inputSchema: {
      command: z.string().describe('The command or script to run.'),
      shell: z.enum(['powershell', 'cmd', 'wsl']).optional().describe('Shell backend; defaults to PowerShell.'),
      cwd: z.string().optional().describe('Working directory; defaults to the configured workspace directory.'),
      timeoutMs: z.number().int().min(100).max(900000).optional().describe('Maximum runtime in milliseconds.'),
    },
    annotations: destructive,
  }, async ({ command, shell, cwd, timeoutMs }) => {
    try { return result(formatProcessResult(await runShell(command, { shell, cwd, timeoutMs }))); } catch (error) { return errorResult(error); }
  });

  server.registerTool('read_file', {
    title: 'Read File',
    description: 'Read a text or binary file from Windows.',
    inputSchema: {
      path: z.string().describe('Absolute or relative file path.'),
      encoding: z.enum(['utf8', 'base64']).optional().describe('Return encoding; defaults to utf8.'),
      maxBytes: z.number().int().min(1).max(50000000).optional().describe('Maximum bytes to return.'),
    },
    annotations: readOnly,
  }, async ({ path: filePath, encoding = 'utf8', maxBytes = MAX_OUTPUT_CHARS }) => {
    try {
      const absolute = ensurePath(filePath);
      const data = await fs.readFile(absolute);
      const limited = data.subarray(0, Math.min(data.length, maxBytes));
      return result({ path: absolute, bytes: data.length, truncated: limited.length < data.length, encoding, content: encoding === 'base64' ? limited.toString('base64') : limited.toString('utf8') });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool('write_file', {
    title: 'Write File',
    description: 'Create or overwrite a file with text or base64 data.',
    inputSchema: {
      path: z.string(),
      content: z.string(),
      encoding: z.enum(['utf8', 'base64']).optional(),
      createDirs: z.boolean().optional(),
    },
    annotations: destructive,
  }, async ({ path: filePath, content, encoding = 'utf8', createDirs = true }) => {
    try {
      const absolute = ensurePath(filePath);
      if (createDirs) await fs.mkdir(path.dirname(absolute), { recursive: true });
      const data = encoding === 'base64' ? Buffer.from(content, 'base64') : Buffer.from(content, 'utf8');
      await fs.writeFile(absolute, data);
      return result({ path: absolute, bytes: data.length, encoding });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool('list_directory', {
    title: 'List Directory',
    description: 'List files and directories, optionally recursively.',
    inputSchema: {
      path: z.string().optional(),
      recursive: z.boolean().optional(),
      maxEntries: z.number().int().min(1).max(10000).optional(),
      includeHidden: z.boolean().optional(),
    },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await listDirectory(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('search_files', {
    title: 'Search Files',
    description: 'Find files by filename substring or case-insensitive regular expression.',
    inputSchema: {
      path: z.string().optional(),
      query: z.string(),
      regex: z.boolean().optional(),
      recursive: z.boolean().optional(),
      maxResults: z.number().int().min(1).max(2000).optional(),
      includeHidden: z.boolean().optional(),
    },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await searchFiles(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('copy_path', {
    title: 'Copy File or Directory',
    description: 'Copy a file or directory to another path.',
    inputSchema: { source: z.string(), destination: z.string(), overwrite: z.boolean().optional() },
    annotations: destructive,
  }, async ({ source, destination, overwrite = true }) => {
    try {
      const from = ensurePath(source, 'source');
      const to = ensurePath(destination, 'destination');
      await fs.cp(from, to, { recursive: true, force: overwrite, errorOnExist: !overwrite });
      return result({ source: from, destination: to, overwrite });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool('move_path', {
    title: 'Move File or Directory',
    description: 'Move or rename a file or directory.',
    inputSchema: { source: z.string(), destination: z.string(), overwrite: z.boolean().optional() },
    annotations: destructive,
  }, async ({ source, destination, overwrite = false }) => {
    try {
      const from = ensurePath(source, 'source');
      const to = ensurePath(destination, 'destination');
      if (overwrite) await fs.rm(to, { recursive: true, force: true });
      await fs.rename(from, to);
      return result({ source: from, destination: to, overwrite });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool('delete_path', {
    title: 'Delete File or Directory',
    description: 'Delete a file or directory. Recursive deletion is available for directories.',
    inputSchema: { path: z.string(), recursive: z.boolean().optional() },
    annotations: destructive,
  }, async ({ path: filePath, recursive = false }) => {
    try {
      const absolute = ensurePath(filePath);
      await fs.rm(absolute, { recursive, force: false });
      return result({ deleted: absolute, recursive });
    } catch (error) { return errorResult(error); }
  });

  server.registerTool('make_directory', {
    title: 'Create Directory',
    description: 'Create a directory and its missing parents.',
    inputSchema: { path: z.string() },
    annotations: destructive,
  }, async ({ path: directoryPath }) => {
    try { const absolute = ensurePath(directoryPath); await fs.mkdir(absolute, { recursive: true }); return result({ created: absolute }); } catch (error) { return errorResult(error); }
  });

  server.registerTool('path_info', {
    title: 'Path Info',
    description: 'Inspect file or directory metadata.',
    inputSchema: { path: z.string() },
    annotations: readOnly,
  }, async ({ path: filePath }) => {
    try { const absolute = ensurePath(filePath); const stat = await fs.stat(absolute); return result({ path: absolute, type: stat.isDirectory() ? 'directory' : stat.isFile() ? 'file' : 'other', size: stat.size, created: stat.birthtime.toISOString(), modified: stat.mtime.toISOString(), accessed: stat.atime.toISOString() }); } catch (error) { return errorResult(error); }
  });

  server.registerTool('screen_capture', {
    title: 'Capture Screen',
    description: 'Capture the entire virtual Windows desktop and return it as an image.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return await captureScreen(); } catch (error) { return errorResult(error); }
  });

  server.registerTool('mouse_move', {
    title: 'Move Mouse',
    description: 'Move the Windows cursor to screen coordinates.',
    inputSchema: { x: z.number().int(), y: z.number().int() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await mouseMove(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('mouse_click', {
    title: 'Click Mouse',
    description: 'Move optionally and click the Windows mouse.',
    inputSchema: { x: z.number().int().optional(), y: z.number().int().optional(), button: z.enum(['left', 'right', 'middle']).optional(), count: z.number().int().min(1).max(10).optional(), delayMs: z.number().int().min(0).max(2000).optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await mouseClick(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('mouse_drag', {
    title: 'Drag Mouse',
    description: 'Drag the mouse from one screen coordinate to another.',
    inputSchema: { startX: z.number().int(), startY: z.number().int(), endX: z.number().int(), endY: z.number().int(), button: z.enum(['left', 'right', 'middle']).optional(), durationMs: z.number().int().min(0).max(10000).optional(), steps: z.number().int().min(1).max(200).optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await mouseDrag(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('key_press', {
    title: 'Press Key',
    description: 'Send a key to the active Windows application.',
    inputSchema: { key: z.string(), repeat: z.number().int().min(1).max(20).optional(), delayMs: z.number().int().min(0).max(2000).optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await keyPress(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('hotkey', {
    title: 'Press Hotkey',
    description: 'Send a modifier-plus-key shortcut to the active Windows application.',
    inputSchema: { modifiers: z.array(z.string()).min(1), key: z.string() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await hotkey(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('type_text', {
    title: 'Type Text',
    description: 'Type text into the active Windows application, using the clipboard-paste path by default for Unicode reliability.',
    inputSchema: { text: z.string(), paste: z.boolean().optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await typeText(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('clipboard_get', {
    title: 'Read Clipboard',
    description: 'Read text from the Windows clipboard.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await getClipboard()); } catch (error) { return errorResult(error); }
  });

  server.registerTool('clipboard_set', {
    title: 'Write Clipboard',
    description: 'Replace the Windows clipboard with text.',
    inputSchema: { text: z.string() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await setClipboard(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('active_window', {
    title: 'Active Window',
    description: 'Inspect the current foreground window and its screen bounds.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await activeWindow()); } catch (error) { return errorResult(error); }
  });

  server.registerTool('list_windows', {
    title: 'List Windows',
    description: 'List visible top-level application windows.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await listWindows()); } catch (error) { return errorResult(error); }
  });

  server.registerTool('focus_window', {
    title: 'Focus Window',
    description: 'Bring a window to the foreground by handle, process ID, or title substring.',
    inputSchema: { handle: z.number().int().optional(), processId: z.number().int().optional(), title: z.string().optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await focusWindow(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('list_processes', {
    title: 'List Processes',
    description: 'List running Windows processes, optionally filtered by process name.',
    inputSchema: { name: z.string().optional() },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await listProcesses(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('launch_process', {
    title: 'Launch Application',
    description: 'Launch an application, executable, document, or URL. Runs as the current Windows user.',
    inputSchema: { target: z.string(), args: z.array(z.string()).optional(), cwd: z.string().optional(), wait: z.boolean().optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await launchProcess(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('stop_process', {
    title: 'Stop Process',
    description: 'Stop a Windows process by ID or name.',
    inputSchema: { processId: z.number().int().optional(), name: z.string().optional(), force: z.boolean().optional() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await stopProcess(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('open_url', {
    title: 'Open URL',
    description: 'Open a URL in the default Windows browser.',
    inputSchema: { url: z.string().url() },
    annotations: destructive,
  }, async ({ url }) => {
    try { return result(await launchProcess({ target: url })); } catch (error) { return errorResult(error); }
  });

  server.registerTool('system_info', {
    title: 'System Information',
    description: 'Inspect Windows, computer, GPU, and runtime information.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await systemInfo()); } catch (error) { return errorResult(error); }
  });

  // ===== New foundation tools (tasks, verify, ollama, registry) =====

  server.registerTool('task_start', {
    title: 'Start Task',
    description: 'Create a durable background task with an objective. Returns a task ID that can be polled later.',
    inputSchema: {
      title: z.string().optional(),
      objective: z.string(),
      command: z.string().optional(),
      cwd: z.string().optional(),
    },
    annotations: destructive,
  }, async (args) => {
    try { return result(await tasks.taskStart(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('task_status', {
    title: 'Task Status',
    description: 'Get the current status of a durable task by ID.',
    inputSchema: { id: z.string() },
    annotations: readOnly,
  }, async ({ id }) => {
    try { return result(await tasks.taskStatus(id)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('task_logs', {
    title: 'Task Logs',
    description: 'Read logs from a durable task.',
    inputSchema: { id: z.string(), limit: z.number().int().optional(), offset: z.number().int().optional() },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await tasks.taskLogs(args.id, { limit: args.limit, offset: args.offset })); } catch (error) { return errorResult(error); }
  });

  server.registerTool('task_artifacts', {
    title: 'Task Artifacts',
    description: 'List artifacts produced by a durable task.',
    inputSchema: { id: z.string() },
    annotations: readOnly,
  }, async ({ id }) => {
    try { return result(await tasks.taskArtifacts(id)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('task_cancel', {
    title: 'Cancel Task',
    description: 'Cancel a running or pending durable task.',
    inputSchema: { id: z.string(), reason: z.string().optional() },
    annotations: destructive,
  }, async ({ id, reason }) => {
    try { return result(await tasks.taskCancel(id, reason)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('task_continue', {
    title: 'Continue Task',
    description: 'Mark a task as continuing / running and optionally append a note.',
    inputSchema: { id: z.string(), note: z.string().optional() },
    annotations: destructive,
  }, async ({ id, note }) => {
    try { return result(await tasks.taskContinue(id, note)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('task_list', {
    title: 'List Recent Tasks',
    description: 'List recent durable tasks.',
    inputSchema: { limit: z.number().int().optional() },
    annotations: readOnly,
  }, async ({ limit }) => {
    try { return result(await tasks.listRecentTasks({ limit })); } catch (error) { return errorResult(error); }
  });

  server.registerTool('verify_file_exists', {
    title: 'Verify File Exists',
    description: 'Check whether a file or directory exists and return metadata.',
    inputSchema: { path: z.string() },
    annotations: readOnly,
  }, async ({ path: p }) => {
    try { return result(await verify.verifyFileExists(p)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('verify_process_running', {
    title: 'Verify Process Running',
    description: 'Check whether a process is running by name or PID.',
    inputSchema: { name: z.string().optional(), processId: z.number().int().optional() },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await verify.verifyProcessRunning(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('verify_port_open', {
    title: 'Verify Port Open',
    description: 'Check whether a TCP port is accepting connections.',
    inputSchema: { port: z.number().int(), host: z.string().optional() },
    annotations: readOnly,
  }, async ({ port, host }) => {
    try { return result(await verify.verifyPortOpen(port, host)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('verify_http_response', {
    title: 'Verify HTTP Response',
    description: 'Fetch a URL and report status code and basic headers.',
    inputSchema: { url: z.string(), expectStatus: z.number().int().optional(), timeoutMs: z.number().int().optional() },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await verify.verifyHttpResponse(args.url, args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('verify_git_status', {
    title: 'Verify Git Status',
    description: 'Run git status in a repository and report clean/dirty state.',
    inputSchema: { path: z.string() },
    annotations: readOnly,
  }, async ({ path: p }) => {
    try { return result(await verify.verifyGitStatus(p)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('verify_window_visible', {
    title: 'Verify Window Visible',
    description: 'Check whether a top-level window with a given title or process is visible.',
    inputSchema: { title: z.string().optional(), processId: z.number().int().optional() },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await verify.verifyWindowVisible(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('ollama_models', {
    title: 'Ollama Models',
    description: 'List locally available Ollama models.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await ollama.ollamaModels()); } catch (error) { return errorResult(error); }
  });

  server.registerTool('ollama_chat', {
    title: 'Ollama Chat',
    description: 'Chat with a local Ollama model.',
    inputSchema: {
      model: z.string(),
      messages: z.array(z.object({ role: z.string(), content: z.string() })),
      system: z.string().optional(),
      temperature: z.number().optional(),
      format: z.unknown().optional(),
    },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await ollama.ollamaChat(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('ollama_generate', {
    title: 'Ollama Generate',
    description: 'Generate a completion from a local Ollama model.',
    inputSchema: {
      model: z.string(),
      prompt: z.string(),
      system: z.string().optional(),
      temperature: z.number().optional(),
      format: z.unknown().optional(),
    },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await ollama.ollamaGenerate(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('ollama_embeddings', {
    title: 'Ollama Embeddings',
    description: 'Generate embeddings with a local Ollama model.',
    inputSchema: { model: z.string(), prompt: z.string() },
    annotations: readOnly,
  }, async (args) => {
    try { return result(await ollama.ollamaEmbeddings(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('ollama_pull', {
    title: 'Ollama Pull',
    description: 'Pull a model into Ollama. Prefer wrapping long pulls in a durable task.',
    inputSchema: { model: z.string() },
    annotations: destructive,
  }, async (args) => {
    try { return result(await ollama.ollamaPull(args)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('ollama_ps', {
    title: 'Ollama Running Models',
    description: 'List models currently loaded in Ollama memory.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await ollama.ollamaPs()); } catch (error) { return errorResult(error); }
  });

  server.registerTool('registry_list', {
    title: 'Registry List',
    description: 'List known projects, ports, and models from the machine registry.',
    inputSchema: {},
    annotations: readOnly,
  }, async () => {
    try { return result(await registry.registryList()); } catch (error) { return errorResult(error); }
  });

  server.registerTool('registry_get', {
    title: 'Registry Get Project',
    description: 'Get details for a registered project by ID.',
    inputSchema: { id: z.string() },
    annotations: readOnly,
  }, async ({ id }) => {
    try { return result(await registry.registryGet(id)); } catch (error) { return errorResult(error); }
  });

  server.registerTool('registry_upsert', {
    title: 'Registry Upsert Project',
    description: 'Create or update a project entry in the machine registry.',
    inputSchema: {
      id: z.string(),
      name: z.string().optional(),
      path: z.string().optional(),
      type: z.string().optional(),
      notes: z.string().optional(),
    },
    annotations: destructive,
  }, async (args) => {
    try {
      const { id, ...data } = args;
      return result(await registry.registryUpsert(id, data));
    } catch (error) { return errorResult(error); }
  });

}

function createMcpServer() {
  const server = new McpServer({
    name: 'grok-machine',
    version: '0.1.0',
    websiteUrl: `https://${PUBLIC_HOST}`,
    description: 'Windows desktop, file, shell, process, and UI control for the paired computer.',
  });
  server.registerPrompt?.('computer_operator', {
    title: 'Computer Operator',
    description: 'Use the paired Windows computer through Grok Machine tools.',
    argsSchema: {},
  }, async () => ({
    messages: [{ role: 'user', content: { type: 'text', text: 'Operate the paired Windows computer directly. Use screen_capture and active_window when visual state matters; use shell_exec for exact file or terminal work.' } }],
  }));
  registerTools(server);
  return server;
}

function requestOriginAllowed(req) {
  const origin = String(req.headers.origin || '').trim().replace(/\/$/, '').toLowerCase();
  if (!origin) return true;
  return allowedOrigins.size === 0 || allowedOrigins.has(origin);
}

function requestHostAllowed(req) {
  const raw = String(req.headers.host || '').toLowerCase();
  if (!raw) return true;
  const host = raw.replace(/^\[/, '').split(']')[0].split(':')[0];
  return host === 'localhost' || host === '127.0.0.1' || host === PUBLIC_HOST;
}

function authenticate(req) {
  const raw = String(req.headers.authorization || '');
  const match = raw.match(/^Bearer\s+(.+)$/i);
  const candidate = match ? match[1].trim() : raw.trim();
  if (!candidate) return { ok: false, reason: 'missing' };

  const oauthToken = oauth.validateAccessToken(candidate);
  if (oauthToken) return { ok: true, kind: 'oauth', record: oauthToken };

  const expected = Buffer.from(AUTH_TOKEN, 'utf8');
  const actual = Buffer.from(candidate, 'utf8');
  if (expected.length === actual.length && timingSafeEqual(expected, actual)) {
    return { ok: true, kind: 'legacy' };
  }
  return { ok: false, reason: 'invalid' };
}

function writeJson(res, status, body, extraHeaders = {}) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    ...extraHeaders,
  });
  res.end(payload);
}

function applyCors(req, res) {
  const origin = String(req.headers.origin || '').trim();
  if (origin && requestOriginAllowed(req)) {
    res.setHeader('Access-Control-Allow-Origin', safeHeaderValue(origin));
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type, MCP-Protocol-Version, MCP-Session-Id, Last-Event-ID');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Expose-Headers', 'MCP-Session-Id, MCP-Protocol-Version, Last-Event-ID');
}

function rejectRequest(req, res, status, message, oauthError) {
  applyCors(req, res);
  if (status === 401) {
    res.setHeader('WWW-Authenticate', oauth.challenge(oauthError?.error, oauthError?.description));
  }
  writeJson(res, status, { error: message });
}

async function readJsonBody(req) {
  const chunks = [];
  let total = 0;
  for await (const chunk of req) {
    total += chunk.length;
    if (total > 5000000) throw new Error('Request body too large.');
    chunks.push(chunk);
  }
  if (chunks.length === 0) return undefined;
  const text = Buffer.concat(chunks).toString('utf8');
  return JSON.parse(text);
}

// 10/17 (Jaron: "is the alert because they CAN'T reach it, or just haven't?"): remember the last good / expired-token /
// no-token visit so tools/connector-watch.py can tell a broken sign-in from bots that are simply quiet. Written at most
// once a minute per kind. Names only, no tokens.
const HITS_FILE = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'state', 'connector-hits.json');
const hitsLastWrite = {};
function noteHit(kind) {
  const now = Date.now();
  if (hitsLastWrite[kind] && now - hitsLastWrite[kind] < 60000) return;
  hitsLastWrite[kind] = now;
  let cur = {};
  try { cur = JSON.parse(readFileSync(HITS_FILE, 'utf8')); } catch {}
  cur[kind] = new Date(now).toISOString();
  fs.writeFile(HITS_FILE, JSON.stringify(cur, null, 1)).catch(() => {});
}

async function handleMcp(req, res) {
  applyCors(req, res);
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  if (!requestHostAllowed(req)) return rejectRequest(req, res, 403, 'Invalid Host header.');
  if (!requestOriginAllowed(req)) return rejectRequest(req, res, 403, 'Invalid Origin header.');
  const authResult = authenticate(req);
  if (!authResult.ok) {
    const invalid = authResult.reason === 'invalid';
    if (req.method !== 'OPTIONS') noteHit(invalid ? 'last_expired_token' : 'last_no_token');
    return rejectRequest(
      req,
      res,
      401,
      invalid ? 'Invalid or expired access token.' : 'OAuth authorization required.',
      invalid ? { error: 'invalid_token', description: 'The access token is invalid or expired.' } : undefined,
    );
  }

  noteHit('last_ok');
  let body;
  try {
    if (req.method === 'POST') body = await readJsonBody(req);
  } catch (error) {
    return rejectRequest(req, res, 400, error instanceof Error ? error.message : String(error));
  }

  const sessionId = String(req.headers['mcp-session-id'] || '');
  try {
    let transport = sessionId ? sessions.get(sessionId) : null;
    if (!transport && req.method === 'POST' && !sessionId && body && isInitializeRequest(body)) {
      let server;
      transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => randomUUID(),
        onsessioninitialized: (newSessionId) => {
          sessions.set(newSessionId, transport);
          console.log(`[mcp] session initialized ${newSessionId}`);
        },
      });
      transport.onclose = () => {
        if (transport?.sessionId) {
          sessions.delete(transport.sessionId);
          console.log(`[mcp] session closed ${transport.sessionId}`);
        }
      };
      server = createMcpServer();
      await server.connect(transport);
      await transport.handleRequest(req, res, body);
      return;
    }

    if (!transport) {
      return rejectRequest(req, res, 400, 'A valid MCP session is required.');
    }
    await transport.handleRequest(req, res, body);
  } catch (error) {
    console.error('[mcp] request failed:', error instanceof Error ? error.message : error);
    if (!res.headersSent) writeJson(res, 500, { error: 'Internal MCP server error.' });
  }
}

const httpServer = createHttpServer(async (req, res) => {
  const requestUrl = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
  if (requestUrl.pathname.startsWith('/.well-known/') || requestUrl.pathname.startsWith('/oauth/')) {
    if (!requestHostAllowed(req)) return rejectRequest(req, res, 403, 'Invalid Host header.');
    if (!requestOriginAllowed(req)) return rejectRequest(req, res, 403, 'Invalid Origin header.');
    if (await oauth.handle(req, res, requestUrl)) return;
  }
  if (requestUrl.pathname === '/healthz') {
    writeJson(res, 200, {
      ok: true,
      service: 'grok-machine-mcp',
      startedAt,
      host: HOST,
      port: PORT,
      auth: true,
      sessions: sessions.size,
      oauth: {
        issuer: oauth.issuer,
        resource: oauth.resource,
        clientId: oauth.clientId,
        authorizationEndpoint: `${oauth.issuer}/oauth/authorize`,
        tokenEndpoint: `${oauth.issuer}/oauth/token`,
        scopes: ['mcp:tools'],
        tokenEndpointAuthMethod: 'none',
      },
    });
    return;
  }
  if (requestUrl.pathname === '/mcp') {
    await handleMcp(req, res);
    return;
  }
  if (requestUrl.pathname === '/') {
    writeJson(res, 200, { service: 'grok-machine-mcp', endpoint: '/mcp', health: '/healthz' });
    return;
  }
  writeJson(res, 404, { error: 'Not found.' });
});

httpServer.on('clientError', (error, socket) => {
  console.error('[http] client error:', error.message);
  socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
});

httpServer.listen(PORT, HOST, () => {
  console.log(`[grok-machine-mcp] listening on http://${HOST}:${PORT}`);
  console.log(`[grok-machine-mcp] MCP endpoint: https://${PUBLIC_HOST}/mcp`);
  console.log(`[grok-machine-mcp] tools run as Windows user: ${process.env.USERNAME || os.userInfo().username}`);
});

async function shutdown(signal) {
  console.log(`[grok-machine-mcp] ${signal}; closing ${sessions.size} MCP session(s)`);
  for (const transport of sessions.values()) await transport.close().catch(() => {});
  httpServer.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000).unref();
}

process.once('SIGINT', () => { void shutdown('SIGINT'); });
process.once('SIGTERM', () => { void shutdown('SIGTERM'); });
