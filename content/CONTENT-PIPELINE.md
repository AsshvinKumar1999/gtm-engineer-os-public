# Content pipeline: 3 posts a week, 3 platforms, one story each

Written 2026-11-09. Operates the plan in `brand/FIRST-3-POSTS.md` and the voice in
`brand/VOICE.md`. The method is the reverse-engineered operating model; everything here
is a means of shipping, not a replacement for the work.

---

## 1. The one rule that makes this work

**Never invent the scenario.** Every number in a post comes from a run file, a repo or a
public source you can open. If it did not happen, it is not in the post.

This is the single most expensive thing to get wrong. A post that invents its example
proves you are a writer. A post that writes what happened proves you are a practitioner.
Every other rule below is downstream of this one.

Sources you can draw on without inventing anything:

| Source | What it gives you | Where |
|---|---|---|
| Play runs | Counts, chains, before/after, surprises | `plays/*/out/*/summary.json`, `accounts.csv`, `jobs.csv` |
| Gift sheets | Buyer lists per company, matched roles | `plays/01-fresh-capital-open-role/out/*/gifts/*.md` |
| The repos | What you built and how big it is | `gtm-engineer-os/`, `revenue-os` (public) |
| Your own job | Real systems, real numbers, real breakages | Nextiva, Carta, EquityList |
| Public records | Dated, free, hard to fake | SEC EDGAR, Dept. of Labor, city open data |

When you have no fresh run, write a **teardown** (post 2 slot) or a **framework** (post 3
slot). Those slots do not need a new dataset. The build-log slot does.

---

## 2. The cadence

Three posts a week. One story each. The story leads; the platform versions follow it.

| Slot | Day | Type | Needs | Length |
|---|---|---|---|---|
| 1 | Monday | **Build log** | A real run with a real number | 900–2,200 chars on LinkedIn |
| 2 | Wednesday | **Teardown** | Something you built or learned that already happened | 900–2,200 chars on LinkedIn |
| 3 | Friday | **Framework** | A named principle you can teach | 900–2,200 chars on LinkedIn |

Each slot produces **one source story** and **three platform versions**:

- **LinkedIn** — the hook, the story, the receipt. Link in the first comment.
- **Substack** — the same story at length, with the reasoning and the method.
- **Medium** — the same story rewritten for a technical reader, canonical URL and tags.

Same facts, three shapes. Never three copies of the same text.

---

## 3. Platform rules

### LinkedIn
- Bold uses Unicode letters. Write `**bold**`, then run `python3 scripts/linkedin_format.py draft.md`.
- Keep it under **2,800** by LinkedIn's count. The formatter prints the count and fails above 3,000.
- Bold only the hook, the key question and short lead-ins. Never a whole paragraph.
- No links in the body. Link goes in the first comment with `?utm_source=linkedin` so analytics count it.
- Attach the animated graphic (GIF under 5 MB at 810 px, or the MP4).
- 12-part structure from `brand/VOICE.md` section 3.
- First 33 characters must stand alone on mobile.

### Substack
- The deep version. Lead with the tension, not the conclusion.
- One thesis per issue. The title states the specific number and the outcome.
- Include the receipt: the run file, the source, the date.
- Name the honest limits. Say what the post does not prove.
- Close with one question that a reader can answer in a sentence.

### Medium
- Technical readers. Lead with the mechanism, then the result.
- Canonical link to your original when the story ran elsewhere.
- 3–5 relevant tags. Subtitle is one sentence, not a tagline.
- Code blocks are welcome when the code is the point.
- No engagement bait. No "comment below and I'll send you the template."

---

## 4. The quality gate

Nothing ships until all six pass. Run them, don't eyeball them.

```bash
# 1. AI-tell lint (blocking)
python3 scripts/lint_ai_tells.py <draft>

# 2. LinkedIn length, counted the way LinkedIn counts
python3 scripts/linkedin_format.py <draft>

# 3. Every number traces to a run file or a public source
python3 scripts/check_claims.py <draft>

# 4. Skeptic pass: agents/skeptic-verifier.md on the data block

# 5. Human approval: YOU publish. Claude drafts, renders and checks.

# 6. Analytics on Friday: impressions, saves, profile views, inbound DMs
```

Rule from the editorial gate: **one auto-retry with the hit list, then halt and show the
human.** Never silently bypass a lint hit.

### About `check_claims.py`

It cannot tell whether a number is true. It tells you whether a number is **traceable**:
every figure in the draft must appear in a source file, or be a documented rounding of a
source value, or be on the structural allowlist. Untraceable means unproven, not wrong.

When a number is legitimately new (a word count, a page-fill reading), it does not go in
the `--allow` list. It goes into a real source file:

| New number | Where it goes |
|---|---|
| Gift-sheet totals across sheets | `plays/01-fresh-capital-open-role/out/<run>/aggregate.json` |
| Resume word counts, page fill, page count | `_source/build-metrics.json` (run `python3 _source/build-metrics.py`) |
| Page-fill history while trimming | `build-metrics.json` → `trim_history` |

That is the point. A number that only exists in a chat message is a number nobody can
check, including you.

---

## 5. Automation

A scheduled task runs every Monday at 8:00 AM America/Phoenix and prepares the coming
week's three slots: one folder per slot under `content/posts/`, each with `post.md`
(facts table + LinkedIn caption + first comment), `substack.md` and `medium.md`.

**It drafts. It never publishes.** Every gate above is enforced before it reports, and
you publish everything yourself.

To change the cadence, the slots or the gates, update the scheduled task rather than
the task prompt's assumptions, and keep this file as the source of truth.

---

## 6. The content source of truth

| I need | Look in |
|---|---|
| Voice, structure, words to avoid | `brand/VOICE.md` |
| My own posting style, the model post | `brand/VOICE.md` section 8 |
| Which posts to write next | `brand/FIRST-3-POSTS.md` section 3 |
| The method behind the framework | `brand/FIRST-3-POSTS.md` and `skills/` |
| A reusable method for a new lane | `skills/` (12 skills, each with a `SKILL.md`) |
| A skeptical check on numbers | `agents/skeptic-verifier.md` |
| Real data to write about | `plays/*/out/` |

`revenue-os` (public, MIT, 758 skills) already carries platform-specific skills for
LinkedIn, newsletters, articles and crossposting. Read them before writing a new one.

---

## 6. What each platform is for

**LinkedIn is where the recruiter sees you.** Short, one number, one image, the proof
that you ship. This is where the job applications convert.

**Substack is where you are trusted.** One long piece a week, deep enough that a
reader forwards it to a peer. This is where the audience grows.

**Medium is where the engineers are.** The same story, told as a mechanism. This is
where the peer network and the inbound DMs come from.

One build, three audiences. Never three versions of the same post.

---

## 7. Where the proof lives

| Asset | Visibility | Status |
|---|---|---|
| `gtm-signal-plays` (Play 01) | **public** | Runs clean from a fresh clone. Verified 2026-11-09: 844 filings → 293 companies → 84 tech → 449 roles → 4 Tier 1, matching the published post exactly. **No LICENSE file yet**, so add MIT before claiming "open source" in a post. |
| `revenue-os` | **public, MIT** | 758 skills, 396 agents, 283 commands. LICENSE present. |
| `gtm-engineer-os-public` (this repo) | **public** | Holds the 11 skills, the plays, the voice files, the scripts, the content pipeline. No LICENSE file, so do not call it open source. |
| `plays/06-fresh-capital-visa-sponsor` | **private** | Real and verified (392K H-1B filings, 23 of 24 matched on EIN) but not published. Publish it to `gtm-signal-plays` if you want a second public artifact. |
| `content/plays/01-permits-queues` | draft | A caption and graphic exist. **No runnable script and no real data pull yet**, so it cannot be a build-log post. It needs one real pull before it can carry a number. |

### The rule about public vs private

Say "open source" only where there is a LICENSE. Say "built" for anything private. The
resume follows this rule and so must every post.
