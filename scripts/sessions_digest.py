"""Digest Claude sessions changed since the last brain sync.

Usage:
  python sessions_digest.py            # sessions changed since last sync, then mark synced
  python sessions_digest.py --since 2  # sessions changed in the last 2 days (does not mark synced)
  python sessions_digest.py --peek     # like default but does not mark synced

Prints a compact text digest (title, dates, first ask, recent turns) for Claude to
summarize into C:\\dev\\brain\\sessions.md. Tool calls and tool output are skipped.
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SESSIONS_DIR = Path.home() / ".claude" / "projects" / "C--dev"
STATE = Path(r"C:\dev\brain\state.json")
RUN_MARKER = "BRAIN-RUN"  # brain's own scheduled runs put this in their prompt; skip them
TURNS = 16
CLIP = 400


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text")
    return ""


def clip(s):
    s = " ".join(s.split())
    return s if len(s) <= CLIP else s[:CLIP] + " …"


def digest(path):
    title, first_ask, turns, first_ts, last_ts, cwd = None, None, [], None, None, None
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = d.get("type")
            if t == "custom-title":
                title = d.get("customTitle") or title
                continue
            if t not in ("user", "assistant") or d.get("isSidechain"):
                continue
            ts = d.get("timestamp")
            if ts:
                first_ts = first_ts or ts
                last_ts = ts
            cwd = d.get("cwd") or cwd
            txt = text_of((d.get("message") or {}).get("content")).strip()
            if not txt or txt.startswith("<"):
                continue
            if t == "user" and first_ask is None:
                first_ask = txt
            turns.append(("USER" if t == "user" else "CLAUDE", clip(txt)))
    if first_ask and RUN_MARKER in first_ask:
        return None
    if not turns:
        return None
    out = [
        f"### {title or '(untitled)'}",
        f"id: {path.stem} | cwd: {cwd} | {(first_ts or '')[:16]} → {(last_ts or '')[:16]} UTC",
        f"first ask: {clip(first_ask or '')}",
        "recent turns:",
    ]
    out += [f"  {who}: {txt}" for who, txt in turns[-TURNS:]]
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    state = load_state()
    now = datetime.now(timezone.utc)
    mark = True
    if "--since" in args:
        days = float(args[args.index("--since") + 1])
        cutoff = now - timedelta(days=days)
        mark = False
    elif state.get("last_sync"):
        cutoff = datetime.fromisoformat(state["last_sync"])
    else:
        cutoff = now - timedelta(days=3)
    if "--peek" in args:
        mark = False

    files = sorted(
        (p for p in SESSIONS_DIR.glob("*.jsonl")
         if datetime.fromtimestamp(p.stat().st_mtime, timezone.utc) > cutoff),
        key=lambda p: p.stat().st_mtime,
    )
    blocks = [b for b in (digest(p) for p in files) if b]
    print(f"# Sessions changed since {cutoff.isoformat()[:16]} UTC: {len(blocks)}\n")
    print("\n\n".join(blocks) if blocks else "(none)")
    if mark:
        state["last_sync"] = now.isoformat()
        save_state(state)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
