# Asshvin's writing style

Use this for every LinkedIn post, website page and play write-up. The skill `skills/linkedin-post` follows it step by step.

## 1. Who we write for
- GTM people (sellers, GTM engineers, RevOps) and job seekers in tech.
- Explain it like you would to a 5-year-old: short words, one idea per line, no jargon without a plain explanation right after.

## 2. Voice
- Personal and honest. First person ("I built", "I ran", "I checked").
- Warm, curious, a little humble. Never salesy, never hype.
- Short paragraphs: one or two lines each. White space is part of the style.
- Story first, numbers inside the story. Never a dashboard of stats on its own.
- Thank real people by name when they helped (tag them with @ on LinkedIn).
- Close warmly with an offer to help and one simple question.

## 3. Post structure (LinkedIn)
1. **Hook, line 1 (bold).** Name who it's for and what they get. A simple question works best.
   Example: "Looking for a job at a company that just raised money? Or for buyers who just got a budget?"
2. **Line 2: the promise.** "Here's a free Claude Code workflow for both. You just copy and paste one prompt."
3. **The plain idea** in 2 to 4 short lines (what the public data is, why nobody uses it).
4. **What I built** and the one question it asks (bold the question).
5. **Why it works** in 3 short lines (signal A tells you X, signal B tells you Y, both = a reason).
6. **What happened when I ran it**: one arrow chain with real counts (A → B → C → result). Say you checked by hand.
7. **The surprise** (bold lead-in) with the one finding people will repeat.
8. **What I learned**: 3 or 4 bullets, each a bold lead-in plus one plain sentence.
9. **Second audience** if there is one (bold lead-in like "Job hunting?"), with the 3 questions the prompt asks.
10. **Thanks** to the person who inspired it.
11. **Where to get it**: "Link in the comments."
12. **Closing question** that invites a one-word answer.

**First comment:** the link, with `?utm_source=linkedin` on the end so analytics can count LinkedIn visits.
**Attach:** the play's animated graphic. A GIF under 5 MB (810 px wide, 12 fps) or the MP4.

## 4. Formatting rules
- **Bold uses Unicode letters** (𝗹𝗶𝗸𝗲 𝘁𝗵𝗶𝘀). Write `**bold**` in drafts and run `python3 scripts/linkedin_format.py draft.md`.
- **LinkedIn counts each bold letter as 2 characters.** The limit is 3,000. Keep posts under **2,800** by LinkedIn's count. The formatter prints the count and fails above 3,000.
- Bold only: the hook, the key question, and short lead-ins (3 to 6 words). Never whole paragraphs or whole bullets.
- Arrows (→) for chains and journeys. Bullets (•) for lessons. Numbered lists for steps or questions.
- No links in the post body (LinkedIn shows them less). Link goes in the first comment.
- No hashtag walls. One or two at most, or none.

## 5. Accuracy rules (never break these)
- Every number comes from a real run file (`summary.json`, CSV) or a source you can open. Write the source in the post's `.md` notes.
- Never invent a story, a person, a quote or a result. If it didn't happen, it isn't in the post.
- Say what you checked by hand, and say what you did NOT do (no meetings claimed unless they happened).
- Count companies once (dedupe repeat filers). Watch for wording that overstates: "844 filings", not "844 companies raised money" when funds are included.
- Data claims ("free", "no API key") must be backed by the provider's own docs.
- Time words go stale: "last week" is only true for 7 days after the window. Change to "in one week" after that.

## 6. Words to avoid
Run `python3 scripts/lint_ai_tells.py` on every draft. Avoid: "game-changer", "unlock", "leverage", "delve", "in today's fast-paced world", "it's not X, it's Y", "here's the thing", empty openers, and em-dash chains.

## 7. Reference example (Play 01, final, 2,227 by LinkedIn's count)
Source: `content/plays/02-fresh-capital-open-role/post.md`

```
**Looking for a job at a company that just raised money? Or for buyers who just got a budget?**

Here's a free Claude Code workflow for both. You just copy and paste one prompt.

When a US startup raises money from investors, it usually has to file a short form with the SEC, called a Form D.

It's public. It's free. Most sales teams never look at it.

So I built a workflow in Claude Code that asks one question:

"**Did this company just raise money, and is it hiring the person my product helps?**"

Money tells you they can buy.
A job post tells you what they want to fix.
Both in the same week = a real reason to reach out.

I ran it on one week of filings (Oct 31 to Nov 6):

844 filings → 293 real companies, not funds → 84 tech → 10 with a jobs page I could find → 4 hiring for sales or marketing.

I checked all 4 by hand. Every one was real.

**The surprise:** 74 of those 84 tech companies had no public jobs page yet. The money shows up before the hiring does. If you only watch job posts, you're late.

**What I learned:**
• **Use data people are forced to publish.** Filings and registries are free, dated and hard to fake.
• **One signal is noise. Two are a play.** Money alone or hiring alone isn't enough.
• **Check by hand.** Two companies can share a name.
• **It cost $0.** No paid tools, no API keys.

**Job hunting?** The same run found 448 open roles at these companies. ...

Big thank you to Jordan Crawford, whose writing on public data got me started.

The full play is on my site: the diagram, the steps in plain English, and the prompts. Link in the comments.

Would you use it to find buyers, or your next job?
```

## 8. Asshvin's own post (the voice model)
The post that set this style was Asshvin's Nextiva post ("I was one plane ticket away from a completely different life."). What to copy from it:
- a personal moment in the bold first line
- the turn ("Then a LinkedIn message changed everything." / "This one was different.")
- honesty about the hard middle
- thanking people by name
- a "→" journey line
- bold lessons
- an offer to help at the end

## 9. Website copy (plays pages)
- Same plain voice, fewer words. Headline in one line.
- Sections in this order: what it does → the run receipt → the diagram → why it works → how it works (5 one-line steps) → real examples → is the data free (quote each source's own docs) → where it can go wrong (3 or 4 plain boxes) → the Claude Code prompt.
- Visual style: see `skills/animated-infographic/SKILL.md` (dark navy, Instrument Serif headlines, light-blue accent, JetBrains Mono labels).
