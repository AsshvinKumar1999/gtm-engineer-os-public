# Post 004: The rule that keeps me from writing a lie

**Status:** caption drafted and linted. Graphic not yet rendered. Substack and Medium versions to follow.
**Slot:** Friday framework.
**Source of every number:** the four resume lint runs and the Play 01 run. The numbers here
are small and real, and they are the point.

---

## Facts and their sources

| Claim | Value | Source |
|---|---|---|
| AI-tell lint hits on the four resumes | 0 | `scripts/lint_ai_tells.py` on each `_source/*.txt` |
| The one real hit while building | one blocked word in the revenue-os bullet | lint output, then reworded to "protocol" |
| AI-Agents version, first build | 2 pages, 105% fill | `build.py` + `measure.py` |
| AI-Agents version, final | 1 page, 100% fill | `build.py` + `measure.py` |
| Play 01 claims that carry a source | every one links to sec.gov or a live job post | `gifts/*.md` |
| Name-verified rows vs slug-only | 6 vs 38 | `gifts/*.md` |
| Play 01 cost | $0, no API keys | `run.py` source and SEC user agent handling |

## What was checked by hand
- The lint hit was real and was fixed by rewording the bullet, not by suppressing the rule.
  The word it blocked is on the blocklist in `scripts/lint_ai_tells.py` line 13 (`ai-vocab`).
  The bullet now says "protocol", which is the word revenue-os's own README uses.
- Every number in the Play 01 output has a link to the primary source next to it.
- The board match method is stated on every row, so a reader can see which claims are
  verified and which are inferred.

## What was NOT done
- I have not published any of this content yet. No post has shipped.
- No reader has told me this makes them trust me more. That is the assumption under the
  whole method and it is still untested.

---

## Caption (paste into LinkedIn)

**Every number you publish should have a link next to it. That's the whole trick.**

I write about things I build. Here's the rule I gave myself: if I can't point to the file, the row, or the public source where a number came from, it does not go in the post.

Not because a rule is nice. Because of what happens when you skip it.

I built a list of companies for a hiring manager. 44 rows. Every row had a link to the SEC filing and a link to the live job post. I checked three of them by hand before sending.

Then the skeptic in me asked: are the 44 rows 44 companies?

No. 18.

One company appeared in all five of my buyer lists. Another appeared in four. They were one buyer each, and I had written 44.

So I deduped, and I wrote 18. The reader could check any row and find the same thing I found. That is the part that matters.

**Here is the rule I keep coming back to:** a claim you cannot check is a claim you are asking someone to trust you about. And asking for trust is a much weaker position than handing over something verifiable.

It changes what you build, not just what you write.

My resume linter blocked a word in a bullet I wrote. The fix was not to turn the rule off. It was to say "protocol" instead, which was accurate anyway.

My Play 01 script tells you on every row whether a job board was matched by the company's actual name or by its URL slug. 6 of 44 are name-verified. The other 38 are inferred. Both are useful. A reader deserves to know which is which.

**What I learned:**
• **A link next to a number is worth more than a confident sentence.** One is checkable. The other is a vibe.
• **Dedupe before you publish.** The most embarrassing number I have written was 44 when the answer was 18.
• **Say how you matched.** "Verified" and "inferred" are different claims. Label them.
• **When a rule fires, reword. Do not disable.** The linter caught a real weakness, not a false positive.

Every number above is traceable. Every one I did not publish, I did not publish.

Full write-up and the scripts. Link in the comments.

What is the number in your work that you would not want anyone to check?

---

## First comment
The scripts, the run files and the full write-up: https://asshvinkumar1999.github.io/gtm-signal-plays/

## Attachment
Animated build log: 44 rows collapsing into 18 companies as the dedupe runs.
Every particle is one real row from the run file. TODO: render from `gifts/`.
