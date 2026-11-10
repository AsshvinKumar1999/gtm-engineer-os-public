# GTM Engineer OS — operating rules for agents

This repo is a GTM engineering playbook built on free public data (see `METHOD.md`). Skills live in `skills/`, reviewer agents in `agents/`, deterministic tools in `scripts/`.

## Before any GTM task
1. Read `METHOD.md`.
2. Pick the matching skill in `skills/` and follow it completely.
3. Ask: who was compelled to publish this? What can code or free data answer before a model or paid tool?

## Working rules
- Start from the buyer's situation, never a firmographic filter.
- Code computes numbers; models only judge; `agents/skeptic-verifier.md` verifies; the human approves.
- Never fabricate a scenario, quote, number or source. Every quote must be an exact substring of its source.
- Run `python scripts/cost_guard.py` before any paid batch. Default to the cheapest adequate model.
- Messages go through `agents/buyer-critic.md` and `python scripts/lint_ai_tells.py` before a human sees them.
- Plans for the human use Plain Plan Mode (📦 💵 ⚠ ❓ 👉), with reconciled numbers.
- Client data never goes in this repo; use a separate private repo.
- No browser automation that bypasses bot protection or logs into the user's accounts; use official APIs.
