#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const BASE_URL = process.env.EVOMAP_BASE_URL || 'https://evomap.ai';
const STATE_PATH = process.env.EVOMAP_STATE_PATH || path.resolve('.openclaw/evomap-state.json');

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function randomHex(n = 8) {
  return crypto.randomBytes(n).toString('hex');
}

function nowIso() {
  return new Date().toISOString();
}

function loadState() {
  if (!fs.existsSync(STATE_PATH)) return {};
  try {
    return JSON.parse(fs.readFileSync(STATE_PATH, 'utf8'));
  } catch {
    return {};
  }
}

function saveState(state) {
  ensureDir(STATE_PATH);
  fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

function ensureSenderId(state) {
  if (!state.sender_id) {
    state.sender_id = `node_${randomHex(8)}`;
    saveState(state);
  }
  return state.sender_id;
}

function envelope(messageType, senderId, payload = {}) {
  return {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: messageType,
    message_id: `msg_${Date.now()}_${randomHex(4)}`,
    sender_id: senderId,
    timestamp: nowIso(),
    payload,
  };
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${JSON.stringify(data)}`);
  }
  return data;
}

async function cmdHello() {
  const state = loadState();
  const senderId = ensureSenderId(state);
  const body = envelope('hello', senderId, {
    capabilities: {},
    gene_count: 0,
    capsule_count: 0,
    env_fingerprint: {
      platform: process.platform,
      arch: process.arch,
      evolver_version: 'custom-openclaw-1.0.0',
    },
  });

  const data = await postJson(`${BASE_URL}/a2a/hello`, body);
  state.sender_id = senderId;
  state.last_hello = nowIso();
  state.claim_url = data?.payload?.claim_url || data?.claim_url || state.claim_url;
  state.claim_code = data?.payload?.claim_code || data?.claim_code || state.claim_code;
  state.heartbeat_interval_ms = data?.payload?.heartbeat_interval_ms || data?.heartbeat_interval_ms || state.heartbeat_interval_ms || 900000;
  saveState(state);

  console.log(JSON.stringify({ ok: true, sender_id: senderId, response: data, state_path: STATE_PATH }, null, 2));
}

async function cmdHeartbeat() {
  const state = loadState();
  const senderId = ensureSenderId(state);
  const data = await postJson(`${BASE_URL}/a2a/heartbeat`, {
    node_id: senderId,
  });

  state.last_heartbeat = nowIso();
  state.heartbeat_interval_ms = data?.next_heartbeat_ms || state.heartbeat_interval_ms || 900000;
  saveState(state);

  console.log(JSON.stringify({ ok: true, sender_id: senderId, response: data }, null, 2));
}

async function cmdFetch() {
  const state = loadState();
  const senderId = ensureSenderId(state);
  const body = envelope('fetch', senderId, {
    asset_type: 'Capsule',
    include_tasks: true,
  });
  const data = await postJson(`${BASE_URL}/a2a/fetch`, body);
  console.log(JSON.stringify({ ok: true, sender_id: senderId, response: data }, null, 2));
}

async function sleep(ms) {
  await new Promise((r) => setTimeout(r, ms));
}

async function cmdLoop() {
  await cmdHello();
  while (true) {
    try {
      await cmdHeartbeat();
    } catch (err) {
      console.error(`[heartbeat] ${err.message}`);
    }
    const state = loadState();
    const interval = Number(state.heartbeat_interval_ms || 900000);
    const waitMs = Number.isFinite(interval) && interval > 0 ? interval : 900000;
    console.error(`[loop] next heartbeat in ${Math.round(waitMs / 1000)}s`);
    await sleep(waitMs);
  }
}

const cmd = process.argv[2];

try {
  if (cmd === 'hello') await cmdHello();
  else if (cmd === 'heartbeat') await cmdHeartbeat();
  else if (cmd === 'fetch') await cmdFetch();
  else if (cmd === 'loop') await cmdLoop();
  else {
    console.log('Usage: node apps/evomap/evomap-client.mjs <hello|heartbeat|fetch|loop>');
    process.exit(1);
  }
} catch (err) {
  console.error(err.message || err);
  process.exit(1);
}
