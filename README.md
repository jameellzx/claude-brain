# Brain: a personal assistant for Claude Code

A personal assistant that runs on a **Claude subscription**, so there are no API keys and no extra cost. It knows your goals, keeps one task list, remembers what you worked on in every Claude session, picks the right skills for each request, briefs you every morning, and you can talk to it from your phone on **Telegram**.

It's plain files plus Claude Code features: skills, scheduled tasks, memory and the official Telegram channel plugin. There's no server or database, and no framework.

## What it does

| Feature | How |
|---|---|
| Knows your goals | `goals.md`: ranked priorities, daily targets and a change log. Edit it by chatting ("push content back a week"). |
| One task inbox | `tasks.md`: "remind me…", "I need to…", "done with…" all land here. |
| Sees all your Claude sessions | `scripts/sessions_digest.py` reads your session transcripts and summarizes them into `sessions.md`: what you worked on, status and next step. |
| Picks the right skill | `playbook.md` maps requests to skill chains. For example, "create content" runs topics, then scoring, then hooks, then scripts. |
| Safe by default | `RULES.md`: it does research, drafts and organizing on its own, and asks first before sending, posting, spending or deleting. |
| Morning brief and evening check-in | Two scheduled tasks (`scheduled/`) that pick today's top 3, do the prep work and send a notification to your phone. |
| Telegram | The official `telegram@claude-plugins-official` channel plugin. Message your own bot, and the brain answers using your skills and files. |

## Setup (Windows)

1. **Copy this folder** to `C:\dev\brain`. The scripts use that path.
2. **Create your personal files** from the templates. These are git-ignored and stay on your PC:
   ```bash
   cp templates/goals.md goals.md
   cp templates/tasks.md tasks.md
   cp templates/sessions.md sessions.md
   ```
3. **Install the skill:** copy `skill/brain/` to `%USERPROFILE%\.claude\skills\brain\`.
4. **Fill in your goals.** Ask Claude "brain, interview me for my goals", or edit `goals.md` by hand.
5. **Scheduled runs:** in the Claude desktop app, create two scheduled tasks using the prompts in `scheduled/brain-morning.md` (daily, for example 8:45) and `scheduled/brain-evening.md` (daily, for example 22:00). On the first run, click "Always allow" on its permission prompts.
6. **Telegram (optional):**
   1. Install [Bun](https://bun.sh): `winget install Oven-sh.Bun`
   2. Install the plugin: `claude plugin install telegram@claude-plugins-official`
   3. Create a bot with [@BotFather](https://t.me/BotFather) (`/newbot`) and copy the token.
   4. Double-click **Save Telegram Token.bat**. It reads the token from your clipboard, saves it and clears the clipboard.
   5. If the terminal Claude isn't logged in, double-click **Log in Claude (terminal).bat**.
   6. Double-click **Start Brain (Telegram).bat**, then DM your bot. It replies with a pairing code. Pair with `/telegram:access pair <code>`, then run `/telegram:access policy allowlist`.

## Launcher gotchas (already handled in the .bat files)

- **Stale login from other sessions:** the launcher clears inherited `CLAUDE*` environment variables. Otherwise a window opened from another Claude session can fail with `401 OAuth access token has expired`.
- **Prompt placement:** the startup prompt goes *before* `--channels`, because that flag takes a variable number of values and swallows anything after it.
- **One window only:** run a single launcher. Two pollers on one bot token conflict.
- **Bun on PATH:** Bun's winget folder is added to PATH, because Explorer may not see the new PATH until you log out and back in.

## Files

```
CLAUDE.md                     makes any Claude session in this folder act as the brain
RULES.md                      what it may do alone vs. ask first
playbook.md                   request → skill chain map
skill/brain/SKILL.md          the brain skill
scheduled/                    morning + evening scheduled-task prompts
scripts/sessions_digest.py    session transcript digest
scripts/save_token.ps1        clipboard → Telegram token file
templates/                    blank goals / tasks / sessions files
*.bat                         double-click launchers
```

Your real `goals.md`, `tasks.md`, `sessions.md`, `log/` and `outputs/` are git-ignored and never published.
