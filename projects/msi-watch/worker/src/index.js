// hb-msi-watch - an alarm that lives OFF the MSI (Cloudflare), built 11/22 after the MSI sat dark for 3 hours with nobody told.
//
// The MSI checks in every 5 minutes (task "MSI Beat" -> tools/msi_beat.py -> POST /beat). That task only runs while the MSI is on
// AND signed in, so silence means: off, frozen, offline, or waiting at the sign-in screen after a restart.
// Every 5 minutes a Cloudflare cron looks at the last check-in. Quiet for QUIET_MIN minutes -> ONE buzz to Jaron's phone (ntfy).
// The first check-in after that -> ONE "back" buzz with how long it was dark. Nothing else, ever (no repeats, no daily noise).
//
// Secrets (Worker secrets, never in this file): BEAT_TOKEN (shared with the MSI, keys.env HB_MSI_BEAT_TOKEN), NTFY_TOPIC.
// Endpoints (all need "Authorization: Bearer <BEAT_TOKEN>"; anything else gets a plain 404):
//   POST /beat     the MSI checking in (optional JSON body: {"boot": "<iso>", "note": "..."})
//   GET  /status   last check-in, minutes quiet, whether an alarm is out (read by the everything check)
//   POST /test     sends one test buzz (used once at setup)

const QUIET_MIN = 20;
const TZ = "America/Indiana/Indianapolis";

function clock(ms) {
  return new Date(ms).toLocaleString("en-US", { timeZone: TZ, weekday: "short", hour: "numeric", minute: "2-digit" });
}

function span(min) {
  const m = Math.round(min);
  if (m < 60) return `${m} min`;
  const h = Math.floor(m / 60), r = m % 60;
  return r ? `${h} h ${r} min` : `${h} h`;
}

let lastBuzzError = null;   // status + ntfy's error text only (ntfy's success body holds the topic, so it is never kept)

async function buzz(env, title, line) {
  if (!env.NTFY_TOPIC) { lastBuzzError = "no NTFY_TOPIC secret"; return false; }
  try {
    const r = await fetch("https://ntfy.sh/" + env.NTFY_TOPIC.trim(), {
      method: "POST",
      body: line,
      headers: { Title: title, Tags: "computer", "User-Agent": "hb-msi-watch/1 (Cloudflare Worker)" },
    });
    if (r.ok) { lastBuzzError = null; return true; }
    let err = "";
    try { err = String((await r.json()).error || ""); } catch (e) { err = "(no json)"; }
    lastBuzzError = `http ${r.status}: ${err.slice(0, 120)}`;
    return false;
  } catch (e) {
    lastBuzzError = "fetch threw: " + String(e).slice(0, 120);
    return false;
  }
}

export class Watch {
  constructor(ctx, env) {
    this.ctx = ctx;
    this.env = env;
  }

  async fetch(req) {
    const url = new URL(req.url);
    const s = this.ctx.storage;
    const now = Date.now();

    if (url.pathname === "/beat" && req.method === "POST") {
      let info = {};
      try { info = await req.json(); } catch (e) { /* empty body is fine */ }
      const alertedAt = await s.get("alerted_at");
      const lastBeat = await s.get("last_beat");
      await s.put("last_beat", now);
      await s.put("last_info", JSON.stringify(info).slice(0, 300));
      if (alertedAt) {
        const darkMin = lastBeat ? (now - lastBeat) / 60000 : 0;
        const sent = await buzz(this.env, "MSI is back",
          `The MSI is back (checked in at ${clock(now)}). It was quiet for ${span(darkMin)}, since ${clock(lastBeat || alertedAt)}. Its own everything check restarts the rest.`);
        await s.delete("alerted_at");
        await s.put("last_outage", JSON.stringify({ from: lastBeat, to: now, minutes: Math.round(darkMin), back_buzz: sent }));
      }
      return Response.json({ ok: true, at: new Date(now).toISOString() });
    }

    if (url.pathname === "/check") {
      const lastBeat = await s.get("last_beat");
      if (!lastBeat) return Response.json({ ok: true, note: "no check-in yet, nothing to judge" });
      const quiet = (now - lastBeat) / 60000;
      const alertedAt = await s.get("alerted_at");
      if (quiet >= QUIET_MIN && !alertedAt) {
        const sent = await buzz(this.env, "MSI went dark",
          `The MSI has been quiet since ${clock(lastBeat)} (${span(quiet)}). It is off, frozen, offline, or waiting at the sign-in screen after a restart. Someone at home: sign in on the MSI (press the power button first if the screen is black).`);
        await s.put("alerted_at", now);
        await s.put("alert_buzz_ok", sent);
        await s.put("alert_buzz_error", lastBuzzError || "");
        return Response.json({ ok: true, alarm: "sent", quiet_min: Math.round(quiet), buzz_ok: sent });
      }
      return Response.json({ ok: true, quiet_min: Math.round(quiet), alarm_out: Boolean(alertedAt) });
    }

    if (url.pathname === "/status") {
      const lastBeat = await s.get("last_beat");
      const alertedAt = await s.get("alerted_at");
      return Response.json({
        ok: true,
        last_beat: lastBeat ? new Date(lastBeat).toISOString() : null,
        last_beat_local: lastBeat ? clock(lastBeat) : null,
        quiet_min: lastBeat ? Math.round((now - lastBeat) / 60000) : null,
        quiet_limit_min: QUIET_MIN,
        alarm_out: Boolean(alertedAt),
        last_info: JSON.parse((await s.get("last_info")) || "{}"),
        last_outage: JSON.parse((await s.get("last_outage")) || "null"),
        last_cron: (await s.get("last_cron")) || null,
        last_alarm_buzz_ok: (await s.get("alert_buzz_ok")) ?? null,
        last_alarm_buzz_error: (await s.get("alert_buzz_error")) || null,
      });
    }

    if (url.pathname === "/test" && req.method === "POST") {
      const sent = await buzz(this.env, "MSI alarm is set up",
        "Test from the new MSI alarm (it lives on Cloudflare, not on the MSI). If the MSI goes quiet for 20 minutes you get one buzz like this, and one more when it's back.");
      return Response.json({ ok: sent, error: lastBuzzError });
    }

    if (url.pathname === "/cron-mark") {
      await s.put("last_cron", new Date(now).toISOString());
      return Response.json({ ok: true });
    }

    return new Response("not found", { status: 404 });
  }
}

function stub(env) {
  return env.WATCH.get(env.WATCH.idFromName("msi"));
}

export default {
  async fetch(req, env) {
    const auth = req.headers.get("authorization") || "";
    if (!env.BEAT_TOKEN || auth !== `Bearer ${env.BEAT_TOKEN}`) return new Response("not found", { status: 404 });
    const url = new URL(req.url);
    if (!["/beat", "/status", "/test"].includes(url.pathname)) return new Response("not found", { status: 404 });
    return stub(env).fetch(req);
  },

  async scheduled(event, env, ctx) {
    const s = stub(env);
    ctx.waitUntil((async () => {
      await s.fetch("https://watch/cron-mark", { method: "POST" });
      await s.fetch("https://watch/check", { method: "POST" });
    })());
  },
};
