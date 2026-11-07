# CSE 216 — Writing & AI Interaction Codebook

**Project:** *Offloading or Surrendering? Mapping Where AI Assistance Substitutes for Thinking in Writing*
**Scope:** formal long-form writing (NIRVANA timed essays; WildChat formal long-form writing), reported as one writing activity. RQ1: which observable patterns of AI use in writing support thinking (offloading) and which substitute for it (surrender). RQ2: which substitutions the writer is likely to notice (analytic only). RQ3: which observable features could signal substitution risk and ground in-situ feedback.
**Version:** 1.2, frozen Nov 7, 2026 (hash in `FROZEN.md`). Sections 1–8 and 10 keep v1.1's coding rules word for word, except the scope line, the §1 bullet on categories and §2's domain note; no window needs recoding. **New:** §9, the inference layer. A change after this point needs a new version.
**Status:** Earlier drafts were piloted on 110 real windows in three rounds by two AI coders, plus 12 constructed cases. This final text was piloted on 22 more windows in round 4. **Not validated.** No human has coded with it yet. Agreement between two AI coders is a consistency check only, since two models can share a bias.
**Replaces:** v1.1 (Nov 6, 2026, `codebook/`). v1.0→v1.1 changes are in `codebook/decisions.tsv`; v1.1→v1.2 changes are in `inference/decisions.tsv`, with evidence in `inference/REPORT.md`.

> **What this is.** Q1–Q5 are a project-specific coding scheme for observable behavior. They are not new as ideas. Who directs the work is coded from prompts by Poquet et al. 2026. Levels of offloading from surface to reasoning, read from interaction and revision evidence, come from Chen 2026. Follow-up types come from Mysore et al. 2025. Paste and edit measures come from NIRVANA (Jelson et al. 2026) and Welzel & Vincent 2026. Division of labor and metacognitive oversight as two axes come from T. Kim et al. 2025 [abstract only]. What this scheme adds is coding these together per window and grading the grounds of a check, and the second is still unproven. No source validates `decision`, `verification` or `uptake` as a set.

## 1. What the codes can and cannot say

**Unit.** One request → its AI response → the writer's first relevant next action, before the next request. Start a new unit at each new request.

**Codes describe behavior, not cognition.** A writer may read and judge silently. So:

- `V0` does not mean the writer did not think.
- `D2` does not mean surrender.
- Absence of visible own work does not mean no work was done.
- **Coders do not label offloading or surrender.** A script assigns each window one category from its codes (§9). The category is a literature-grounded inference from behavior with a stated strength, never a probability or a measure of cognition. Agreement is measured on the observable codes only.
- **AI correctness is not coded.** `D4`+`V0` on a true claim and on a false one look the same here. Shaw & Nave and Tao can read uptake against known truth because they plant answers or flaws. This project cannot. If an AI error is plainly visible in the window, note it in `evidence_note`.

## 2. Setup fields

**`coverage`** is given to you. Do not recode it.

| Code | Visible | Consequence |
|---|---|---|
| `C0` | Request and response, no usable next action | `V`=`VX`, `U`=`UX` |
| `C1` | Plus later chat turn only | Chat evidence only. Never `U1`,`U2`,`U3`,`U7` |
| `C2` | Plus editor or paste actions | Can code editor use |

**`domain`.** `ESSAY_TASK` (always for NIRVANA), `RESEARCH_EXPLICIT` (the trace clearly concerns scholarly writing: paper, literature review, methods, research question), `ACADEMIC_STATED` (a course assignment with no research-writing element), `OTHER_WRITING`, `DOMAIN_UNKNOWN`. A course assignment that is itself research work is `RESEARCH_EXPLICIT`. **v1.2 note:** codes are unchanged, but RQ analysis pools all formal long-form writing as one writing activity; `domain` is kept as a descriptor, not a split.

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

## 9. Inference layer: from codes to a window category

**What this section does.** It replaces v1.1 §9, which kept offloading and surrender "interpretive". Following Wayne's Nov 7 direction, a script (`inference/scripts/apply_rules.py`) assigns each window exactly one category from its Q1–Q5 codes and `prior_own_work`, with a strength and the rule that fired. Q1–Q5 are unchanged from v1.1, so no window is recoded.

**What a category is, and is not.** A category is a **literature-grounded inference from observed behavior**. It says which pattern in the sources the window's behavior resembles. It is not a probability, not a measurement of cognition, and not a judgment of the person. Shaw & Nave define surrender partly by the absence of deliberation (Table 2, p. 16), which no log can show. Every category therefore keeps the silent-evaluation alternative open. Agreement numbers (Bet 4) cover the codes, not the categories. No number here calibrates a category against cognition.

**Scope.** RQ1–RQ3 concern formal long-form writing, reported as one writing activity: NIRVANA timed essays and WildChat formal long-form writing together, with datasets kept apart in counts because their coverage differs.

**v1.1's candidate risk indicators** stay computable from the codes. The rules absorb them: "AI content adopted, no visible check" is R09/R11; "surface edits on substantive AI drafting" is R15 (chat) or R11 (editor); "AI content changed by the writer" is R04/R08; "writer-supplied content rendered" is R12–R14. "Only the AI checks itself" (`V2`) is a session-level indicator for Bet 8. T. Kim et al. 2025's two axes, division of labor and metacognitive oversight [abstract only], remain a credited map: Q2–Q3 for the first, Q4 for the second.

### 9.1 Categories

| Category | Project definition (behavioral) | Sources (opened; page = PDF page unless noted) |
|---|---|---|
| `SURRENDER_LEANING` | AI-originated substance (claim, argument, draft text) is taken over or carried forward with no visible check beyond surface edits | Shaw & Nave 2026: surrender is "uncritical adoption", the answer "accepted as one's own, without verification" (Table 2, p. 16); it is "an uncritical abdication of reasoning itself", unlike offloading (p. 17); expected signs are acceptance without critical analysis and low override (p. 18). Bastani et al. (working-paper version): students "simply copying answers" from unrestricted GPT-4 (p. 14), and conversations that only ask for the answer are "superficial" (p. 15). Contractor & Reyes 2026: "automation", AI doing the work for the student, e.g. generating essay text (LLM prompt, p. 68); automation users' essay advantage is gone a week later (p. 23) |
| `OFFLOADING` | The writer keeps the substance. Either the AI handles a demand that is not the substance (language, mechanics, format of the writer's own content), or AI content is integrated under visible writer control (selection, partial take, claim change, reasoned challenge) | Risko & Gilbert 2016: offloading is "the use of physical action to alter the information processing requirements of a task in order to reduce cognitive demand" (ms p. 2); its benefit for learning holds only if the demand removed is "unnecessary with respect to the learning goal" (ms p. 14). Shaw & Nave: in offloading "internal reasoning remains active … System 2 integrates artificial cognition. Strategic delegation" (Table 2, p. 16); hybrid routes include "verify-then-adopt, override System 3" (Table 2) |
| `AUGMENTING` | The writer asks for explanation, critique of their own text, or options, and the AI output is not reused as text; the writer keeps composing | Contractor & Reyes 2026: "augmentation", AI working with the student, "understand concepts, get explanations, … get feedback on their own writing, or check their work" (p. 68), classified from logs and separable from automation in prompts, time use, AI-detected text and week-later outcomes (pp. 22–23); explanation, feedback and brainstorming are "with" channels (p. 77). Maier et al. 2026: asking how to approach a problem or for an explanation is "instrumental help that support[s] continued engagement" (p. 2); four requested-support levels from guided help to the complete answer (p. 10). Bastani et al.: "ask for help" and "attempted answers" are non-superficial (p. 15) |
| `NEUTRAL_MECHANICAL` | No substantive writing decision is in play (`D0`): formatting, syntax, a reference look-up, a spelling question, or a non-writing request | **Project category, not from a source.** It follows v1.1 `D0`. Risko & Gilbert warn that whether a demand matters depends on the learning goal (ms p. 14), so "neutral" means "no substantive decision visible", not "low stakes" |
| `INDETERMINATE` | The codes cannot support a category: no next action, no trace, origin unknown, a reject without reasons, or a pattern no rule covers | Project category. v1.1 §1: absence of evidence is never a verdict |

**Augmenting is kept, with a caveat.** Contractor & Reyes separate it from automation by behavior and by outcome, so it is sourced as distinct from surrender. They do not separate it from offloading in the project's sense, and Maier counts guided help as a beneficial form of offloading (p. 5–6). The project keeps `AUGMENTING` apart from `OFFLOADING` because the behavior differs (no AI text enters the document versus AI text on a non-substantive demand), and reports both on the "supports thinking" side of RQ1. Merge them if a reader prefers Maier's usage; no rule changes.

**Categories cut.** None of the proposed five was cut. A separate "hybrid / writer retains control" category (Shaw & Nave's recursive routes) was not added: those routes are folded into `OFFLOADING` (R04, R08), because Shaw & Nave place the locus in System 2 for both.

**"Offloading" is not used the same way across sources.** The project's definition is the one above: Risko & Gilbert's demand reduction, with Shaw & Nave's condition that the writer's own reasoning stays in charge. Sources that use "offloading" for substitution:

| Source | Use | Project term |
|---|---|---|
| Alam 2026, PAUSE (abstract, p. 1) | "AI-associated cognitive offloading" is routinely substituting LLM output for one's own reasoning | `SURRENDER_LEANING` |
| Maier et al. 2026 (pp. 2, 6) | "answer offloading", requesting the complete answer, is the negative form | `SURRENDER_LEANING` when adopted |
| Contractor & Reyes 2026 (p. 77) | In students' narratives, "shortcutting and offloading" are channels where AI works for the student | `SURRENDER_LEANING` |
| Risko & Gilbert 2016 (ms pp. 2, 12, 14) | Neutral: costs and benefits | `OFFLOADING` only when the substance stays the writer's |

### 9.2 Strength

| Strength | Meaning |
|---|---|
| strong | The window shows the behavioral signature a source names (AI answer copied with no check), and coverage lets the codes see it (`C2`, `NONE_VISIBLE`) |
| moderate | Matches a source's definition, but one element is unobservable (chat-only uptake, own work outside the channel) or a live alternative stays open (e.g. visible own work before a `D4` paste: the writer may already have held the idea) |
| weak | Matches only by request type or by extending a source beyond its task |

Strength grades the link between behavior and source. It is not a confidence score.

### 9.3 Rule table

First match wins, so every window gets exactly one category. `NOCHECK` = `V0`, `V1` or `V2` (`V2` asks the AI to check itself, which v1.1 §6 says has no independent grounds; no calibration window had `V2`, so this is untested). Calibration changes from draft 0 are logged in `inference/decisions.tsv`.

| Rule | Pattern (codes) | Category | Strength | Source support | Main alternative reading |
|---|---|---|---|---|---|
| R00 | Any field missing, `UNSETTLED`, or not a v1.1 code | `INDETERMINATE` | – | v1.1 §1 | – |
| R01 | `D0` + `F4` | `INDETERMINATE` | – | v1.1 §1 | Generation was requested (C&R automation, p. 68), but nothing substantive came back to adopt |
| R02 | `D0` (other) | `NEUTRAL_MECHANICAL` | moderate | Project category (v1.1 `D0`) | Mechanical work can be the learning goal (Risko & Gilbert ms p. 14); a term explanation can be C&R "get explanations" (p. 68) |
| R03 | `C0`, or `UX`, or `DX` | `INDETERMINATE` | – | v1.1 §1, §2 | A request for generation alone resembles C&R automation, but no use is seen |
| R04 | `V3` or `V4` | `OFFLOADING` | moderate | Shaw & Nave: verify-then-adopt, override (Table 2, p. 16) | Tao et al. 2026 (v1.1 §6): stated reasons can be superficial |
| R05 | `U6` (reject in words) | `INDETERMINATE` | – | – | Override of System 3 (Shaw & Nave), or a demand for fuller text (v1.1 E14) |
| R06 | `D3` + (`U1`/`U2`) + `NOCHECK` | `SURRENDER_LEANING` | moderate | Shaw & Nave: answer "accepted as one's own, without verification" (Table 2, p. 16), applied to the part taken | Choosing which part to take is itself a judgment |
| R07 | (`D3` or `U3`) + chat uptake (`U4`/`U5`) + no own work visible (`NONE_VISIBLE`/`UNOBSERVABLE`) | `SURRENDER_LEANING` | weak | Shaw & Nave: offloading needs "internal reasoning remains active" (Table 2, p. 16); chat steering with nothing of the writer's visible does not show it, and the substance stays AI's | The selection or steer may be the writer's own judgment over the content (Shaw & Nave's override route) |
| R08 | `D3` or `U3` (other) | `OFFLOADING` | moderate | Shaw & Nave: "System 2 integrates artificial cognition" (Table 2) | Changes may be cosmetic in effect; the part kept may still be AI substance |
| R09 | `D4` + `NOCHECK` + (`U1`/`U2`) + `NONE_VISIBLE` | `SURRENDER_LEANING` | strong | Shaw & Nave: uncritical adoption (Table 2; p. 18); Bastani: "simply copying answers" (p. 14); C&R automation (p. 68) | Silent evaluation before pasting; content may be right (AI correctness is not coded) |
| R10 | `D4` + `NOCHECK` + `F1`/`F6` | `AUGMENTING` | weak | C&R: "get feedback on their own writing, or check their work" (p. 68); no AI text enters the writing | Accepting the AI's judgment unchecked is what Shaw & Nave call adopting "the AI's judgment as their own" (p. 4) |
| R11 | `D4` + `NOCHECK` (other) | `SURRENDER_LEANING` | moderate | As R09, with own work visible, or acceptance only in chat | The writer may already have held the idea; the AI only voiced it |
| R12 | `D1` + `U7` | `AUGMENTING` | moderate | C&R: "get feedback on their own writing" (p. 68) | The writer may retype the AI's wording in short runs |
| R13 | `D1` + `F5`/`F8` | `OFFLOADING` | moderate | Risko & Gilbert: demand reduction (ms p. 2), beneficial only if the demand is not the learning goal (ms p. 14); Shaw & Nave: strategic delegation (Table 2) | C&R list proofreading and editing among automation users' uses (p. 52, Fig. A10); if language is the goal, it substitutes |
| R14 | `D1` (other) | `OFFLOADING` | weak | As R13 | The AI rendering may add substance the codes miss |
| R15 | `D2` + `F4` + `V1` | `SURRENDER_LEANING` | moderate | Shaw & Nave: acceptance without critical analysis, low override (p. 18); surface edits are not a deliberation route in Table 2 | The writer may already agree with the content and judge only its form |
| R16 | `D2` + `F4` + (`V0`/`V2`) + (`U4`/`U5`/`U8`) | `SURRENDER_LEANING` | weak | C&R: generating essay text is automation, classified from logs (p. 68); Bastani: asking for the answer is "superficial" (p. 15) | No adoption is seen; the text may be discarded, used as reference, or invented around missing input |
| R17 | `D2` + `F4` + `U7` + own draft visible (`VISIBLE_DRAFT`/`VISIBLE_PARTIAL`) | `AUGMENTING` | weak | C&R: student "retains ownership of the thinking and writing process" (p. 68) | Typed text may echo AI ideas (v1.1 `D2`); without a visible own draft this stays `INDETERMINATE` |
| R18 | `D2` + `F1`/`F6` + (`U4`/`U5`/`U7`/`U8`) | `AUGMENTING` | moderate | C&R: explanations, feedback on own writing (p. 68); Maier: "instrumental help" (p. 2) | A critique can hand over the evaluation the writer would have made; the critiqued text may be AI-written |
| R19 | `D2` + `F2`/`F3` + `U7` | `AUGMENTING` | weak | C&R: brainstorming is a "with" channel (p. 77) | Typed text may only echo AI ideas (v1.1 `D2`) |
| R20 | `D2` + `F7` + `U7` | `OFFLOADING` | weak | Risko & Gilbert: retrieval offloaded to an external store (ms p. 9) | The fact may carry an AI claim into the writing unchecked |
| R99 | Anything else | `INDETERMINATE` | – | – | – |

### 9.4 Coverage

- `C0` and `UX` windows are `INDETERMINATE` unless the request alone is `D0` and not a generation request (R02 comes first).
- WildChat has no editor. `U1`–`U3` and `U7` cannot occur, so R06, R09, R12, R17, R19 and R20 cannot fire, and uptake rests on chat (`U4`, `U5`, `U8`). No WildChat window can be strong. Options or outlines worked on in chat (`F2`/`F3` + `U4`) stay `INDETERMINATE`.
- `UNOBSERVABLE` own work is never treated as `NONE_VISIBLE`.

### 9.5 Session measures (for Bet 8)

Computed by `apply_rules.py` per session, from windows ordered by turn. The 100 calibration windows are a sample, so their sessions are incomplete; complete sessions come from Bets 6 (all NIRVANA) and 7 (WildChat).

| Measure | Definition |
|---|---|
| Category sequence | Categories in turn order |
| Switches | Adjacent pairs with different categories; also reported with `INDETERMINATE` removed |
| Transition counts | Counts of each ordered pair A→B |
| Proportions | Share of windows in each category |
| First surrender-leaning window | Its index (1-based) and relative position (index−1)/(n−1); none if absent |

Report windows from one session as clustered, not independent. A session pattern describes behavior, not a person.

## 10. Coding record

`window_id`, `domain`, `prior_own_work`, `operation`, `function`, `object`, `decision`, `verification`, `uptake`, `confidence` (`HIGH`, `MEDIUM`, `LOW`), `evidence_note`, optional `u4_subtype`, `flag_note`. One primary label per field. Report windows from one session as clustered, not independent. Keep NIRVANA and WildChat separate. NIRVANA is a timed essay, not research writing, and WildChat identities are unknown and its use of text is unseen.

## 11. References

Flower & Hayes 1981, *CCC* 32(4). · Le et al. 2026, ScholaWrite, arXiv:2502.02904. · Risko & Gilbert 2016, doi:10.1016/j.tics.2016.07.002. · Reza et al. 2025, arXiv:2504.12488. · Jelson et al. 2026, arXiv:2501.10551. · Jelson et al. 2026, NIRVANA, arXiv:2604.07344. · Mysore et al. 2025, EMNLP, doi:10.18653/v1/2025.emnlp-main.852. · Poquet et al. 2026, doi:10.1007/978-3-032-37979-5_34. · Chen 2026, doi:10.3389/fpsyg.2026.1906199. · T. Kim et al. 2025, doi:10.1002/arcp.70008. · Tao et al. 2026, arXiv:2609.23936. · Welzel & Vincent 2026, doi:10.1145/3805689.3812389. · Shaw & Nave 2026, SSRN 6097646. · Peters & Chin-Yee 2025, doi:10.1098/rsos.241776. · Zhao et al. 2024, WildChat, arXiv:2405.01470. · van Merriënboer & Sweller 2010, doi:10.1111/j.1365-2923.2009.03498.x. · Zimmerman 2002, *Theory Into Practice* 41(2). · Bereiter & Scardamalia 1987. · Contractor & Reyes 2026, *Experimental Evidence on the Learning Impact of Generative AI*, arXiv:2607.08849. · Bastani et al. 2025, *PNAS* 122(26), doi:10.1073/pnas.2422633122 (read as the working-paper version, *Generative AI Can Harm Learning*; page numbers are that version's). · Maier, Schwabe, Schneider & Feuerriegel 2026, *Designing Against Deskilling*, arXiv:2609.20143. · Alam 2026, PAUSE, arXiv:2609.13155 [abstract only]. · Shaw & Nave 2026 is read from the PsyArXiv/OSF version, doi:10.31234/osf.io/yk25n_v1; page numbers are that PDF's. Risko & Gilbert page numbers are accepted-manuscript pages. · Harvard College Writing Program, *A Source's Role in Your Paper*, Harvard Guide to Using Sources, https://usingsources.fas.harvard.edu/sources-role-your-paper (v1.0 said Writing Center; the page says Writing Program).

## 12. Change log

v1.1 → v1.2: §9 replaced by the inference layer; scope set to formal long-form writing; §1 bullet on categories and a §2 domain note updated. Codes, definitions and worked examples are unchanged. See `inference/decisions.tsv` and `inference/REPORT.md`.


v1.0 → v1.1: see `decisions.tsv`. `decisions.tsv` marks edits made after round 3; round 4 tested the final text. Drafts between rounds were not archived, so the log is the record of them. v1.0 stays in place as the earlier version.
