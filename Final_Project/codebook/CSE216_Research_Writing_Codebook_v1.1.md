# CSE 216 — Research Writing & AI Interaction Codebook

**Project:** *Offloading or Surrendering? Mapping Where AI Assistance Substitutes for Thinking in Research Writing*
**Version:** 1.1, frozen Nov 6, 2026. Do not change it before Bet 4 is coded. A change after this point needs a new version and a logged recode.
**Status:** Earlier drafts were piloted on 110 real windows in three rounds by two AI coders, plus 12 constructed cases. This final text was piloted on 22 more windows in round 4. **Not validated.** No human has coded with it yet. Agreement between two AI coders is a consistency check only, since two models can share a bias.
**Replaces:** v1.0 (Nov 2, 2026). Every change is in `decisions.tsv`, with its evidence in `REPORT.md`.

> **What this is.** Q1–Q5 are a project-specific coding scheme for observable behavior. They are not new as ideas. Who directs the work is coded from prompts by Poquet et al. 2026. Levels of offloading from surface to reasoning, read from interaction and revision evidence, come from Chen 2026. Follow-up types come from Mysore et al. 2025. Paste and edit measures come from NIRVANA (Jelson et al. 2026) and Welzel & Vincent 2026. Division of labor and metacognitive oversight as two axes come from T. Kim et al. 2025 [abstract only]. What this scheme adds is coding these together per window and grading the grounds of a check, and the second is still unproven. No source validates `decision`, `verification` or `uptake` as a set.

## 1. What the codes can and cannot say

**Unit.** One request → its AI response → the writer's first relevant next action, before the next request. Start a new unit at each new request.

**Codes describe behavior, not cognition.** A writer may read and judge silently. So:

- `V0` does not mean the writer did not think.
- `D2` does not mean surrender.
- Absence of visible own work does not mean no work was done.
- **There is no per-window "offloading" or "surrender" label.** Q3–Q5 are reported as risk indicators (§9). Agreement is measured on the observable codes. Relating patterns to offloading and surrender is a later interpretive step, and it is argued, not coded.
- **AI correctness is not coded.** `D4`+`V0` on a true claim and on a false one look the same here. Shaw & Nave and Tao can read uptake against known truth because they plant answers or flaws. This project cannot. If an AI error is plainly visible in the window, note it in `evidence_note`.

## 2. Setup fields

**`coverage`** is given to you. Do not recode it.

| Code | Visible | Consequence |
|---|---|---|
| `C0` | Request and response, no usable next action | `V`=`VX`, `U`=`UX` |
| `C1` | Plus later chat turn only | Chat evidence only. Never `U1`,`U2`,`U3`,`U7` |
| `C2` | Plus editor or paste actions | Can code editor use |

**`domain`.** `ESSAY_TASK` (always for NIRVANA), `RESEARCH_EXPLICIT` (the trace clearly concerns scholarly writing: paper, literature review, methods, research question), `ACADEMIC_STATED` (a course assignment with no research-writing element), `OTHER_WRITING`, `DOMAIN_UNKNOWN`. A course assignment that is itself research work is `RESEARCH_EXPLICIT`.

**`prior_own_work`.** Own work by the writer on this document that is visible before this request. Look at the editor state, the request, and earlier turns.

| Code | Use when |
|---|---|
| `VISIBLE_DRAFT` | Running text by the writer, at least a few full sentences |
| `VISIBLE_PARTIAL` | Notes, fragments, an outline, or a stated position of the writer's own |
| `NONE_VISIBLE` | **NIRVANA only.** The editor and chat show none. The channel exists, and it shows nothing |
| `UNOBSERVABLE` | **Chat-only data with no writer text in it.** The writer's document is outside the channel |

Text pasted from the AI is not own work. An assignment prompt is not own work. In WildChat, pasted text is treated as the writer's, but authorship cannot be confirmed. **Absence never means no work.**

## 3. Q1: operation

Code from the request. One primary label, by the dominant requested deliverable. If the request is bare (only a paste, or an unfinished sentence), infer the task from earlier turns or the pasted task, and say so in the note.

| Code | Operation | Boundary |
|---|---|---|
| `O01` | Goal or problem framing: purpose, research question, scope | Wording an already set thesis → `O14`/`O08` |
| `O02` | Ideation: topics, examples, candidate directions | Judging evidence for one claim → `O06` |
| `O03` | Organization: outline, sequence, argument plan before drafting | Reordering an existing draft → `O13` |
| `O04` | Source discovery: find papers, references, search terms, a fact or statistic | Does the source support the claim? → `O06` |
| `O05` | Comprehension of one supplied text or term: a source, an assignment prompt, a marker's feedback, a definition | Across several sources → `O07` |
| `O06` | Evidence or claim evaluation: relevance, strength, support | Rewording for fluency → `O14` |
| `O07` | Cross-source synthesis | Listing citations → `O04`/`O11` |
| `O08` | Claim or thesis formulation and scoping | Organizing around a fixed claim → `O09`/`O03` |
| `O09` | Argument construction: warrant, counterargument, reasoning | Prose from a complete supplied argument → `O10` |
| `O10` | Drafting: new sentences, sections, essays, or **expanding with new content** | Rewrite with no new content → `O14`/`O12` |
| `O11` | Citation or evidence integration: link a reference to a passage, reference list | Formatting only → `O15` |
| `O12` | Substantive review: critique or change meaning, claim, argument | Drafting from scratch → `O09`/`O10` |
| `O13` | Coherence or structure: reorder, connect, **write a transition between existing parts** | Changing the inference → `O12` |
| `O14` | Language: proofread, simplify, tone, **shorten, translate supplied text** | Editing a caveat or result → `O12` |
| `O15` | Formatting: LaTeX, bibliography style, headings | Whether to cite → `O11` |
| `O16` | Monitoring: workflow, what to do next, reflection on AI use | A concrete outline → `O03` |
| `OX` | Not classifiable, or **not a writing request** (a chat about the AI itself, a code task with no writing). Explain in the note | |

**Report at family grain.** `FRAME_IDEA_PLAN` (`O01`–`O03`), `SOURCE_WORK` (`O04`–`O07`), `CLAIM_ARGUMENT` (`O08`–`O09`), `PROSE_CITATION` (`O10`–`O11`), `REVIEW_SUBSTANCE` (`O12`–`O13`), `SURFACE` (`O14`–`O15`), `MONITOR` (`O16`). A script rolls codes up. Chen 2026's four layers informed this reporting choice. The grouping itself is the project's, and it is not Chen's.

**`process` is no longer coded.** A script derives it from `operation`, after Flower & Hayes 1981: `O01`–`O09`→`P`; `O10`–`O11`→`T`; `O12`–`O15`→`R`; `O16`→`M`; `OX`→`PX`.

## 4. Q2: delegation

Code what the writer **asks for**, not what the AI delivers.

| `function` | Definition | Boundary |
|---|---|---|
| `F1_EXPLAIN` | Explain or summarize for understanding | Summary of someone else's text defaults here |
| `F2_OPTIONS` | Generate alternatives or directions | One final thesis to insert → `F4` |
| `F3_PLAN` | Outline, plan, argument map | Full prose → `F4` |
| `F4_GENERATE` | New claim, argument, draft, completed text, or added content | |
| `F5_TRANSFORM` | Rewrite, proofread, translate, shorten supplied text, with no new content asked for | Asks for more content → `F4`. Shortening the writer's own text defaults here |
| `F6_CRITIQUE` | Evaluate, score, diagnose | Source validity → `F7` |
| `F7_FIND_CHECK` | Locate evidence or generate a reference list; check facts or attribution | Formatting known references → `F8` |
| `F8_PROCEDURAL` | Formatting, syntax, conventions | |
| `FX_OTHER` | Unclear or not a writing request. Explain | |

**`object`.** One of `IDEA`, `SOURCE`, `EVIDENCE`, `CLAIM`, `ARGUMENT`, `STRUCTURE`, `PROSE`, `REFERENCE`, `PROCESS`, `OTHER`. `EVIDENCE` means material from a source or data. An example offered to illustrate a point, or a research question, is `IDEA`. An assignment prompt is `OTHER`.

## 5. Q3: decision

A substantive decision changes a goal, claim, argument, interpretation, evidence choice or meaningful plan. Answer in three steps.

**Step 1. Is any substantive decision in play in the response?** If not → `D0`.
**Step 2. Where did the response's main content come from?** List its main claims or choices. If most already appear in text the writer supplied → `D1`. If most are new in the response, **or come from an earlier AI turn** (the writer asks the AI to rework its own output) → AI-origin, go to step 3. A summary, comparison or analysis of supplied material is AI-origin, because what is selected or concluded is new. It takes this route even when the request is only to understand the material. A rewording of the writer's own claims stays `D1`. A stated stance counts only for what it states. If the writer gives a stance and asks the AI to argue it, the arguments are AI-origin. An assignment prompt or a generic instruction ("write my essay") is not a writer's decision.
**Step 3. For AI-origin content, what does the next action show?** `D4`, `D3`, or else `D2`.

| Code | Use when | Do not use when |
|---|---|---|
| `D0_NO_DECISION` | Mechanical work (formatting, citation syntax), an explanation of a term, task or feedback that offers no claim for the writing, or a non-writing request | **Polishing or translating text with claims in it is `D1`, not `D0`** |
| `D1_HUMAN_GIVEN` | The response mainly renders content the writer supplied, including proofreading and rewording | |
| `D2_AI_PROPOSED_OPEN` | AI-origin content, and no acceptance, selection or change is shown. **Includes typed text that only echoes the AI's ideas** | Not acceptance, and not surrender |
| `D3_HUMAN_CHOSE_REVISED` | The writer explicitly selects or rejects, pastes less than about half of the response, or pastes and then changes or adds claims. Exchanges where both parties change a claim go here too (v1.0's `D5`) | Cosmetic edits alone. A silent resend is `D2` |
| `D4_AI_PROPOSAL_TAKEN` | The writer says they accept it, or reuses about half or more of it verbatim in the editor (paste or retyped run of about 30+ characters) with no content change | Echoes without a verbatim run. Not proof of uncritical belief |
| `DX_INDETERMINATE` | Origin truly cannot be told from the window | Not a fallback for hard calls between `D2` and `D4`. **A request missing its input, where the AI invents content, is AI-origin: `D2`** |

**Never infer adoption from conceptual similarity in typed text.** No threshold exists for it, and coders cannot apply one. Use `D2`.

## 6. Q4: verification

**Only the next action counts.** A challenge written in this request is aimed at the previous response, so credit it to the previous window. Code what the writer visibly does to check **this response**. This field means visible checking, never attention.

| Code | Use when | Does not count |
|---|---|---|
| `V0_NONE_VISIBLE` | A next action exists and shows no check. Includes a move to a new goal, requests for more content or more depth, and questions about the writer's own text | Does not mean no thought |
| `V1_SURFACE_ONLY` | The writer visibly edits **AI text** only for grammar, tone or format, or asks for changes of style, length or format to this output | Edits to the writer's own text |
| `V2_AI_SELF_CHECK` | The writer asks the AI to justify, recheck or add references to its own content, with no independent grounds. "Are you sure?" | AI citations are not independent |
| `V3_REASONED_CHALLENGE` | **In words**, the writer gives a counterexample, limit, contradiction, or criterion against this output. An assignment requirement counts as a criterion. **Weak evidence:** Tao et al. 2026 found stated reasons can be superficial, so `V3` shows stated engagement, not quality of evaluation | **Silent content edits are `U3`, not `V3`** |
| `V4_SOURCE_COMPARISON` | The trace compares this output with original source text, data, or evidence the writer supplied, with or without a stated reason (v1.0's `V5` goes here) | Asking the AI for sources → `V2` |
| `VX_UNOBSERVABLE` | `C0` only | Not a failure to verify |

Priority: `V4` > `V3` > `V2` > `V1` > `V0`. A style complaint in words ("too many big words", "that's filler") is `V1`, not `V3`. Pasting the error from running the AI's code counts as evidence: `V4`. Asking the AI to polish its own last output is `V1`. A deletion of a few characters at a paste seam is not an edit: `V0`. Asking the AI to check the writer's own essay is a new request, not a check on this output: `V0`.

## 7. Q5: uptake

The first relevant, traceable treatment of this response. Editor events come before the next chat turn in time, so read them first.

| Code | Definition | Evidence |
|---|---|---|
| `U1_EDITOR_DIRECT` | AI text pasted, or a verbatim run retyped, with no later change to it in the window. A few characters trimmed at a paste seam still count as no change | `C2` |
| `U2_EDITOR_SURFACE` | AI text inserted, then only surface changes to it | `C2` |
| `U3_EDITOR_SUBSTANTIVE` | AI text inserted, then its claim or evidence changed, or claims replaced or added beside it | `C2`. Explain the change |
| `U7_EDITOR_NEW_TEXT` | Text typed on the goal with no verbatim AI run. Origin of ideas stays open | `C2`. Never infer origin from typing |
| `U4_CHAT_ITERATE` | The next turn **reacts to or works on this output, including feeding it into a new task**, or repeats or repairs the same request (including sending input that was missing). A follow-up is not by itself human-led | Chat |
| `U5_CHAT_ACCEPT` | The writer says they will use, accept or select from this output, with no insertion seen. Courtesy or praise alone is `U8` | Chat |
| `U6_REJECT` | The writer says no to this output in words ("no", "not what I wanted"), even if they then ask again. Comes before `U4`. A silent resend is `U4` | Chat or editor |
| `U8_MOVED_ON` | **New.** A next turn exists but does not touch this output: the next paragraph of a batch, a different sub-goal, an unrelated text. Says nothing about use | Chat |
| `UX_NO_TRACE` | Nothing relevant observable. Always for `C0`. A copy with no paste stays `UX`; say so in the note | |

If a turn both accepts and asks for more, code `U5` only if it states use, acceptance or a selection. Otherwise code `U4`. **`U8` is not `U4`, and `UX` is not `U8`.** With `U8`, `V` is `V0`.

**Script audit.** Coders label from the trace. `scripts/overlap.py` then measures, with no judgment, how much added text matches this response and how much pasted text survives. It audits `U1`, `U2`, `U7`. When coder and script differ on `U1` vs `U2`, the script decides: `U1` if at least 99.5% of pasted AI text survives in the editor at the end of the window, else `U2`. Whether a change is surface or substantive (`U2` vs `U3`) stays a reading judgment. Coders do not see these numbers.

**`u4_subtype`, secondary note, not in agreement statistics.** Adapted from Mysore et al. 2025 Table 4 (11 follow-up types). `RESTATE_OR_ELABORATE`, `MORE_OUTPUTS`, `QUESTION`, `STYLE`, `ADD_OR_REMOVE_CONTENT`, `OTHER`. Mysore's courtesy and feedback types map to `U5`/`U6` or to `OTHER`, and its "original request" is close to `U8`.

## 8. Worked examples (constructed, not data)

| # | Case | Codes |
|---|---|---|
| E1 | "Format this citation in ACM style." Pasted (`C2`) | `O15` `F8` `REFERENCE` `D0` `V0` `U1` |
| E2 | Writer's limited claim, "fix grammar, keep the limit". Pasted, wording edits | `O14` `F5` `PROSE` `D1` `V1` `U2` |
| E3 | "Polish this paragraph." Next turn is the next paragraph, no comment (`C1`) | `O14` `F5` `PROSE` `D1` `V0` `U8` |
| E4 | "Give three thesis options." The writer picks one and limits it, saying the evidence does not generalize (`C1`) | `O08` `F2` `CLAIM` `D3` `V3` `U5` |
| E5 | "Write a full essay." Pasted whole, no edits | `O10` `F4` `PROSE` `D4` `V0` `U1` |
| E6 | The writer states a stance, asks for an essay. Pasted, then claims replaced | `O10` `F4` `PROSE` `D3` `V0` `U3` |
| E7 | "What is lost here?" The AI lists items. The writer types own sentences near one item, no verbatim run | `O02` `F2` `IDEA` `D2` `V0` `U7` |
| E8 | "Compare papers A and B, find a gap." No later action (`C0`) | `O07` `F4` `EVIDENCE` `D2` `VX` `UX` |
| E9 | "Summarize this study." The writer quotes the source's limit and says the summary overgeneralizes (`C1`) | `O05` `F1` `SOURCE` `D3` `V4` `U4` |
| E10 | "Is that definitely true? Give references." on the AI's own claim, next action of the prior window | Prior window `V2`, `U4` |
| E11 | "Generate an outline." "I'll use this outline." (`C1`) | `O03` `F3` `STRUCTURE` `D4` `V0` `U5` |
| E12 | A polish template with no text attached. The AI invents a paragraph. The writer then sends the text (`C1`) | `O14` `F5` `PROSE` `D2` `V0` `U4` |
| E13 | "Condense what you wrote above." The next turn feeds that summary into a new question (`C1`) | `O14` `F5` `PROSE` `D2` `V0` `U4` |
| E14 | "Write my conclusion." The AI gives advice only. "No, write the actual text." (`C1`) | `O10` `F4` `PROSE` `D3` `V0` `U6` |

## 9. How Q3–Q5 are reported

Report them as **risk indicators, computed by script from the codes**, per dataset and family. These are candidates for Bet 5, written before coding so that they cannot be fitted to it. They are hypotheses, not findings, and not diagnoses of a person.

| Candidate indicator | Rule | What it does not show |
|---|---|---|
| AI content adopted, no visible check | `D4` + (`V0` or `V1`) + (`U1` or `U2`) | Silent evaluation, or whether the content was right |
| Only the AI checks itself | `V2` with no `V3`/`V4` later in the session | Checks in another tab |
| Surface edits on substantive AI drafting | `F4` + `V1` + `U2` | Whether the writer agreed already |
| AI content changed by the writer | `D3` + (`U3` or `V3`/`V4`) | Whether the change is an improvement |
| Writer-supplied content rendered by AI | `D1` | Whose idea it first was |
| No visible own work before asking for generation | `NONE_VISIBLE` + `F4`. **NIRVANA only**, since WildChat has no editor | Earlier thinking, notes elsewhere |

T. Kim et al. 2025's axes, division of labor and metacognitive oversight, can serve as a credited map: Q2–Q3 for the first and Q4 for the second [abstract only; conceptual paper]. **Mechanical work is not automatically low stakes:** whether a demand matters depends on the learning goal (Risko & Gilbert 2016, ms p. 14).

The proposal's success criterion says the framework "assigns real interactions to these categories". Windows are assigned to observable risk patterns. Offloading and surrender stay interpretive. Milestone 2 states this reinterpretation plainly, and it is raised with the instructor on Nov 19.

## 10. Coding record

`window_id`, `domain`, `prior_own_work`, `operation`, `function`, `object`, `decision`, `verification`, `uptake`, `confidence` (`HIGH`, `MEDIUM`, `LOW`), `evidence_note`, optional `u4_subtype`, `flag_note`. One primary label per field. Report windows from one session as clustered, not independent. Keep NIRVANA and WildChat separate. NIRVANA is a timed essay, not research writing, and WildChat identities are unknown and its use of text is unseen.

## 11. References

Flower & Hayes 1981, *CCC* 32(4). · Le et al. 2026, ScholaWrite, arXiv:2502.02904. · Risko & Gilbert 2016, doi:10.1016/j.tics.2016.07.002. · Reza et al. 2025, arXiv:2504.12488. · Jelson et al. 2026, arXiv:2501.10551. · Jelson et al. 2026, NIRVANA, arXiv:2604.07344. · Mysore et al. 2025, EMNLP, doi:10.18653/v1/2025.emnlp-main.852. · Poquet et al. 2026, doi:10.1007/978-3-032-37979-5_34. · Chen 2026, doi:10.3389/fpsyg.2026.1906199. · T. Kim et al. 2025, doi:10.1002/arcp.70008. · Tao et al. 2026, arXiv:2609.23936. · Welzel & Vincent 2026, doi:10.1145/3805689.3812389. · Shaw & Nave 2026, SSRN 6097646. · Peters & Chin-Yee 2025, doi:10.1098/rsos.241776. · Zhao et al. 2024, WildChat, arXiv:2405.01470. · van Merriënboer & Sweller 2010, doi:10.1111/j.1365-2923.2009.03498.x. · Zimmerman 2002, *Theory Into Practice* 41(2). · Bereiter & Scardamalia 1987. · Harvard College Writing Program, *A Source's Role in Your Paper*, Harvard Guide to Using Sources, https://usingsources.fas.harvard.edu/sources-role-your-paper (v1.0 said Writing Center; the page says Writing Program).

## 12. Change log

v1.0 → v1.1: see `decisions.tsv`. `decisions.tsv` marks edits made after round 3; round 4 tested the final text. Drafts between rounds were not archived, so the log is the record of them. v1.0 stays in place as the earlier version.
