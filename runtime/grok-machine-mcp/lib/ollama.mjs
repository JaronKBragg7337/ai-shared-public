const DEFAULT_OLLAMA_HOST = 'http://127.0.0.1:11434';

function ollamaHost() {
  return (process.env.OLLAMA_HOST || DEFAULT_OLLAMA_HOST).replace(/\/$/, '');
}

async function ollamaFetch(pathname, options = {}) {
  const url = `${ollamaHost()}${pathname}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Ollama ${res.status}: ${text.slice(0, 400) || res.statusText}`);
  }
  return res.json();
}

export async function ollamaModels() {
  const data = await ollamaFetch('/api/tags');
  return {
    host: ollamaHost(),
    models: (data.models || []).map((m) => ({
      name: m.name,
      size: m.size,
      modified: m.modified_at,
      digest: m.digest,
      details: m.details,
    })),
  };
}

export async function ollamaChat({ model, messages, system, temperature, format }) {
  if (!model) throw new Error('model is required');
  const body = {
    model,
    messages: messages || [],
    stream: false,
  };
  if (system) body.messages = [{ role: 'system', content: system }, ...(body.messages || [])];
  if (temperature != null) body.options = { ...(body.options || {}), temperature };
  if (format !== undefined) body.format = format;

  const data = await ollamaFetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify(body),
  });
  return {
    model: data.model,
    message: data.message,
    done: data.done,
    total_duration: data.total_duration,
    load_duration: data.load_duration,
    prompt_eval_count: data.prompt_eval_count,
    eval_count: data.eval_count,
  };
}

export async function ollamaGenerate({ model, prompt, system, temperature, format }) {
  if (!model) throw new Error('model is required');
  if (!prompt) throw new Error('prompt is required');
  const body = { model, prompt, stream: false };
  if (system) body.system = system;
  if (temperature != null) body.options = { temperature };
  if (format !== undefined) body.format = format;

  const data = await ollamaFetch('/api/generate', {
    method: 'POST',
    body: JSON.stringify(body),
  });
  return {
    model: data.model,
    response: data.response,
    done: data.done,
    total_duration: data.total_duration,
    eval_count: data.eval_count,
  };
}

export async function ollamaEmbeddings({ model, prompt }) {
  if (!model) throw new Error('model is required');
  if (!prompt) throw new Error('prompt is required');
  let data;
  try {
    data = await ollamaFetch('/api/embed', {
      method: 'POST',
      body: JSON.stringify({ model, input: prompt }),
    });
  } catch {
    data = await ollamaFetch('/api/embeddings', {
      method: 'POST',
      body: JSON.stringify({ model, prompt }),
    });
  }
  const embedding = Array.isArray(data.embedding)
    ? data.embedding
    : Array.isArray(data.embeddings) ? data.embeddings[0] : null;
  return {
    model,
    embedding,
    dimensions: Array.isArray(embedding) ? embedding.length : null,
  };
}

export async function ollamaPull({ model }) {
  if (!model) throw new Error('model is required');
  const res = await fetch(`${ollamaHost()}/api/pull`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: model, stream: false }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Ollama pull failed: ${res.status} ${text.slice(0, 300)}`);
  }
  const data = await res.json();
  return { model, status: data.status || 'ok', detail: data };
}

export async function ollamaPs() {
  try {
    const data = await ollamaFetch('/api/ps');
    return { host: ollamaHost(), running: data.models || [] };
  } catch (err) {
    return { host: ollamaHost(), running: [], error: err.message };
  }
}

export function getOllamaHost() {
  return ollamaHost();
}
