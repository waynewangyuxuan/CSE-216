# Framework comparison: Risko & Gilbert, Shaw & Nave, PAUSE, Maier, and this project

**Read this first.**

- The four frameworks were not built to label chat logs. A "Cannot" often means "not its job", not "a flaw".
- Every verdict is my application of a framework to a case. None of these authors applied their work to these cases.
- The project column describes what codebook v1.0 *should* do on paper. It has **not been tested on real windows**. Bet 3 and Bet 4 test it.
- I wrote the project's codes and I am rating them, so this table can favor the project. A separate critic agent read every cell and found that it did (`critic_report.md` D3–D8). Section 3 is the corrected version, and its remaining judgment calls are listed below it.

**Bottom line.** After an independent critic found the first version of this table favored the project, I re-rated it (section 3). Across 11 case pairs, the project is the only one of the five rated Yes on **3 pairs** (1, 2, 7). Two of those shrink at once:

- NIRVANA's own metrics already separate pairs 1 and 2, without any new framework.
- Pair 7 is built from the codebook's own worked examples, written to exercise those codes, so the project could not have failed it.

**That leaves one distinction that is not already done elsewhere: grading the grounds of a check (pair 7). It is unproven until real windows test it, and it may be rare.** The project cannot separate pairs 5, 8 and 11, does worse than an existing metric on pair 3, and pair 10 is outside its scope.

So the submitted success criterion, "distinguishes cases existing frameworks cannot", is **not established by this comparison**. See `REPORT.md`.

## 1. What each framework is

| | Risko & Gilbert 2016 | Shaw & Nave 2026 | PAUSE (Alam 2026) | Maier et al. 2026 | Project codebook v1.0 |
|---|---|---|---|---|---|
| **Kind** | Review and metacognitive theory | Theory plus 3 preregistered experiments | Self-reflection web tool | Preregistered experiment and a request classifier | Coding manual |
| **Scope** | Physical action that reduces cognitive demand, pre-LLM (ms p. 3) | Reasoning with AI on Cognitive Reflection Test items (pp. 18–19) | A person's self-reported use across four domains (§3.1) | Learners practicing fraction arithmetic with an LLM (Abstract) | One request, response and next action in writing (§2.2) |
| **Evidence** | Choice and consequences in lab tasks (Box 1) | Follow or override, accuracy, confidence (p. 20) | Likert items and two short probes (§3.5) | Highest support level requested per item; unaided test (§4.2.3) | Observable trace only (§2.3) |
| **Causal story** | Metacognitive evaluation drives offloading, which changes capacity and beliefs (pp. 11–13) | System 3 can displace or trigger deliberation (pp. 5, 17) | None claimed; pattern only (§6.3) | Request level associated with later performance; feedback causally reduces offloading (Discussion) | None claimed; risk configurations only (§11) |
| **Strong proposition** | Self-reinforcing drift away from internal ability (p. 13) | Accuracy tracks AI accuracy under surrender (p. 6) | None; author says it is not validated (§4.4) | Metacognitive feedback reduces answer offloading (Abstract) | None yet |
| **Read as** | Accepted manuscript, full | PsyArXiv preprint, through Study 1 plus limitations | arXiv preprint, relevant sections | arXiv preprint, relevant sections | Full |

## 2. "Offloading" does not mean the same thing across these sources

This matters because RQ1 pairs offloading with *supporting* thinking and surrender with *substituting* for it.

| Source | How "offloading" is used | Fits RQ1's pairing? |
|---|---|---|
| Risko & Gilbert (ms pp. 3, 12–14) | Physical action reducing demand, with both costs and benefits; neutral | Partly: not defined as support |
| Shaw & Nave (pp. 4, 16, 17) | Strategic delegation with internal reasoning still active; surrender is uncritical adoption | **Yes**, the closest match |
| PAUSE (Abstract, §1) | "AI-associated cognitive offloading" is routinely substituting LLM output for one's own reasoning; PAUSE places itself at the offloading end, where substitution is quiet (§2.1) | **No**: here offloading *is* the substitution |
| Maier (§1, §2) | Offloading can reduce practice; "answer offloading" is named as its negative form, against guided help | **No**: a form of offloading is the harm |
| Padmakumar 2026 (Intro) | Fraction of planning, execution and verification steps handed to AI; high scores may still be appropriate | Neither: offloading is a quantity |

So the literature does not back the pairing as a settled definition. It is one defensible stipulation, closest to Shaw & Nave. Shaw & Nave also define surrender by the absence of deliberation (Table 2, p. 16), which logs cannot show, and that is a further problem for the success criterion. See `REPORT.md`.

## 3. Case pairs

**Verdicts.**

- **Yes**: states a rule or criterion that separates the pair, whether or not anyone has tested it on this case.
- **Partly**: separates it only by extending the framework beyond what it states, or by indirect inference.
- **Cannot**: its unit fits the case, but it gives both the same treatment.
- **N/A**: the case is outside its unit of analysis or scope by design.

**Evidence tag on each Yes.** **[theory]**: stated as theory, with no tool or coding rule. **[tested]**: its own study applied it to such cases. **[untested]**: a stated rule or tool not yet evaluated on such cases, which includes all the project's codes.

**Cases.** P-numbers are real, published NIRVANA participants, as described in Jelson et al. 2026 (arXiv:2604.07344) §6. I read the paper's description, not their raw events, so **project codes on them are provisional**. Pairs 5, 8, 9 and 11 are constructed. **Pairs 6 and 7 use the codebook's own examples (§8), so the project passes them by construction.** Pair 10 is Maier's own example (Figure 1), which favors Maier in the same way.

| # | Pair | R&G 2016 | Shaw & Nave | PAUSE | Maier | Project v1.0 |
|---|---|---|---|---|---|---|
| 1 | **P77** pastes a generated essay (§6.2) vs **P57** requests a full essay, uses it as reference, does not paste (§6.2) | **N/A.** No interaction-level unit; both could begin as an extended strategy (ms pp. 3, 11–14) | **Partly.** Follow vs override (p. 20) is defined on items with a checkable answer; an essay needs extension | **N/A.** Person-level over two weeks (§1) | **Cannot.** Both are "complete answer"; only requests are classified (§4.2.3) | **Yes [untested].** `F4` for both; `U1` vs `U7` (§4, §7) |
| 2 | **P26** edits an AI draft lightly vs **P77** pastes with no edits (§6.2) | **N/A** (ms pp. 3, 11–14) | **Cannot.** Both fit uncritical adoption; surface edits are not a route in Table 2 (p. 16) | **N/A** (§1) | **Cannot.** Same request level (§4.2.3) | **Yes [untested].** `U2`/`V1` vs `U1`/`V0` (§6, §7). A thin gain: the paper still reads P26 as concerning, and `U2` makes no such judgment |
| 3 | **P54** drafts alone first, then adopts AI content that replaces the draft vs **P26** starts from an AI draft (§6.2) | **N/A** (ms pp. 3, 11–14) | **Partly.** Hybrid routes exist, with no measure (p. 16) | **N/A** (§1) | **Cannot.** Requests only (§4.2.3) | **Partly.** Window codes nearly match (`D4`, then `U1` or `U2`). Only linked episodes show the earlier draft (§2.2), and no field records it |
| 4 | **P47** draws ideas from an AI reply, then writes alone (§6) vs **P30** only asks about grammar and vocabulary (§6.2) | **N/A** (ms pp. 3, 11–14) | **Cannot.** Neither "follows" an answer in a checkable way (p. 20) | **N/A** (§1) | **Partly.** Request levels differ, but the scale was built for arithmetic (§4.2.3) | **Partly.** `F` and `O` separate the requests; uptake is `U7` for both, and §7 forbids inferring idea origin from typing |
| 5 | Writer pastes an AI claim **after checking the source in another tab** vs **without checking** (constructed) | **N/A** (ms pp. 3, 11–14) | **Partly.** Only by inference, in aggregate, when AI accuracy is known (pp. 18–19) | **Partly.** It can ask the person, as a self-report habit (items B1, B5, Appendix A) | **Cannot.** Not observed (§4.2.3) | **Cannot.** Both `V0`, by design (§6) |
| 6 | Writer supplies a scoped claim and AI rewords it (codebook E2) vs AI generates the claim, which is adopted (codebook E4) | **N/A** (ms pp. 3, 11–14) | **Yes [theory].** Delegation with own reasoning active vs adopting a generated answer (pp. 4, 16, 17). No trace measure | **N/A** (§1) | **Partly.** Its numeric check separates a new value from one the participant produced (§4.2.3); arithmetic only | **Yes [untested].** `D1`+`F5` vs `D4`+`F4` (§4, §5) |
| 7 | Writer cites source text against a summary (codebook E6) vs asks the AI to check itself (codebook E7) | **N/A** (ms pp. 3, 11–14) | **Partly.** Names verify-then-adopt (p. 16); no grading of grounds | **Partly.** Self-reported habit of checking against a source (item B1, Appendix A), not this interaction | **Cannot** (§4.2.3) | **Yes [untested].** `V4`/`V5` vs `V2` (§6). May be rare; unknown until piloted |
| 8 | Writer adopts a **true** vs a **false** AI claim (constructed) | **N/A** (ms pp. 3, 11–14) | **Yes [tested, in aggregate].** This is its core design (pp. 18–19) | **N/A.** Its probe tests a separate claim (§3.5) | **Cannot.** Rewards and levels ignore this (§4.2.3) | **Cannot.** No field records AI correctness (§5–§7) |
| 9 | Same request when the work **is** the learning goal vs routine work (constructed) | **Yes [theory].** Benefit depends on whether the demand is needed for the learning goal (ms p. 14) | **Cannot.** Its point about adaptive deferral concerns statistically superior systems, not learning goals (p. 18) | **Partly.** Targets effort a person may want to retain (§1), by their own view | **Cannot.** Studies learning only, so has no rule separating the two (Abstract) | **Partly.** Discussed in §1.2 as interpretive, stratified by `domain`; never coded per window |
| 10 | "How do I start?" vs "Give me the answer." on one practice item (Maier's own example, Figure 1) | **N/A** (ms pp. 3, 11–14) | **Cannot.** Follow or override comes after the output (p. 20) | **N/A** (§1) | **Yes [tested].** Guided help vs complete answer, with a frozen classifier evaluated on 198 synthetic held-out dialogues (§4.2.3) | **N/A.** A non-writing request is out of scope (§2.1). For a writing analogue, `F3` or `F1` vs `F4` (§4) would add nothing to Maier |
| 11 | One-off use vs a habit over weeks (constructed) | **Yes [theory].** Drift prediction (ms p. 13) | **Partly.** Theory names long-run reanchoring (Table 2, p. 16); authors call their studies a snapshot (pp. 48–49) | **Yes [untested].** Two-week self-report; the author says it is not validated (§1, §4.4) | **Cannot.** Single brief session (Limitations) | **Cannot.** NIRVANA is 30 minutes; WildChat has no verified identity (§10) |

### Count of verdicts

| | Yes | of which tested | Partly | Cannot | N/A |
|---|---|---|---|---|---|
| Risko & Gilbert | 2 | 0 | 0 | 0 | 9 |
| Shaw & Nave | 2 | 1 | 5 | 4 | 0 |
| PAUSE | 1 | 0 | 3 | 0 | 7 |
| Maier | 1 | 1 | 2 | 8 | 0 |
| Project v1.0 | 4 | 0 | 3 | 3 | 1 |

Do not read this as a score. I chose the pairs for a comparison about interaction-level coding, the project's own home ground, and the project was designed after these frameworks were known. Pairs chosen around learning or long-term change would rank Maier, Risko & Gilbert and PAUSE higher. **Only two Yes verdicts in the whole table have been tested on such cases, and neither belongs to the project.**

**Judgment calls that remain.** Reasonable readers could differ on Shaw pair 5 (I rate Partly because it infers checking indirectly, while pair 8 is what the design manipulates) and on whether Risko & Gilbert belong under Cannot rather than N/A. I chose N/A because a pre-LLM theory of strategy choice has no interaction-level unit.

## 4. Where the project adds nothing

1. **Pair 10.** Maier already separates request levels, with a tested tool, and the case is out of the project's scope.
2. **Pairs 1, 2 and 3.** NIRVANA's Human Contribution and Human Edit Ratios already reflect paste vs no paste, and they cluster P26 and P77 apart. On pair 3 the Edit Ratio does better than the window codes. These come free with the dataset. The caveat is that the authors show the clusters can mislead (P26), so the codes may still help interpretation.
3. **Pair 6.** Shaw & Nave state this distinction, and Poquet 2026 codes something close from prompts.
4. **Pairs 5 and 8.** Silent checking and AI correctness are not visible to the codes. Shaw & Nave's experimental control gets at both in aggregate, and the project cannot do so on observational data.
5. **Pair 11.** PAUSE and Risko & Gilbert speak to habit and drift. The project's data cannot.
6. **Causal claims.** Bastani 2025 and Maier 2026 connect behavior to later unaided performance. The project promised not to measure skill change, so its risk readings stay borrowed.
7. **Work outside the four narrows the claim further.** The assignment names four frameworks, but Milestone 2 should not imply these are the only rivals. The forward search and the seed list turned up:

| Paper | What it already separates | Effect on the project's claim | How read |
|---|---|---|---|
| Poquet et al. 2026 (arXiv:2606.10434) | Prompts coded as active or passive by who directs the work, and as local or global; 97 students in synthesis writing; compared to essay authorship | **Closest rival.** Comes near pair 6 and Q2. Reports expert-LLM kappas of 0.64 and 0.61 on this coding. It does not code checks or uptake the way the project does | Relevant sections |
| Chen 2026 (doi:10.3389/fpsyg.2026.1906199) | Surface, structural, idea and reasoning offloading, from coded interaction and revision evidence; later no-AI outcomes | Comes near the project's `object` and `operation` fields, and links them to outcomes, which the project cannot do. Only six classes, so the author treats significance as fragile | Abstract, method sections |
| Zhu et al. 2026 (doi:10.3389/fpsyg.2026.1878629) | Dependent vs autonomous offloading: substitute or scaffold | **Same conceptual split as RQ1**, measured by self-report over three waves, with no trace data. All outcomes are perceived, as the authors stress | Abstract, limitations |
| T. Kim et al. 2025 (doi:10.1002/arcp.70008) | Division of cognitive labor vs metacognitive oversight, giving four patterns including Cognitive Surrender | A conceptual two-axis map close to the project's Q2–Q4. No coding or data | Abstract only |
| Padmakumar et al. 2026 (arXiv:2605.29392) | Share of planning, execution and verification steps handed over, by counterfactual workflow | A quantitative alternative. Validated with 40 developers on programming, not writing | Relevant sections |
| Hossain & Nawmi 2026 (arXiv:2607.14301) | Strategic, Instrumental, Dependent and Dialogic reliance in academic writing | A validated survey scale for types of reliance, including a Critical Evaluation facet. Self-report, not traces | Abstract and construct section |
| Contractor & Reyes 2026 (arXiv:2607.08849) | Augmentation vs automation, classified from conversation logs, linked to unaided essays a week later | Log-based split **with** a learning outcome | Abstract and introduction |
| Tao et al. 2026 (arXiv:2609.23936) | Adoption of flawed vs sound suggestions in a writing task | **Does pair 8 for writing**, by planting flaws. The project cannot | Abstract, method sections |

Pair 7, grading the grounds of a check from traces, is the most defensible remaining gain, and it is the least proven because such checks may be rare.

## 5. What the project plausibly does add

These are predictions on paper, not findings, and the first two are the only ones not already done somewhere.

- **Grading the grounds of a check** (pair 7), rather than only whether one occurred. Self-set so far; it needs real cases, and Bet 3 should look for them.
- **Coding request, decision, check and uptake together in one window**, where a single scale would merge them. I found no scheme doing all four, but the search was bounded. Maier's own limitation points to the need: their design makes offloading an explicit choice and may not generalize to assistants that give full answers unasked (Limitations).
- **Separating text origin from claim origin across later uptake** (pair 6). Poquet 2026 and Chen 2026 come close, so the gain lies in combining this with uptake, not in the distinction itself.
- **Refusing to convert missing evidence into a verdict** (`VX`, `UX`, `C0`). None of the four needed this, because none of them codes logs with missing follow-up. This is careful method, not a new distinction.

## 6. Limits of this comparison

- **Cells for R&G rest on the accepted manuscript**, so page numbers are manuscript pages.
- **Shaw & Nave, Maier and PAUSE were read by relevant sections**, not line by line. Cells cite those sections.
- **Hornbæk & Oulasvirta's scope, causality and proposition questions shaped section 1, from the abstract only.**
- **The P-cases come from a short published paragraph each.** Real coding could change the project codes.
- **NIRVANA is an essay task, not research writing.** No real research-writing case appears here, because verified WildChat candidates are Bet 1's output.
