# Playbook — which skills to use for what

Match the user's request to a row, run the chain in order, and pass each step's output to the next.
If nothing fits, invoke `creator-toolkit:index` to pick a skill. If no skill fits at all, do the work directly and add a line under "Missing skills" at the bottom.
Everything that goes out to other people (DMs, emails, posts, CRM writes) stops at a draft. The user sends it.

## Content
| Request | Chain |
|---|---|
| "create content", "content for the week", "what do I post" | `creator-toolkit:topic-engine` (pick topics) → `creator-toolkit:mass-desire-scorer` (keep the best 3) → `creator-toolkit:hook-machine` (hooks) → `creator-toolkit:kallaway` (full scripts), in the user's voice from `creator-toolkit:identity-bank` → 3 ready-to-film scripts |
| "is this idea good", "will this get views" | `creator-toolkit:mass-desire-scorer` |
| "rate/grade my ideas properly" | `creator-toolkit:topic-value-scorer` |
| "break down this video", "steal this" | `creator-toolkit:steal-template` → offer to save it with `creator-toolkit:script-structure-templates` |
| "write hooks", "grade this hook" | `creator-toolkit:hook-machine` |
| "who is my audience", "what do they want" | `creator-toolkit:avatar-research` or `creator-toolkit:audience-bullseye-builder` |
| "here are my numbers", "what's working" | `creator-toolkit:performance-loop` |
| "brand strategy", "how do I grow" | `creator-toolkit:personal-brand-expert` |
| "watch this video/link" | `watch` |
| "what are people saying about X" | `last30days` |

## Agency / clients
| Request | Chain |
|---|---|
| "find me leads", "leads for <niche> in <city>" | `lead-generator` → notes into `lead-tracker` → draft first messages → STOP, the user sends them |
| "who do I follow up with", "who's due" | `lead-tracker` (`tracker.py due`) → draft follow-ups |
| "I messaged/called X", "X replied" | `lead-tracker` log/reply |
| "outreach plan for today" | `lead-tracker` due list + today's targets from goals.md → split into DMs, emails and calls, with drafts ready |
| "audit a client's site/marketing", "proposal", "ad creative" | `creator-toolkit:market` |
| "write copy for a page" | `copywriting` |
| Former employer's CRM tools (`punch-in-leads`, CRM DM sender) | Not the user's own business any more. Ask before using them. |

## Sites / design
| Request | Chain |
|---|---|
| "edit my portfolio", "open the site editor" | `editlocal` |
| "clone this site into Shopify" | `shopify-clone-kit:theme-clone` |
| "make it look better", UI work | `design-pro` |

## Brain itself
| Request | Action |
|---|---|
| "what's today", "what should I do" | Read goals + tasks + sessions.md + `tracker.py due` → top 3 |
| "catch up" | Run `scripts/sessions_digest.py` → update sessions.md and tasks.md |
| "change goal…" | Edit goals.md and its change log |

## Missing skills
(Add a line here when a request had no fitting skill: date — request — suggestion.)
