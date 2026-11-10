---
name: linkedin-post
description: Write a LinkedIn post in Asshvin's voice from a real build or play run, formatted with LinkedIn bold and checked against the 3,000-character limit. Use for every LinkedIn post, build log or play announcement.
---

# LinkedIn post in Asshvin's voice

Read `brand/VOICE.md` first. It is the source of truth for voice, structure and rules.

## Steps
1. **Collect the facts.** Open the run's `summary.json` / CSV (or the build's real output). List every number you will use and where it came from. Nothing else goes in the post.
2. **Pick the audiences.** Who is this for? (sellers, job seekers, GTM engineers). Line 1 names them with a simple question.
3. **Draft in `**bold**` markdown** following the 12-part structure in VOICE.md section 3. Bold only the hook, the key question and short lead-ins.
4. **Plain-language pass.** Could a 5-year-old follow each line? Cut jargon or explain it right after.
5. **Accuracy pass** (VOICE.md section 5): no invented stories, no overstated wording, time words still true, nothing claimed that didn't happen. Run `agents/skeptic-verifier.md` on the numbers.
6. **Lint:** `python3 scripts/lint_ai_tells.py draft.md` and fix every hit.
7. **Format and count:** `python3 scripts/linkedin_format.py draft.md -o post.txt`. Must say OK (2,800 or less by LinkedIn's count). If not, cut bold first, then words.
8. **Save** next to the play as `post.md` with: the facts and their sources, the paste-ready text, the first comment (link with `?utm_source=linkedin`), the attachment (GIF under 5 MB or MP4), and the plain-text version.
9. **Hand to Asshvin.** Never post or send anything yourself.
