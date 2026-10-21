import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import * as os from 'node:os';

const REGISTRY_PATH = process.env.MCP_REGISTRY_PATH
  || path.join(process.env.LOCALAPPDATA || os.homedir(), 'GrokMachineMcp', 'registry.json');

function registryPath() {
  return process.env.MCP_REGISTRY_PATH || REGISTRY_PATH;
}

const DEFAULT_REGISTRY = {
  version: 1,
  updatedAt: null,
  projects: {
    'grok-machine-mcp': {
      name: 'Grok Machine MCP',
      path: 'G:\\My Drive\\Codex Active\\projects\\grok-machine-mcp',
      type: 'mcp-server',
      notes: 'Primary capability bus for Grok',
    },
    'SYL-Full-Game': {
      name: 'SYL Full Game',
      path: 'G:\\My Drive\\Codex Active\\projects\\SYL-Full-Game',
      type: 'game',
    },
    'heartbeat-observatory': {
      name: 'Heartbeat Observatory',
      path: 'G:\\My Drive\\Codex Active\\projects\\heartbeat-observatory',
      type: 'observatory',
    },
  },
  knownPorts: {
    '3001': 'grok-machine-mcp',
    '11434': 'ollama',
  },
  launchCommands: {},
  ollamaModels: ['llama3.2:3b', 'qwen3.5:4b'],
};

async function loadRegistry() {
  try {
    const raw = await fs.readFile(registryPath(), 'utf8');
    return { ...DEFAULT_REGISTRY, ...JSON.parse(raw) };
  } catch {
    return { ...DEFAULT_REGISTRY };
  }
}

async function saveRegistry(reg) {
  await fs.mkdir(path.dirname(registryPath()), { recursive: true });
  reg.updatedAt = new Date().toISOString();
  await fs.writeFile(registryPath(), JSON.stringify(reg, null, 2), 'utf8');
  return reg;
}

export async function registryList() {
  const reg = await loadRegistry();
  return {
    projects: Object.entries(reg.projects || {}).map(([id, p]) => ({ id, ...p })),
    knownPorts: reg.knownPorts || {},
    ollamaModels: reg.ollamaModels || [],
    updatedAt: reg.updatedAt,
  };
}

export async function registryGet(id) {
  const reg = await loadRegistry();
  const project = reg.projects?.[id];
  if (!project) throw new Error(`Project not found in registry: ${id}`);
  return { id, ...project };
}

export async function registryUpsert(id, data) {
  const reg = await loadRegistry();
  reg.projects = reg.projects || {};
  reg.projects[id] = { ...(reg.projects[id] || {}), ...data };
  await saveRegistry(reg);
  return { id, ...reg.projects[id] };
}

export { REGISTRY_PATH, loadRegistry, saveRegistry, registryPath };
