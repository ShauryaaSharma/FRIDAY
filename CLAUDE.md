# friday-ai-agent-harness — working conventions

**Friday** — a local-first personal assistant demonstrating the four pillars behind every
serious agent: Harness, Loop, Memory, and Eval/LLM-Ops. It began as a teaching repo you
could read in an afternoon, and it's now growing toward a full open-source assistant (the
next Hermes / OpenClaw). The bar for every change: **clear, honest code a newcomer can
follow** — each pillar legible on its own. The project will get bigger; it must never get
muddier. New scope is welcome when it stays self-contained, tested, and readable; complexity
for its own sake is not.

## Architecture map (file ↔ diagram box)

- `friday/gateway/` — cli, voice (wake word), telegram. Gateways only move text.
- `friday/runtime/session.py` — working memory assembly (SOUL.md + memory + history)
- `friday/loop/agent.py` — THE loop; `loop/models.py` — pluggable providers, 2 wire formats
- `friday/graph/` — engine + node factories + `workflows/` (triage) — opt-in structure
  AROUND the loop (the loop never changes; a graph node can BE a loop turn); every
  failure fails open to the plain loop
- `friday/tools/` — create_event / save_note / send_message (flagship task only)
- `friday/memory/` — semantic (FTS5) / episodic / procedural (SKILL.md) +
  `retrieval_gate.py` (hero 1) + `consolidation.py` (every N exchanges)
- `friday/ops/` — tracing (JSONL + OTel), dashboard (localhost:7777), release_gate,
  `compare_history.py` (the Compare arena's own JSONL scoreboard — never state.db)
- `evals/deterministic/` (0/1, pytest) vs `evals/judge/` (DeepEval, scored) — never mix
- Runtime state lives in `.friday/` (state.db, calendar.ics, outbox/, traces/) — gitignored

## Rules

- **Be concise.** Shaurya wants short replies: lead with the answer, cut preamble and
  recap. A few lines beats a wall of text. Expand only when they ask for detail.
- **Never wipe runtime data without asking first, every time.** `scripts/demo_seed.py`
  and anything else that clears `.friday` (memory, calendar, chat log, traces, or the
  `usage.jsonl` spend ledger) must be proposed and explicitly approved by the user
  *immediately before each run*. Permission never carries over from a previous run.
  The script backs up first, but restoring is a hassle — ask, wait for a clear yes,
  then run. It refuses to do anything without the `--yes` flag for this reason.
- **Commit messages are about the CODE, not the conversation.** Subject = what
  changed, under ~70 chars. Body = why, in a few tight lines. Then stop.
  No narrating who asked for it, no "Shaurya caught", no story of what I tried
  first, no re-deriving the reasoning. This is a public repo — a stranger
  reading `git log` wants the change, not a diary. If the reasoning is worth
  keeping, it belongs in a code comment next to the code it explains.
- **Version control — commit AND ship every milestone, same turn.** The moment a change
  works (tests pass / verified live), commit it and get it onto GitHub before moving on. Never end a
  turn or session with working changes left uncommitted — the repo must always be traceable
  from GitHub, and uncommitted work has been lost to branch switches before. Use the `/ship`
  skill. If several milestones land in one session, commit each as its own logical commit.
- **`main` is protected — `git push origin main` is REJECTED, for everyone.** A commit
  lands only once BOTH required checks are green — `skills-and-evals (ubuntu-latest)`
  and `skills-and-evals (windows-latest)` — and `enforce_admins` is on, so the rule
  binds Shaurya and Claude identically. Ship via
  `git checkout -b <topic>` → `gh pr create --fill` → `gh pr checks --watch` (~2m,
  windows is the slow one) → `gh pr merge --squash --delete-branch`.
  `GH006: Protected branch update failed` is the guard working; never route around it.
  Two required checks, not one, because both bugs that reached main in 2026-08 were
  Windows-only and an ubuntu-only CI called them green. If the matrix in
  `.github/workflows/validate-skills.yml` ever changes, the check NAMES change with it
  and protection must be updated to match, or nothing is required at all.
  Verify with `gh api repos/ShauryaaSharma/FRIDAY/branches/main/protection` — this rule
  was silently absent for a stretch before 2026-08-22 while this file still claimed it.
- **Gate before push**: `make gate` (deterministic must pass; judge runs with a key).
  When a live bug is found, fix it AND add a regression case to `evals/deterministic/`.
- **No emojis** in any UI surface (dashboard, CLI output, README prose).
- **No new dependencies without discussion** — the core is stdlib + anthropic/openai.
  Optional features go behind extras (`[voice]`, `[telegram]`, ...).
- **Footprint ladder — where new capability goes.** Every registered tool ships in
  every prompt, so the core stays narrow and capability lives at the edges. In order:
  extend existing code → a skill (`SKILL.md`, no Python) → a CLI + README →
  a tool behind an extra → a gateway (one file, text in/out only) →
  **a new core tool, last resort**.
- **Scope**: scheduling is the flagship teaching task, but the project is growing toward a
  full assistant. New capabilities (providers, tools, gateways, integrations) are welcome
  when they're self-contained, tested, and keep the core legible. Reject only complexity
  that muddies how the system works or bloats the default path — prefer opt-in extras.
- Providers are framed neutrally in docs (Anthropic, OpenAI, Gemini, DeepSeek, Kimi, GLM,
  OpenRouter) — no ranking, no "open-source vs closed" framing.

## Commands

`make run` · `make voice` · `make dashboard` (7777) · `make trace` (6006) ·
`make eval` · `make gate` · `make lint` · tests live under `evals/`, not `tests/`
