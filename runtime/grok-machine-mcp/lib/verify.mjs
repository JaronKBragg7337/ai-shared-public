import * as fs from 'node:fs/promises';
import * as net from 'node:net';
import { spawn } from 'node:child_process';
import * as path from 'node:path';

export async function verifyFileExists(filePath) {
  try {
    await fs.access(filePath);
    const stat = await fs.stat(filePath);
    return {
      ok: true,
      path: path.resolve(filePath),
      type: stat.isDirectory() ? 'directory' : 'file',
      size: stat.size,
      modified: stat.mtime.toISOString(),
    };
  } catch {
    return { ok: false, path: filePath, error: 'does not exist or is not accessible' };
  }
}

export async function verifyProcessRunning({ name, processId } = {}) {
  return new Promise((resolve) => {
    const args = name
      ? ['-NoLogo', '-NoProfile', '-NonInteractive', '-Command',
         `Get-Process -Name '${name.replace(/'/g, "''")}' -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle | ConvertTo-Json -Compress`]
      : processId
        ? ['-NoLogo', '-NoProfile', '-NonInteractive', '-Command',
           `Get-Process -Id ${Number(processId)} -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle | ConvertTo-Json -Compress`]
        : null;

    if (!args) {
      resolve({ ok: false, error: 'name or processId required' });
      return;
    }

    const child = spawn('powershell.exe', args, { windowsHide: true });
    let stdout = '';
    child.stdout.on('data', (c) => { stdout += c.toString(); });
    child.on('close', () => {
      try {
        const data = stdout.trim() ? JSON.parse(stdout) : null;
        const list = Array.isArray(data) ? data : data ? [data] : [];
        resolve({
          ok: list.length > 0,
          count: list.length,
          processes: list,
        });
      } catch {
        resolve({ ok: false, error: 'failed to query processes', raw: stdout.slice(0, 500) });
      }
    });
  });
}

export async function verifyPortOpen(port, host = '127.0.0.1') {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    const timer = setTimeout(() => {
      socket.destroy();
      resolve({ ok: false, port, host, error: 'timeout' });
    }, 2500);

    socket.once('connect', () => {
      clearTimeout(timer);
      socket.destroy();
      resolve({ ok: true, port, host });
    });
    socket.once('error', (err) => {
      clearTimeout(timer);
      resolve({ ok: false, port, host, error: err.code || err.message });
    });
    socket.connect(Number(port), host);
  });
}

export async function verifyHttpResponse(url, { timeoutMs = 8000, expectStatus } = {}) {
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const res = await fetch(url, { signal: controller.signal, redirect: 'manual' });
    clearTimeout(timer);
    const statusOk = expectStatus ? res.status === expectStatus : res.status >= 200 && res.status < 400;
    return {
      ok: statusOk,
      url,
      status: res.status,
      statusText: res.statusText,
      headers: Object.fromEntries([...res.headers.entries()].slice(0, 20)),
    };
  } catch (err) {
    return { ok: false, url, error: err.message };
  }
}

export async function verifyGitStatus(repoPath) {
  return new Promise((resolve) => {
    const child = spawn('git', ['-C', repoPath, 'status', '--porcelain', '-b'], {
      windowsHide: true,
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (c) => { stdout += c.toString(); });
    child.stderr.on('data', (c) => { stderr += c.toString(); });
    child.on('close', (code) => {
      if (code !== 0) {
        resolve({ ok: false, path: repoPath, error: stderr || 'git status failed' });
        return;
      }
      const lines = stdout.trim().split(/\r?\n/).filter(Boolean);
      const branchLine = lines.find(l => l.startsWith('##')) || '';
      const dirty = lines.filter(l => !l.startsWith('##'));
      resolve({
        ok: true,
        path: repoPath,
        branch: branchLine.replace(/^##\s*/, ''),
        clean: dirty.length === 0,
        dirtyCount: dirty.length,
        dirty: dirty.slice(0, 30),
      });
    });
  });
}

export async function verifyWindowVisible({ title, processId } = {}) {
  return new Promise((resolve) => {
    const filter = title
      ? `$_.MainWindowTitle -like '*${title.replace(/'/g, "''")}*'`
      : processId
        ? `$_.Id -eq ${Number(processId)}`
        : null;
    if (!filter) {
      resolve({ ok: false, error: 'title or processId required' });
      return;
    }
    const script = `Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and (${filter}) } | Select-Object Id,ProcessName,MainWindowTitle | ConvertTo-Json -Compress`;
    const child = spawn('powershell.exe', ['-NoLogo', '-NoProfile', '-NonInteractive', '-Command', script], { windowsHide: true });
    let stdout = '';
    child.stdout.on('data', (c) => { stdout += c.toString(); });
    child.on('close', () => {
      try {
        const data = stdout.trim() ? JSON.parse(stdout) : null;
        const list = Array.isArray(data) ? data : data ? [data] : [];
        resolve({ ok: list.length > 0, count: list.length, windows: list });
      } catch {
        resolve({ ok: false, error: 'query failed', raw: stdout.slice(0, 300) });
      }
    });
  });
}
