# CSE 216 — Research Writing & AI Interaction Codebook

**Project:** *Offloading or Surrendering? Mapping Where AI Assistance Substitutes for Thinking in Research Writing*  
**Version:** 1.0 (reconstructed working draft) · **Date:** November 2, 2026  
**Status:** Operational manual ready for a fresh pilot; **not yet validated by independent coding**.  
**Use:** CSE 216 / COGS 230, Milestone 1 discussion and Milestone 2 analysis.

> **Provenance and integrity.** This is a new reconstruction from the submitted proposal, Milestone Report 1, October 17 notes, and the cited literature. It is **not** a recovered copy of the codebook on the unavailable laptop. The 6 real + 16 synthetic pilot cases described in Milestone 1 have **not** been recovered or rerun here; all examples in §8 are freshly constructed and labeled illustrative. The labels and operational rules below are our **proposed synthesis**, not an existing validated scale.

## Executive summary — the one-page version

**Research logic:** `Literature → static writing framework → observable codes → sequences in datasets → distributions / transitions / candidate patterns → RQ1–RQ3.` The codebook is static; patterns and conclusions are empirical products of later analysis, **not labels assumed in advance**.

**Research questions.** RQ1: Which observed AI-use patterns appear to support writer thinking, and which raise substitution risk? RQ2: Which substitutions may be less visible to writers? RQ3: Which observable signals could inform in-situ feedback? **None of these are direct measurements of someone's private cognition.**

**Unit:** One *focal request–response window*, including the writer's first relevant subsequent action(s) for the same writing goal. Maintain links among windows from one goal or session for later transition analysis. Where follow-up is absent, code it as **unobserved**, never automatically “accepted.”

| Milestone 1 question | Fields in this manual | What we can actually code |
|:--|:--|:--|
| Q1. What writing operation? | `process`, `operation` | The task the request/trace visibly addresses |
| Q2. What is assigned to AI? | `function`, `object` | What the writer asks AI to do and to what content |
| Q3. Who contributes decisions? | `decision` | Observable origin, selection, constraints, or adoption of substantive choices |
| Q4. Who checks and on what grounds? | `verification` | Explicit checks, challenges, source comparisons, or absence of visible evidence |
| Q5. How is output used or changed? | `uptake` | Observed follow-up, editor incorporation, revision, rejection, or unknown |

**Minimum record:** `unit_id`, `dataset`, `session_id`, `episode_id`, `turn_order`, `domain`, `evidence_scope`, `process`, `operation`, `function`, `object`, `decision`, `verification`, `uptake`, `evidence_note`, `confidence`. One primary label for each coded field. Optional secondary-operation notes are exploratory and **not** included in agreement statistics.

**Core protection against overclaiming:** A writer may silently read and evaluate an answer; a model may suggest a claim without the writer ever using it. Therefore, `V0 = no check visible` is **not** “did not think,” and `D2 = AI proposed, unresolved` is **not** “surrender.”

---

## 1. Constructs and literature grounding

### 1.1 Five complementary lenses

| Lens | What the literature contributes | How we use it (and do not use it) |
|:--|:--|:--|
| **Writing-process cognition** | Flower & Hayes: recursive **planning, translating, reviewing**, regulated by monitoring [1]. | Provides `process`, a coarse description of *what kind of writing work* is happening. It is not a linear timeline. |
| **Scholarly-writing operations** | ScholaWrite: 15 writing intentions under planning, implementation, revision, derived from scholarly keystrokes [2]. | Grounds our `operation` vocabulary. We add source/claim/argument operations relevant to research writing; we do **not** treat ScholaWrite as AI-interaction data. |
| **Writing-to-learn and education** | Knowledge transforming differs from simply telling what one knows [3]; self-regulation involves goal setting, monitoring and reflection [4]. | Explains the educational stakes of idea, evidence, argument, and review work. Does not justify diagnosis of learning ability from logs. |
| **AI delegation and agency** | Cognitive offloading can be useful [5]. Reza et al. distinguish structured guidance, exploration, co-writing and critical feedback, and find ownership preferences vary across writers [6]. | Motivates separate codes for AI function, visible decision contribution, checks and uptake. None of these alone proves surrender. |
| **Observable AI-assisted writing** | Jelson et al. code queries by writing stage; NIRVANA has chat + editor traces [7,8]. Mysore et al. characterize follow-up behaviors in writing conversations [9]. | Motivates request–response–next-action windows and linked episodes. Establishes important dataset-specific limits. |

A further **AI-specific epistemic risk** is that model-generated summaries of scientific work can overgeneralize the scope of findings [13]. That motivates `O06` (evidence evaluation), `O08` (claim scoping) and `V4` (source comparison), but does **not** mean every AI summary is inaccurate.

Cognitive Load Theory [10] is relevant to why some work is difficult and educationally valuable, but **intrinsic/extraneous/germane load is not a fixed property of an operation**: task complexity, prior expertise, and instructional goals matter. We therefore use it as an interpretive lens, **not as a directly coded psychometric measure**. Source evaluation and integration literature [11] motivates research-specific operations.

### 1.2 Static activity attributes (interpretive layer, not observed mental states)

These attributes are attached to an *operation family* to guide discussion. They are **contextual propositions**; they do not become numeric “surrender scores,” and the coder need not estimate a student's actual cognitive load.

| Activity family | Typical educational role | What AI can substitute for | Why substitution can be hard/easy to notice |
|:--|:--|:--|:--|
| **Framing, ideation, structure** (`O01–O03`) | Setting goals and organizing a rhetorical problem; often central to independent work | Goal statements, ideas, outlines | A coherent outline may appear aligned even when its central framing came from AI. |
| **Source comprehension, evaluation, synthesis** (`O04–O07`) | Understanding source claims, comparing evidence, handling uncertainty; typically core to research training | Search summaries, reading notes, evidence comparisons, syntheses | Fluent summaries may suppress caveats or blur distinctions; source verification is often costly. |
| **Claims and argument** (`O08–O09`) | Formulating, limiting, justifying and revising claims; typically core | Theses, warrants, counterarguments, inferences | Polished reasoning can obscure who made the decisive interpretive choice. |
| **Prose and citation integration** (`O10–O11`) | Translating reasoning into text and connecting it to evidence; learning value depends on the assignment | Full prose, paraphrases, source linkage, citation commands | Text origin is sometimes visible; whether an idea is original can be much less visible. |
| **Substantive and structural review** (`O12–O13`) | Re-evaluating meaning, accuracy, logic, organization; often core | Critique, corrections, reorganizations | A revision can change a conclusion while looking like ordinary editing. |
| **Language, formatting** (`O14–O15`) | Expressive clarity or mechanical compliance; developmental importance is task-dependent | Grammar, concision, reference formatting | Textual changes are usually inspectable; this does not make all style decisions educationally trivial. |
| **Monitoring/self-regulation** (`O16`) | Selecting strategies, reflecting on accuracy, managing assistance; typically core for learning autonomy | AI-generated plans, self-assessment prompts, feedback | Public actions give incomplete access to the writer's private standards or awareness. |

**Four conceptual axes originally promised in the proposal:** (a) *load type*: discuss only conditionally; (b) *AI substitutability*: ability to generate a plausible artifact, not evidence of learning loss; (c) *developmental value*: educational importance conditional on assignment/goals; (d) *detectability*: visibility of a potential transfer of judgment, **not measured self-awareness**. Do not fill a “high/low” value automatically into each case.

---

## 2. Sampling, eligibility and unit boundaries

### 2.1 Eligible material

Include a window when (i) there is a concrete writing or writing-research goal, (ii) the request and response are available, and (iii) the target can be assigned an operation. Both argumentative essays and research writing are eligible, but **must be stratified by domain**. Do not silently assume a WildChat account belongs to a student.

`domain` values:

- `RESEARCH_EXPLICIT`: trace clearly concerns scholarly/research writing (paper, literature review, research claim, methods, etc.). User identity may still be unknown.
- `ACADEMIC_STATED`: an academic assignment is stated without clear research-writing elements.
- `ESSAY_TASK`: constrained argumentative essay (e.g., NIRVANA's study task).
- `OTHER_WRITING`: writing task outside these groups, retained only for boundary testing.
- `DOMAIN_UNKNOWN`: evidence insufficient to determine context.

Exclude clearly unrelated chats and non-writing requests; log exclusions and reasons in the sampling sheet. Preserve the denominator screened, included and excluded. WildChat research-writing examples are **not** evidence about the behavior of identified students without corroboration.

### 2.2 Unit and linked episode

**Base unit:** `one user request → corresponding AI response → first relevant subsequent writer action(s)` about the same immediate goal. Relevant actions include another user turn, tracked editing/paste, explicit acceptance/rejection, or a documented move away from the goal. If no subsequent evidence exists, the unit still gets Q1/Q2 and appropriate unknown labels for Q3–Q5.

**Episode:** one coherent goal (e.g., “formulate the contribution statement”) spanning potentially many base units. Save `episode_id`, `turn_order` and `previous_unit_id` (optional). **Do not compress a long episode into a single subjective “surrender” label**. Episodes are for later sequences and transitions.

**Boundaries and ties:**

1. Start a new base unit at each new request to AI, even if it continues the same episode. Group by focal writing goal, not simply temporal proximity.
2. For a multi-purpose request, choose the **primary** operation by the dominant requested deliverable; write secondary operations in notes. If two independent requests are concatenated, segment them only when the dataset supports a reliable split, and document the rule consistently.
3. Give priority to the **observable requested task** over assumptions about motivation. “Write a paragraph from these ideas” is prose generation even if it could also support planning.
4. Use the first relevant action before a new independent goal or session termination. For NIRVANA, consult intervening editor actions; for WildChat, subsequent chat does **not** establish whether the text was inserted into an outside document.
5. Never merge different participants/sessions into a trajectory. A single-turn session provides a valid descriptive unit but **not** a transition.

### 2.3 Evidence coverage (mandatory metadata)

| Code | What is visible | Downstream constraints |
|:--|:--|:--|
| `C0` | Request + AI response, **no usable subsequent action** | Q1/Q2 possible; Q3 may be `D2` or `DX`; Q4=`VX`, Q5=`UX` by default. |
| `C1` | Request + response + subsequent **chat** turns only | Can code chat acceptance/challenge/iteration; **cannot infer editor uptake**. |
| `C2` | Request + response + temporally linked **editor/paste** actions (possibly chat too) | Can code text incorporation and edits when linkage is clear. |
| `CX` | Truncated/missing request or response / corrupted linkage | Usually exclude from formal sample; retain separate audit row. |

A rich editor trace still does not reveal private reading, thought, independent browser activity, or reasoning not verbalized. `confidence` = `HIGH` (explicit direct evidence), `MEDIUM` (coherent but partial trace), `LOW` (ambiguous); retain low-confidence windows for pilot but consider excluding or separately reporting them in primary quantitative results.

---

## 3. Q1 — Writing operation (`process` + `operation`)

`process` (one required):

- `P` **Planning** — establishing a goal, selecting ideas, gathering/organizing material for writing.
- `T` **Translating** — rendering ideas, evidence or argument into prose/visible manuscript content.
- `R` **Reviewing** — evaluating and modifying existing writing or claims.
- `M` **Monitoring** — reflecting on writing decisions, strategies, progress, standards, or AI use.
- `PX` **Indeterminate/other** — insufficient evidence or outside the model.

The four labels are process-level **functions**, not immutable stages. Assign according to this request's immediate purpose, not the writer's presumed overall stage. `operation` supplies the finer-grained, research-sensitive label:

| Code | Operation and inclusion rule | Contrast / common boundary |
|:--|:--|:--|
| `O01` | **Goal/problem framing.** Define task purpose, research question, scope, success criteria. | Choosing wording for an already-set thesis → `O14` or `O08`. |
| `O02` | **Ideation.** Generate topics, hypotheses, examples, candidate directions. | Select/evaluate evidence for one hypothesis → `O06`. |
| `O03` | **Organization/planning.** Outline sections, sequence ideas, plan argument structure before drafting. | Reorder existing draft paragraphs → `O13`. |
| `O04` | **Source discovery.** Find papers, references, search terms, background material. | Evaluate whether a source's result actually supports a claim → `O06`. |
| `O05` | **Source comprehension.** Explain, paraphrase or interpret what one source says. | Compare findings across multiple sources → `O07`. |
| `O06` | **Evidence/claim evaluation.** Test relevance, strength, reliability, limitations, factual support, or contradiction. | Reword an accurate statement for fluency → `O14`. |
| `O07` | **Cross-source synthesis.** Integrate/compare evidence or positions from two or more sources to develop a conclusion. | Merely listing citations without comparison → `O04`/`O11`. |
| `O08` | **Claim/thesis formulation and scoping.** Formulate, qualify, narrow, or generalize a central claim. | Organize the paragraph around a fixed claim → `O09`/`O03`. |
| `O09` | **Argument/reasoning construction.** Build a warrant, justification, counterargument, causal chain, or relationship between claims and evidence. | Pure prose realization of a complete supplied argument → `O10`. |
| `O10` | **Text drafting/translation.** Produce new sentences, paragraphs, summaries or sections for a document. | Rewrite existing text without new content → `O12`/`O14`. |
| `O11` | **Citation/evidence integration.** Link reference to passage, attribute a statement, create reference list, insert quotation. | Verify whether cited evidence is true/supportive → `O06`; formatting-only → `O15`. |
| `O12` | **Substantive content review.** Critique or change an existing text's factual meaning, argument, claim or interpretation. | Draft a new argument from scratch → `O09`. |
| `O13` | **Coherence/structural revision.** Reorder or connect existing sections, paragraphs, transitions; improve logic of presentation without changing the central claim. | Change underlying inference or conclusion → `O12`. |
| `O14` | **Language/clarity/style revision.** Proofread, simplify, adjust voice/tone, sentence-level concision without intended claim change. | Edit a caveat or statistical interpretation → `O12`. |
| `O15` | **Formatting/mechanics.** LaTeX, bibliography style, headings, figure placement, typographic conventions. | Deciding whether to cite a source as evidence → `O11`. |
| `O16` | **Metacognitive monitoring.** Evaluate workflow, set self-check standards, ask what to do next, reflect on AI dependence or learning. | “What should paragraph 2 contain?” with a concrete outline deliverable → `O03`. |
| `OX` | **Not classifiable** after applying boundary rules. | Use only with a written explanation. |

**Recommended macro defaults (override based on observed purpose):** `O01–O04 → P`; `O05–O09 → P or R` depending on whether initiating or checking a claim; `O10–O11 → T`; `O12–O15 → R`; `O16 → M`. The cross-cutting nature is deliberate: `O06` might occur before drafting or during review. One primary `process` and `operation` per unit.

**Connection to ScholaWrite:** `O02–O03` overlap idea generation/organization and section planning; `O10–O11` overlap text production and citation integration; `O12–O15` overlap accuracy, clarity, coherence, structure, fluency, style and formatting. `O04–O09` make explicit research-specific cognitive activities that a keystroke-intention taxonomy alone may not capture. This is an **informed adaptation**, not a one-to-one reproduction of ScholaWrite's 15 labels.

---

## 4. Q2 — Delegation (`function` + `object`)

Record what the **writer requests** AI to provide, not what the AI successfully delivers. A system may comply poorly; coding delegation does not validate correctness.

| `function` | Operational definition | Disambiguation |
|:--|:--|:--|
| `F1_EXPLAIN` | Explain, define, teach, clarify or summarize information for understanding. | “Explain this paper's limitations” → `F1` unless asked to judge evidence. |
| `F2_OPTIONS` | Generate possible topics, interpretations, directions, alternatives. | Asking for one final thesis to insert → `F4`. |
| `F3_PLAN` | Construct outline, research plan, argument map or ordered steps. | Full paragraphs or an essay → `F4`. |
| `F4_GENERATE` | Produce new substantive claim, argument, draft, summary-for-insertion, or completed text. | Summarize solely to understand → `F1`; ambiguity resolved using wording/context. |
| `F5_TRANSFORM` | Rewrite, proofread, translate, simplify, expand existing supplied content. | Asked to change underlying argument → `F4` or `F6` depending on task. |
| `F6_CRITIQUE` | Evaluate, score, compare, diagnose problems, propose critiques. | Request source validity checking specifically → `F7`. |
| `F7_FIND_CHECK` | Locate evidence/citations; check factual, attribution, source support or reliability. | Merely format known references → `F8`. |
| `F8_PROCEDURAL` | Supply formatting, citation syntax, LaTeX, conventions or mechanical help. | Citation selection as argumentative support → `F7`/`F6`. |
| `FX_OTHER` | Unclear or otherwise outside codes. | Must annotate why. |

Choose one primary `object` (the *content controlled*): `IDEA`, `SOURCE`, `EVIDENCE`, `CLAIM`, `ARGUMENT`, `STRUCTURE`, `PROSE`, `REFERENCE`, `PROCESS`, `OTHER`. If one prompt asks for options **and** polished prose, choose the dominant deliverable and place the rest in `secondary_note` (or segment reliably per §2.2).

**Useful distinction:** Delegating *wording* (`F5` + `PROSE`) is not equivalent to delegating *claim selection* (`F4` + `CLAIM`). The same AI-generated paragraph can involve both. Code the main requested task and record any mixed behavior in evidence notes.

---

## 5. Q3 — Observable decision contribution (`decision`)

A *substantive decision* changes a goal, claim, argument, interpretation, evidence choice, or meaningful organizational plan; spelling and cosmetic changes normally do not count. Track **visible contribution to the decision**, not ownership feelings or mental control.

| Code | Include when the trace shows... | Exclude / caution |
|:--|:--|:--|
| `D0_NO_DECISION` | Mechanical work only; no identifiable substantive choice is at issue. | Choosing which evidence supports a claim is substantive. |
| `D1_HUMAN_GIVEN` | Writer provides the focal substantive decision/argument and asks AI to implement or express it. | A generic “write my essay” instruction is **not** a substantive decision. |
| `D2_AI_PROPOSED_OPEN` | AI introduces a meaningful option/claim/plan but the writer's disposition toward it is **not observed**. | Not evidence that the writer has accepted it. |
| `D3_HUMAN_CHOSE_REVISED` | Writer explicitly selects, rejects, narrows or substantively changes an AI proposal with a discernible decision. | Cosmetic edits alone → not this code. |
| `D4_AI_PROPOSAL_TAKEN` | Writer explicitly accepts/incorporates an AI-origin substantive choice, by statement or traceable adoption into editor. | Means *observable uptake of content*, not proof of uncritical belief. |
| `D5_CO_CONSTRUCTED` | A linked exchange shows **both** parties contributing substantive changes to the same claim/goal. | Repeated “make it longer” requests alone do not qualify. |
| `DX_INDETERMINATE` | Provenance or decision contribution cannot reasonably be established. | Use when missing context, not to mask weak coding rules. |

**Tie-break order:** (1) locate the focal decision, (2) identify its first visible substantive formulation, (3) inspect next actions, (4) choose final trace label. `D2` is the default for a clearly AI-proposed decision with no follow-up; use `DX` if it is unclear whether the idea originated in AI or the writer. `D4` requires affirmative adoption evidence—not merely absence of a complaint. When human and AI both make distinct substantive revisions, prefer `D5`. An AI revision of an author-supplied claim that preserves meaning is generally `D1` even if all resulting words are AI-written.

---

## 6. Q4 — Observable verification and grounds (`verification`)

This is evidence that the writer **checks or questions** the AI contribution, *not* a measure of how much attention they spent internally.

| Code | Sufficient observable evidence | What does **not** count |
|:--|:--|:--|
| `V0_NONE_VISIBLE` | There is a usable subsequent action / editor trace but no substantive or surface check is visible in the window. | Do not use when there is **no** follow-up: `VX`. Does **not** mean “no thought.” |
| `V1_SURFACE_ONLY` | Writer visibly reads/edits only grammar, tone, length, formatting or phrasing. | Does not establish evaluation of content validity. |
| `V2_AI_SELF_CHECK` | Writer asks AI to explain, justify, cite or recheck **its own** claim without visible independent grounds. | AI-generated citations are not independent verification. |
| `V3_REASONED_CHALLENGE` | Writer states a substantive counterexample, limitation, contradiction, criterion, or independent rationale to test AI output. | “Are you sure?” without grounds → `V2`. |
| `V4_SOURCE_COMPARISON` | Trace explicitly compares AI claims with original source text, data, or independently supplied evidence. | Requesting AI to “provide sources” alone → `V2`. |
| `V5_MULTIPLE_GROUNDS` | Both `V3` and `V4` are visible in the same window. | Not simply multiple prompts asking AI to self-check. |
| `VX_UNOBSERVABLE` | No usable post-response trace or observation channel for the relevant check. | Do not interpret as failure to verify. |

**Priority when multiple checks occur:** `V5` if source + reasoned critique; otherwise `V4` > `V3` > `V2` > `V1` > `V0`. If `C0`, choose `VX`. A writer can verify silently or in another tab; our code always means **visible verification**. Record the exact evidence in `evidence_note`.

---

## 7. Q5 — Observable uptake (`uptake`)

Uptake is the first relevant, *traceable* use or treatment of the AI response in the immediate window. Chat confirmation and editor incorporation are different kinds of evidence. Code one primary event; follow-up windows track the sequence.

| Code | Definition | Evidence needed |
|:--|:--|:--|
| `U1_EDITOR_DIRECT` | AI text pasted/inserted into editor with no substantive alteration in the window. | Linked editor event (usually `C2`). Does not imply a copied *idea* was unexamined. |
| `U2_EDITOR_SURFACE` | AI text inserted, then only lexical/grammar/style/format changes are visible. | Linked editor event and observable text comparison (`C2`). |
| `U3_EDITOR_SUBSTANTIVE` | Writer changes inserted/proposed content's claim, evidence, position, or inferential meaning. | Linked editor trace; explain the semantic difference (`C2`). |
| `U4_CHAT_ITERATE` | Next chat turn requests clarification, revisions, an alternative, justification, or further development of the same goal. | Subsequent chat (`C1` or `C2`). A follow-up is not by itself “human-led.” |
| `U5_CHAT_ACCEPT` | Writer explicitly says they accept/use the output, but insertion is not observed. | Explicit chat statement; **not** proof of actual editor paste. |
| `U6_REJECT` | Writer explicitly rejects the output/claim or produces a clearly incompatible alternative. | Clear negative decision, not simply no follow-up. |
| `U7_EDITOR_NEW_TEXT` | Trace shows independent/manual composition on the same goal without an attributable AI paste; relationship to AI ideas remains uncertain. | Editor trace; never infer origin from typing alone. |
| `UX_NO_TRACE` | No clearly relevant subsequent action is observable. | Default for `C0`/truncated follow-up. |

**Priority:** use the first causally/semantically linked uptake in the immediate window. If the first action is “Please revise this” followed by a new AI response, this window is `U4`; the next request–response window may later be `U1`, `U2`, or `U3`. For chat-only data, never assign `U1–U3` or `U7`. Substantial *manual* edits do not prove the ideas originated with the writer.

---

## 8. Worked coding examples (newly constructed; NOT data results)

These short examples are designed to exercise boundary rules. Their labels are proposed for pilot adjudication; they are not observations of NIRVANA or WildChat.

**E1 — Bibliography formatting (`C2`).** “Format this existing citation in ACM style.” AI formats it; the writer pastes it directly.  
Codes: `R/O15` · `F8_PROCEDURAL/REFERENCE` · `D0_NO_DECISION` · `V0_NONE_VISIBLE` · `U1_EDITOR_DIRECT`.

**E2 — Writer-specified claim (`C2`).** “My result applies only to first-year CS students. Improve grammar; preserve that limit.” AI rewrites it; writer makes wording-only edits.  
Codes: `R/O14` · `F5_TRANSFORM/PROSE` · `D1_HUMAN_GIVEN` · `V1_SURFACE_ONLY` · `U2_EDITOR_SURFACE`.

**E3 — Writer narrows an AI claim (`C1`).** “Give three thesis options.” The writer selects option two, but limits it to the observed sample because the evidence does not support generalization.  
Codes: `P/O08` · `F2_OPTIONS/CLAIM` · `D3_HUMAN_CHOSE_REVISED` · `V3_REASONED_CHALLENGE` · `U4_CHAT_ITERATE`.

**E4 — Complete essay inserted (`C2`).** “Write a full essay on this topic.” AI generates it; the same essay is pasted without substantive changes.  
Codes: `T/O10` · `F4_GENERATE/PROSE` · `D4_AI_PROPOSAL_TAKEN` · `V0_NONE_VISIBLE` · `U1_EDITOR_DIRECT`.

**E5 — Research gap without follow-up (`C0`).** “Compare papers A and B and identify a research gap.” AI proposes a gap; no later action is recorded.  
Codes: `P/O07` · `F4_GENERATE/EVIDENCE` · `D2_AI_PROPOSED_OPEN` · `VX_UNOBSERVABLE` · `UX_NO_TRACE`.

**E6 — Source-grounded challenge (`C1`).** “Summarize this study's findings.” AI makes an overly broad claim; the writer cites original source wording restricting the result and explains why the summary overgeneralizes.  
Codes: `P/O05` · `F1_EXPLAIN/SOURCE` · `D3_HUMAN_CHOSE_REVISED` · `V5_MULTIPLE_GROUNDS` · `U4_CHAT_ITERATE`.

**E7 — Asking the AI to check itself (`C1`).** “Is your claim definitely true? Please give references.” AI supplies references; writer asks for prose next, but shows no independent comparison.  
Codes: `R/O06` · `F7_FIND_CHECK/EVIDENCE` · `D2_AI_PROPOSED_OPEN` · `V2_AI_SELF_CHECK` · `U4_CHAT_ITERATE`.

**E8 — Chat-only acceptance (`C1`).** “Generate an outline for my essay.” AI provides one; writer says “I'll use this outline.” There is no editor trace.  
Codes: `P/O03` · `F3_PLAN/STRUCTURE` · `D4_AI_PROPOSAL_TAKEN` · `V0_NONE_VISIBLE` · `U5_CHAT_ACCEPT`.

**Adjudication notes:** E6 has `V5` only because it combines a source quotation **and** substantive reasoning about the source's scope; a pasted source without an explicit comparison may be `V4` at most. E7's `D2` is provisional if the writer merely asks for references and never adopts the claim. E4 makes the AI's text origin observable but says nothing definitive about private deliberation.

**Published-case orientation, not formal recoding:** The NIRVANA paper describes participant P54 as writing a draft first, then adopting AI-proposed elaboration, and P57 as receiving a full AI essay but not pasting it [8]. These examples underscore why *prompt type alone* is insufficient. We have **not** accessed and independently labeled their raw event streams in this reconstruction.

---

## 9. Full coding protocol (for a solo primary coder + LLM consistency check)

### 9.1 Before coding

1. Freeze this document as **v1.0**, recording any future change in the revision log. Avoid revising labels while silently retaining old annotations.
2. Select the sample with transparent screening: domain, session diversity, at least some `C1/C2` continuity. Keep NIRVANA and WildChat **separately identified**. The milestone plan specifies 50–100 windows; that is a proposed sample size, not a result already achieved.
3. Prepare a source record with `dataset`, `session_id`, `episode_id`, `turn_order`, request, response, next relevant action, evidence link/row IDs, and de-identified excerpts. Do not treat a synthetic case as empirical data.
4. Pilot ~8–12 genuine windows covering easy, ambiguous, and missing-follow-up cases. Note ambiguous rules; if labels change, issue v1.1 and recode the pilot. The historical 6+16 pilot cannot be asserted reproduced until the original files are recovered.

### 9.2 Per-unit annotation sequence

1. **Eligibility and coverage:** Is it writing-related? Set `domain` and `C0/C1/C2/CX`.
2. **Q1:** Read the *request* and immediate context; select one `process` and one `operation`. Use subsequent actions to resolve only genuine ambiguity.
3. **Q2:** From the request, select one `function` and one `object` (AI task, not outcome).
4. **Q3:** Locate a focal substantive decision. Record whether it was provided by the writer, proposed by AI, visibly selected/adopted, co-constructed, or unresolved.
5. **Q4:** Inspect available follow-up/editor trace for check type and its **grounds**; do not confuse AI self-justification with independent source checking.
6. **Q5:** Record the first relevant uptake event. `C0 → UX`; chat-only cannot support editor-based labels.
7. **Evidence and uncertainty:** Write a short anchored evidence note (the exact turn or event ID, or brief paraphrase), confidence, and boundary ambiguity.

### 9.3 Adjudication and boundary rules

- **Missingness outranks inference:** `C0 → VX + UX`. `C1` with no editor never implies a paste. `V0` requires usable post-response observation, though off-platform checks still remain possible.
- **Task vs output:** An AI response may exceed its request. Code Q2 from the **request**. In Q3/Q5, code any **substantive added choice** only if traceably observed.
- **Wording vs epistemic judgment:** An AI-written sentence can preserve a human decision (`D1`), or introduce a new one (`D2/D4`). Do not equate text-origin with claim-origin.
- **Checking vs changing:** Fixing grammar is `V1`; changing the conclusion with reasons is `V3`; comparing original paper text is `V4`/`V5`.
- **Acceptance vs silence:** Lack of objection is not acceptance. Use `D2`/`UX` when follow-up is absent.
- **Multi-label ambiguity:** Choose a primary code using the main request goal; leave a secondary note. If multiple codes repeatedly tie, revise definitions **between batches**, not ad hoc per case.
- **No moral verdict:** Never label an individual “lazy,” “deskilled,” “unaware” or “surrendered” as a factual diagnosis.

### 9.4 Reliability and versioning

- **Primary coder:** project author independently annotates the selected windows first; save a timestamped CSV before model assistance.
- **Second pass:** an LLM receives the **same evidence packet and frozen codebook**, with temperature/settings, prompt, model/version and date recorded. It must not see the primary coder's labels before its own first pass.
- **Report per field:** number of comparable windows, missing/uncertain proportions, raw percent agreement, Cohen's κ for *single-label* fields, and disagreements with rule updates. Consider prevalence and small-cell effects; κ is not guaranteed meaningful for rare categories.
- **Interpretation:** Human–LLM agreement is a **consistency/reproducibility check**, **not** human–human inter-rater reliability and **not** validation of inferred cognition. If large numbers of `DX/VX/UX`, report this coverage limit prominently.
- **Revision log:** v1.0 reconstructed before new pilot; v1.1 after fresh pilot (if needed); v2.0 after M2 disagreement review. Preserve label mapping between versions.

---

## 10. Dataset adapter — what each source supports

| Source | Strongest evidence available | Safe analyses | Not supported |
|:--|:--|:--|:--|
| **NIRVANA [8]** | 77 student essays; timestamped `gpt_inquiry`, `gpt_response`, editor operations and paste events. Published OSF dataset has `essay_num`, `op_index`, `time`, `op_loc`, `op_type`, `current_editor`, `add`, `delete`, `selected_text`, etc. | Q1–Q5 on well-linked windows; editing-based uptake; limited within-session transitions; essay-domain behavior. | Treating the 30-minute argumentative task as an actual multi-week research paper; interpreting private awareness from logs. |
| **WildChat [12]** | Public chat transcripts and subsequent user turns; identity, task setting, editor work and submitted artifact generally unknown. | Q1/Q2; Q3/Q4 when writer explicitly responds; `U4/U5/U6`; chat-level trajectories if multi-turn. | `U1/U2/U3/U7` editor codes; assuming all users are students or all prompts lead to actual submitted academic writing. |
| **ScholaWrite [2]** | Human-only scholarly keystroke edits with expert intention labels (15 classes), without chat/AI action pairing. | Derive/check activity vocabulary; contextualize how nonlinear scholarly writing proceeds. | AI delegation, writer–AI decision contribution or uptake in that dataset. |

**Actual NIRVANA event handling:** Group by `essay_num`; sort by `op_index` and check `time`; identify `op_type = gpt_inquiry` paired to `gpt_response`; collect until next inquiry/new goal or end of essay. Use `op_loc`, `add`, `delete`, `selected_text`, `current_editor`, and paste operations to verify attributed uptake. **A timestamp alone is not proof that a later edit was caused by a particular AI response.**

**Sample composition:** Count `unique sessions`, `unique participants` (NIRVANA), units by domain, mean windows per session, distribution of `C0/C1/C2`, and exclusions. Do not pool datasets without reporting their differences; a higher WildChat `UX` frequency may simply reflect lack of editor access.

---

## 11. From a static codebook to dynamic analysis (Milestone 2, not yet findings)

For **RQ1**, produce (a) writing operation × delegation function distribution, (b) decision × verification × uptake combinations among observable windows, and (c) a qualitative comparison of content-related versus mechanical work. Report **substitution-risk indicators**, not confirmed mental surrender. For example, `O08/O09 + F4 + D4 + V0 + U1` is a *candidate visible-risk configuration*, not a diagnosis; `O15 + F8 + D0 + U1` is often a lower-stakes mechanical delegation. These are **analytic hypotheses**, not predetermined types of people.

For **RQ2**, write an explicit **analytic detectability argument**: where could a writer encounter a discrepancy, what visible cues make the origin of a decision salient, and which fluent AI contributions might be misattributed to writer reasoning? Separate **possible opacity** from *measured awareness*. The available logs do not contain a validated moment-by-moment awareness measure.

For **RQ3**, explore possible **in-situ observable signals**: repeated AI-introduced claim adoption without visible challenge; repeated AI self-checks without source comparison; transition from AI generation to human evidence scrutiny; or surface-only edits after substantive AI drafting. Every signal needs false-positive caveats and contextual thresholds before it becomes a design recommendation.

Suggested figures: `operation × function` stacked counts; `decision × verification` heatmap; `uptake` by `evidence_scope`; and a **within-episode** transition matrix (e.g., `D4 → D3` across adjacent windows) only where linked multi-turn episodes exist. Use counts alongside percentages and avoid treating correlated windows from one participant as independent people.

**Primary analytic distinction:** Descriptive codes are observations; *patterns* are aggregate combinations discovered in data; educational/risk interpretations are a third step requiring argument. Never put your hoped-for Pattern A/B/C in the codebook as if it were observed.

---

## 12. Decision rules to review in the first real pilot

1. **Granularity:** Is `O04–O09` too fine for short NIRVANA essays? If many are empty, retain codes but report research/essay strata separately, or collapse families for presentation.
2. **Decision provenance:** Does `D4` require editor evidence or does an explicit chat “I'll use this claim” suffice? v1.0 accepts both but requires distinguishing uptake channel (`U1` vs `U5`).
3. **Verification:** How often can `V3` be distinguished from routine edits? Require a reason, contradiction or explicit standard.
4. **Window linkage:** When can a paste confidently be tied to one AI output? If ambiguous, use `UX` or low confidence, not forced attribution.
5. **Agreement:** If `D5` is rare or confusable, refine its requirement of two substantive contributions; don't collapse it into repeated prompts.
6. **External validity:** Are WildChat's verified research-writing cases numerous enough to make claims about that domain? Otherwise treat them as qualitative boundary examples and rely on NIRVANA for quantitative trajectories.

**What is ready today:** a reconstructed activity framework, the five operationalized questions, explicit evidence/missingness rules, an annotation protocol, a coding template, and illustrative test cases. **What is not done:** recovery of the original Mac codebook, fresh annotation of real raw windows, comparison statistics, evidence of the originally reported pilot, or empirical discovery of patterns. Those are next-stage work.

---

## References and source mapping

1. Flower, L., & Hayes, J. R. (1981). *A Cognitive Process Theory of Writing.* College Composition and Communication, 32(4), 365–387. https://eric.ed.gov/?id=EJ256235
2. Le, K. C., et al. (2026 version). *ScholaWrite: A Dataset of End-to-End Scholarly Writing Process.* arXiv:2502.02904. https://arxiv.org/html/2502.02904
3. Bereiter, C., & Scardamalia, M. (1987). *The Psychology of Written Composition.* https://eric.ed.gov/?id=ED279025
4. Zimmerman, B. J. (2002). *Becoming a Self-Regulated Learner: An Overview.* Theory Into Practice, 41(2). https://eric.ed.gov/?id=EJ656632
5. Risko, E. F., & Gilbert, S. J. (2016). *Cognitive Offloading.* Trends in Cognitive Sciences, 20(9), 676–688. https://doi.org/10.1016/j.tics.2016.07.002
6. Reza, M., et al. (2025). *Co-Writing with AI, on Human Terms: Aligning Research with User Demands Across the Writing Process.* arXiv:2504.12488. https://arxiv.org/html/2504.12488
7. Jelson, A., et al. (2026). *An Empirical Study to Understand How Students Use ChatGPT for Writing Essays.* CHI 2026 / arXiv:2501.10551. https://arxiv.org/html/2501.10551
8. Jelson, A., et al. (2026). *NIRVANA: A Comprehensive Dataset for Reproducing How Students Use Generative AI for Essay Writing.* arXiv:2604.07344. https://arxiv.org/html/2604.07344
9. Mysore, S., Das, D., Cao, H., & Sarrafzadeh, B. (2025). *Prototypical Human-AI Collaboration Behaviors from LLM-Assisted Writing in the Wild.* EMNLP 2025. https://aclanthology.org/2025.emnlp-main.852/
10. van Merriënboer, J. J. G., & Sweller, J. (2010). *Cognitive load theory in health professional education: Design principles and strategies.* Medical Education, 44, 85–93. https://doi.org/10.1111/j.1365-2923.2009.03498.x
11. Harvard College Writing Center. *A Source's Role in Your Paper.* https://usingsources.fas.harvard.edu/sources-role-your-paper
12. Zhao, W., et al. (2024). *WildChat: 1M ChatGPT Interaction Logs in the Wild.* ICLR. https://arxiv.org/abs/2405.01470
13. Peters, U., & Chin-Yee, B. (2025). *Generalization Bias in Large Language Model Summarization of Scientific Research.* Royal Society Open Science, 12, 241776. https://doi.org/10.1098/rsos.241776

### Research provenance notes

- `process` is adapted from Flower & Hayes, with monitoring explicit as in Reza et al.; `operation` is an original synthesis using ScholaWrite and research-writing needs.
- `function` draws on Reza's delegation strategies and the request-taxonomy approach of Jelson et al.; **our actual codes are newly defined**.
- `decision`, `verification`, `uptake` are **project-specific proposed operational categories**, grounded by research on ownership and interaction traces but **not validated by those papers**.
- NIRVANA dataset structure and event keys are sourced from its published Appendix A; ScholaWrite is a human-only activity anchor.
- The original proposal and Milestone 1 are project-level commitments, not independent evidence that this particular reconstructed coding scheme was previously pilot-tested.
