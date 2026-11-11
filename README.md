# GTM Engineer OS

My working GTM engineering system: Claude Code skills, reviewer agents, scripts and plays built on free public data. By [Asshvin Kumar](https://asshvinkumar1999.github.io/gtm-signal-plays/).

**Start with [`METHOD.md`](METHOD.md)**, the whole approach on one page.

| Path | What it is |
|---|---|
| `METHOD.md` | The method: situations not filters, compelled records, two signals, code counts and humans approve. |
| `skills/` | 14 Claude Code skills: asymmetry-engine, pain-segment-finder, pvp-writer, dossier-builder, win-loss-rewind, cheap-right-answers, evidence-pack-judge, editorial-gate, data-source-hunter, non-us-data-map, lever-test, monetization-ladder, animated-infographic, linkedin-post. |
| `agents/` | Reviewer agents: skeptic-verifier, buyer-critic, blind-planner. |
| `plays/` | Runnable plays. `01-fresh-capital-open-role` (SEC Form D × job boards) and `06-fresh-capital-visa-sponsor` (Form D × DOL H-1B data × job boards). Standard-library Python, no API keys. |
| `scripts/` | `lint_ai_tells.py` (writing lint), `cost_guard.py` (spend tiers + ledger), `check_claims.py` (checks numbers in a draft against run files), `lever_test.py` (Wilson intervals, the 2×SE lever test, the tie band), `verify_sources.py` (data-source lineage gate before you spend), `linkedin_format.py` (LinkedIn bold + length check), `render_animation.py` (HTML → MP4/GIF). |
| `brand/VOICE.md` | My writing style for posts and pages, with a reference post. |
| `content/` | LinkedIn posts and animated graphics, one folder each. |

## Use the skills in Claude Code
```bash
ln -s "$PWD/skills/"* ~/.claude/skills/
ln -s "$PWD/agents/"*.md ~/.claude/agents/
```

## Run a play
SEC asks every client to include a contact, so put your own name and email in `SEC_USER_AGENT`:
```bash
SEC_USER_AGENT="Your Name you@example.com" python3 plays/01-fresh-capital-open-role/run.py --days 7
```
Run outputs go to `plays/*/out/` and aren't committed.

## Tests
```bash
uv run --with pytest python -m pytest -q tests
```

## Live plays
https://asshvinkumar1999.github.io/gtm-signal-plays/

## Credit
Jordan Crawford's writing on public-data GTM got me started. His free starter: https://github.com/SantaJordan/gtm-engineer-starter

MIT licensed. See `LICENSE`.
