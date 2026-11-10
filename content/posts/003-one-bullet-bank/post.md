# Post 003: One bullet bank, four resumes

**Status:** caption drafted and linted. Graphic not yet rendered. Substack and Medium versions to follow.
**Slot:** Wednesday teardown.
**Source of every number:** the four `.txt` files in `_source/`, the `content.py` bullet bank,
and `measure.py` output. Nothing here is estimated.

---

## Facts and their sources

| Claim | Value | Source |
|---|---|---|
| Resume versions | 4 | `_source/content.py` → `VERSIONS` |
| Bullets in the shared bank | 28 (23 used across the 4 versions) | `_source/content.py` → `BANK` (counted) |
| Bullets in the largest version | 12 job + 1 build | `VERSIONS["Post-Sale-and-CX-Automation"]` |
| Bullets in the smallest | 8 job + 5 build | `VERSIONS["Founding-GTM-Engineer"]` |
| Words per version | 714 / 689 / 634 / 625 | `wc -w` on the four `.txt` files |
| Page fill, measured in headless Chrome | 100% / 95% / 95% / 96% | `measure.py` |
| Page count of every PDF | 1 | `build.py` → `page_count()` |
| AI-tell lint hits on all four | 0 | `scripts/lint_ai_tells.py` |
| Builds before the rewrite | 3 + 2 links | `content.py` pre-edit |
| Builds after | 5 in the Founding version | `content.py` post-edit |

## What was checked by hand
- Every version was opened as a rendered PDF and read, not just measured.
- The page-fill numbers come from headless Chrome measuring the real document height
  against a Letter page, so "95%" means the last line sits 95% down the page.
- The lint was run against the extracted text of each resume, not the source file.
- I re-read the Founding version after the last rebuild to confirm the numbers landed in
  the right company and no stale figure survived.

## What was NOT done
- No resume was sent to anyone. No recruiter has seen these.
- The four versions were not tested against a live applicant tracking system.
- I did not measure whether recruiters prefer one version over another. That is a claim
  nobody can make without data, so I am not making it.

---

## Caption (paste into LinkedIn)

**Four resumes. One bullet bank. I changed one number and all four rebuilt.**

Building a resume usually means copy-pasting it four times and editing each one. Then you find a typo in one and hunt for the other three.

So I built it the other way.

Every bullet lives once, in a file. Each version is a list of bullet IDs and an order. Then one script renders four PDFs, four Word files, and four text versions, and tells me if any of them spills onto a second page.

28 bullets in the bank, 23 of them used. 4 versions. 714 words at the longest, 625 at the shortest.

**The part that actually broke:** one page. My first build was 2 pages on all four. Not "slightly over". Two full pages.

I did not fix it by making the font smaller. I fixed it by measuring.

Headless Chrome reports the real document height. So I could ask "how full is this page" and get a number back: 105%. Then cut one bullet. 111%. Cut one. 104%. Cut one. 102%.

One version is now at 100%. The other three sit at 95%, 95% and 96%. Every one is exactly one page, with a little air at the bottom.

**What I learned:**
• **Measure the page. Do not eyeball it.** I was wrong about "that fits" twice.
• **One source of truth is not a style choice.** It is how you change a number once instead of four times. My EquityList expansion number changed. One edit, four rebuilds, zero drift.
• **Cutting a bullet is a decision, not a trim.** Every cut made me choose what the version is for. The AI version lost its root-cause bullet. That was the point.
• **A resume is a set of claims. A lint is a floor.** A rule set caught the words. It cannot catch a number that is wrong.

Everything here was checked by a script: page count, page fill, and an AI-writing lint that now returns zero hits on all four.

The interesting part was not the PDFs. It was finding out which bullets each company actually cares about.

Full details and the build script. Link in the comments.

Would you keep four separate resume files, or one source and four builds?

---

## First comment
The bullet bank, the build script and all four PDFs: https://asshvinkumar1999.github.io/gtm-signal-plays/

## Attachment
Animated build log: 23 bullets flowing into 4 versions, each landing on exactly one page.
TODO: render from `_source/content.py`.
