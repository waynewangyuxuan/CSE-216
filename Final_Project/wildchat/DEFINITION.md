# Inclusion definition (Bet 7, frozen before screening)

Written 2026-11-07 before any record was labelled under it. Its sha256 is in `decisions.tsv` W01. Changing it after screening means a new version and a rerun, logged.

## Include

A conversation is **formal long-form writing** when, somewhere in it, the user is producing or revising an extended, formal text. The text is one of:

- an essay, including a course essay or an essay-style answer of several paragraphs
- a research paper, journal or conference article, or a section of one (abstract, introduction, literature review, methods, results, discussion, conclusion)
- a report (lab, technical, business, policy or course report)
- a thesis, dissertation or capstone, or a chapter or section of one
- a literature review or annotated bibliography that runs as prose
- a proposal (research, grant, project or business proposal; a business plan)
- an article for publication: news, feature, opinion, review, or an expository magazine or encyclopedia-style piece
- a formal statement: personal statement, statement of purpose, scholarship or admission essay, policy or position statement

"Producing or revising" covers any route: the user drafts and asks for edits, pastes text for paraphrase, proofreading or expansion, asks for an outline or a section, or asks the AI to write the whole text. Asking the AI to write the whole text counts.

## Boundary calls

| Case | Call | Why |
|---|---|---|
| Fiction, poetry, song lyrics, scripts, role-play, fan fiction | Exclude | Creative, not formal expository text |
| Emails, letters, cover letters, messages, social posts | Exclude | Short correspondence, not long-form |
| Résumés, CVs, LinkedIn summaries | Exclude | Templated job documents |
| Marketing, SEO or product copy, ads, slogans, listicles for promotion | Exclude | Promotional, not formal expository |
| Blog posts | Include only when written as an expository or argumentative article; exclude SEO or promotional posts | Follows the article rule |
| Speeches, presentation slides, video scripts | Exclude | Spoken or visual genre |
| Short answers: quiz or homework items, definitions, one-paragraph replies, multiple choice | Exclude | Not extended. An "answer in N words" item counts as an essay only when the target is several paragraphs (about 300 words or more) |
| A single paragraph that is plainly part of a longer formal text the user is writing (e.g. "rewrite this paragraph of my thesis") | Include | The text is long-form even if one paragraph is in view |
| Code, software documentation, READMEs, data analysis | Exclude | Not prose writing |
| Translation only | Exclude unless the user is also producing or revising the text | Translation of another's text is not producing it |
| Summaries of a source for the user's own reading | Exclude unless the summary is written into the user's document (e.g. a literature review) | Reading aid, not writing |
| Factual questions, tutoring, brainstorming with no target text | Exclude | No text is being produced |
| Mixed conversations | Include if any part meets the rule | The writing task may come at any turn |

When the evidence is too thin to decide, the label is `UNSURE`, which is not included.

## Mechanical requirements (applied by script)

1. WildChat-1M, the non-toxic release (`allenai/WildChat-1M`, pinned revision). The `toxic` field is checked to be false.
2. Conversation `language` field is English.
3. At least 2 non-blank user turns.
4. The writing task may appear in any turn, not only the first. The labeller reads the whole conversation. A conversation also needs at least one user turn after the first writing-task turn, so the writing has a follow-up to code.
5. Not already used: conversations in `coding/` (Bet 4 sample and gold) or the codebook pilot rounds are excluded from selection, and re-judged separately.
6. Duplicates: the first record of each `conversation_hash`, then the first of each normalized first user turn, in shard and row order.
