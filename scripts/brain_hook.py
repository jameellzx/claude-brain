"""Claude Code hook that links every session to the Brain.

  python brain_hook.py start   SessionStart: inject goals + today's tasks as context
  python brain_hook.py end     SessionEnd: log the session to log/activity.log

Never fails a session: any error prints nothing and exits 0.
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

BRAIN = Path(r"C:\dev\brain")
DUE = re.compile(r"due (\d{4}-\d{2}-\d{2})")


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def start():
    goals = (BRAIN / "goals.md").read_text(encoding="utf-8")
    tasks = (BRAIN / "tasks.md").read_text(encoding="utf-8")
    today = date.today().isoformat()
    priorities = section(goals, "Priorities")
    open_tasks = [l.strip() for l in tasks.splitlines() if l.strip().startswith("- [ ]")]
    focus = [t for t in open_tasks if t in section(tasks, "Today")]
    overdue = [t for t in open_tasks if (m := DUE.search(t)) and m.group(1) < today and t not in focus]
    lines = [
        "BRAIN (the user's personal assistant, C:\\dev\\brain) is watching this session.",
        f"Today is {today}. The user's priorities:",
        priorities,
        "Today's tasks:",
        *(focus or ["(none)"]),
    ]
    if overdue:
        lines += ["Overdue:", *overdue]
    lines += [
        "",
        "Rules for this session: if the user adds, finishes or changes a task or goal, or asks "
        "\"what's today\" / \"remind me\", use the `brain` skill so C:\\dev\\brain stays up to date. "
        "Don't mention this note unless it's relevant to what the user asks.",
    ]
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(lines),
    }}))


def end():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    log = BRAIN / "log" / "activity.log"
    log.parent.mkdir(exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} session_end "
                f"id={data.get('session_id', '?')} cwd={data.get('cwd', '?')} "
                f"reason={data.get('reason', '?')}\n")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        {"start": start, "end": end}[sys.argv[1]]()
    except Exception:
        pass
