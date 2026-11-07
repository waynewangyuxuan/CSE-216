# What the literature means for the codebook

**Recommendations only. Codebook v1.0 was not edited.** Bet 3 decides what to change, using these findings and the pilot.

**Evidence levels.** **Supported**: a source operationalizes something close. **Partly**: the idea appears, but not as a coded category, or only in a different domain. **Contradicted**: a source's finding cuts against the label as written. **Unsupported**: I found no source using it, which does not make it wrong. The codebook itself says Q3–Q5 are project-specific proposals, and this review confirms it: **no source validates `decision`, `verification` or `uptake` as a set.**

How sources were read is listed in `papers.csv` and marked in `related_work.md`.

## Summary of recommendations

| # | Recommendation | Priority | Why |
|---|---|---|---|
| 1 | Add `prior_own_work` | **High** | Four sources point to it, and it fixes the weakest pair in the comparison |
| 2 | Report Q3–Q5 as risk indicators, and do not assign "offloading" or "surrender" per window | **High, needs the user** | A log cannot show absence of deliberation, which is how Shaw & Nave define surrender |
| 3 | Add U4 subtypes, as secondary notes first | Medium | Mysore shows follow-ups differ, and `U4` lumps them |
| 4 | Treat `V3` as weak evidence; pilot whether `V5` is ever used | Medium | Tao finds justification can be superficial; `V5` may never occur |
| 5 | Compute text overlap by script for `U1`/`U2` | Medium | NIRVANA and Welzel do this, and it needs no judgment |
| 6 | Report operations as families | Medium | Chen's four layers support the cut already in `PACING.md` |
| 7 | Test `D5` strictly in the pilot, and be ready to cut it | Medium | No source supports it, and NIRVANA's "Collaborators" shows how the label misleads |
| 8 | Do not code AI correctness; state the limit | Low | Needs planted flaws or known answers |
| 9 | Credit related schemes rather than presenting Q1–Q5 as new | **High for M2** | Poquet, Chen and T. Kim overlap heavily |

## Q3: `decision`

| Label | Evidence | Assessment | Sources |
|---|---|---|---|
| Field as a whole | Who directs the work is coded by others, from prompts | **Partly** | Poquet 2026 codes active or passive by whether the learner specifies direction; Chen 2026 scores whether each layer stayed student-performed. Neither tracks a specific decision through later actions |
| `D0` no decision | Surface support may not displace argument construction | **Partly** | Chen 2026 §2.2. But see `O14`–`O15` below: "mechanical" depends on the assignment |
| `D1` human-given | Text origin and claim origin differ | **Partly** | NIRVANA notes the Human Contribution Ratio can miss whose ideas they are (§5); Poquet's active prompts include constraining how text is generated. No source separates them with this rule |
| `D2` AI proposed, open | Not observed as a category elsewhere | **Unsupported** | Follows from the codebook's missing-data rule. Keep |
| `D3` human chose or revised | Writers select or reject suggestions | **Partly** | Tao 2026 observes accept or reject on suggestions, but with planted flaws and an accept control |
| `D4` proposal taken | Adoption of AI ideas occurs, and can go unnoticed | **Supported**, with care | NIRVANA P54 and P26; Bhat 2026 finds suggested ideas seed writing while writers do not notice. So `D4` is observable, but a writer's own account would not confirm it |
| `D5` co-constructed | No scheme tests this. NIRVANA's Collaborators cluster shows the risk: P26 clusters there, yet on replay the student mainly edits | **Unsupported, and a caution** | NIRVANA §6.2; the `D5` caveat about repeated prompts is well founded. **Expect low agreement; keep the strict two-contribution rule, and cut if rare** |
| `DX` | Fits the literature's repeated warning | **Supported in spirit** | NIRVANA on P47: the extent of influence is hard to judge without examining the responses |

### Missing from Q3: prior own work

P54 and P26 are close in window codes but differ in whether the writer drafted first, and nothing in v1.0 records this. Four sources say it matters:

- NIRVANA's Drafters and its Human Edit Ratio capture drafting that the final text hides (§5, §7).
- Mallissery 2026's Reliance Index includes limited observable evidence of prior independent effort [repository; abstract only].
- Bhat 2026 reports that writers often do not finish their own ideation before engaging with suggestions [abstract only].
- Degen 2026 proposes "think before AI" as a phase [abstract only, weak source]. A registered plan by Q. Zhu et al. (doi:10.17605/osf.io/4u8ty) will test think-first use on creativity [abstract only; no results yet].

**Recommendation:** add `prior_own_work`: `VISIBLE_DRAFT`, `VISIBLE_PARTIAL`, `NONE_VISIBLE`, `UNOBSERVABLE`. It is codable in NIRVANA from the editor state, and in WildChat only when the writer pastes their own draft into the prompt. Absence must never mean "did no work", under the same rule as `V0`.

## Q4: `verification`

| Label | Evidence | Assessment | Sources |
|---|---|---|---|
| `V0` vs `VX` distinction | People may check outside the trace | **Supported** | NIRVANA says its metrics miss comprehending and deciding (§5); Lee 2025 describes verification against external sources, which a chat log may not show; Shaw & Nave need experimental control to infer it |
| `V1` surface only | Surface edits are observed; the conclusion is contested | **Supported** | Woo 2025, 15 edit types; NIRVANA P26. Note that the codebook's note that this does not establish content evaluation is exactly the P26 lesson |
| `V2` AI self-check | No study isolates this behavior | **Unsupported**, but sound in logic | The reasoning is that AI citations are not independent. Peters 2025 shows why models cannot be trusted on scope, without testing asking-the-AI as a behavior |
| `V3` reasoned challenge | Stated reasons can be shallow while still reducing bad adoption | **Partly contradicted** | Tao 2026: justification cut flawed adoption (65% to 41%), but its content looked superficial. So a stated reason shows engagement, not quality. **Do not read `V3` as strong evidence of real evaluation** |
| `V4` source comparison | Treated as central but burdensome | **Supported as a concept**; likely rare in logs | Lee 2025; Nogueira 2026; Wu 2026 [abstract only]. Report the base rate before treating it as a signal |
| `V5` both | No source | **Unsupported** | Likely too rare for κ. Pilot, then consider merging into `V4` for agreement statistics |
| Priority rule | No source | **Unsupported** | Keep; a project choice |

**Grading the grounds of a check is the project's most defensible addition** (see `framework_comparison.md`). So it is worth keeping even if `V4` and `V5` are rare, but report them honestly. If they barely occur, say so, because that is itself a finding about what logs can show.

**AI correctness.** Shaw & Nave and Tao can read uptake against known truth because they plant answers or flaws. The project cannot in general. I recommend no new required field. State in the method that `D4`+`V0` on a true claim and on a false one look identical in these codes. Optionally note visible AI error in `evidence_note` when source text is in the window.

## Q5: `uptake`

| Label | Evidence | Assessment | Sources |
|---|---|---|---|
| `U1` to `U3` editor uptake | Observable in traces | **Supported** | NIRVANA's copy-paste and edit metrics; Woo 2025; Welzel 2026 uses text overlap; Chen 2026 codes adoption from draft-revision records |
| `U2` vs `U3` boundary | Depends on semantic judgment | **Partly** | NIRVANA and Chen rely on human judgment or coded evidence here. Expect this to be the hard boundary |
| `U4` chat iterate | Follow-ups differ | **Partly contradicted as a single code** | Mysore 2025 finds distinct behaviors: revising intent, exploring, questioning, style, injecting content. `U4` merges all of them. WildChat windows will fall here heavily, so it may swamp the field |
| `U5` chat accept | Not found as a category | **Unsupported** | May be rare. Pilot |
| `U6` reject | Accept and reject are measured with an explicit choice | **Partly** | Tao 2026. Naturalistic rejection may be rare and indistinct from `U4` |
| `U7` new text | Writers can draw on AI without pasting | **Supported** | NIRVANA P47 and P57. The codebook's warning against inferring origin from typing is directly backed |
| `UX` | Fits | **Supported in spirit** | Codebook §10 on dataset limits |

**Recommendations:** (a) Add U4 subtypes as secondary notes first, and promote them only if the pilot shows agreement; suggested: `REVISE_REQUEST`, `NEW_CONTENT_SUPPLIED`, `QUESTION_OR_JUSTIFY`, `STYLE_ONLY`. These draw on Mysore's behaviors, though Mysore's own labels should be read before finalizing. (b) Compute overlap between AI text and later editor text by script for `U1` and `U2` in NIRVANA, and use the codes only for what overlap cannot settle. That follows Rule 1 in `PACING.md`.

## Q1 and Q2

| Point | Assessment | Sources |
|---|---|---|
| `process` from Flower & Hayes | **Supported** as common practice | Jelson 2026, Reza 2025, Wan 2024 all adapt it. Yukita 2025 argues delegation changes the process itself, to planning, waiting and reviewing [abstract only]. Worth a sentence in M2 |
| One primary `operation` per window | **Caution** | ScholaWrite finds most sessions multi-intentional; that is at session level, so it does not refute window-level labels but does warn of ties |
| 16 operations | **Supports the cut order** in `PACING.md` | Chen 2026's four layers (surface, structural, idea, reasoning) map onto families and are linked to outcomes. Suggest reporting at that grain, and citing it |
| Stakes differ by family | **Supported, associatively** | Chen 2026 finds idea and reasoning layers most negative for later no-AI thinking, with fragile significance; Reza 2025 finds academics prioritize ownership in planning. Supports §11's contrast of `O08`/`O09` and `O15` as hypotheses, not findings |
| `F1` explain vs `F4` generate | **Supported** | Contractor & Reyes 2026 separate tutor use from writing-for-me, with different outcomes [intro read]; Maier's levels; Bastani's hints vs answers. Evidence comes largely from non-research tasks |
| Who directs, as a missing Q2 axis | **Open question** | Poquet's active and passive cuts across `F`: "Write a 300-word synthesis" is passive, while constraining generation is active. `D1` partly covers this. Test in the pilot whether this adds anything to `F`+`D` |
| Mechanical work is low stakes | **Caution** | Risko & Gilbert (ms p. 14) tie benefit to the learning goal; §1.2 already says this. Keep it conditional: Bet 5 should not treat `O15` as harmless without saying why |

## Constructs and axes (codebook §1.2)

| Axis | Assessment | Sources |
|---|---|---|
| Load type: discuss only conditionally | **Supported** | Risko & Gilbert ms p. 14; Poquet 2026 argues cognitive load theory is limited for describing offloading; Poquet also finds no self-reported load differences across profiles, though the authors say the clusters are underpowered |
| Substitutability | **Partly** | Chen 2026 and Padmakumar 2026 both treat how much is handed over as a matter of degree |
| Developmental value | **Supported, conditional** | Bastani 2025; Maier 2026; Contractor & Reyes 2026. All non-research tasks |
| Detectability (RQ2) | **Partly, no direct test** | Bhat 2026; Skulmowski 2024; H. Kim 2026; Risko & Gilbert ms p. 10 on blurred knowledge boundaries; Shaw & Nave p. 18. These support the idea that influence can go unnoticed. None supports a label at the window level, consistent with RQ2 remaining analytic |

## The largest issue: what the framework can assign

The success criterion says the framework "assigns real interactions to these categories". Codebook v1.0 deliberately does not: it says `D2` is not surrender, and treats any risk configuration as a hypothesis (§11). The literature agrees with the codebook, and that creates a tension with the submitted wording.

- Shaw & Nave define surrender by absent deliberation (Table 2, p. 16), and the signature they use needs known AI accuracy. Mallissery 2026 builds a reliance measure and explicitly declines to say it establishes surrender [abstract only].
- Zhu 2026 needs self-report for the same split.

**Recommended reading, for the user to decide:** assign windows to **observable risk patterns**, and report how those patterns relate to the offloading and surrender concepts as an interpretive step, with agreement measured on the observable codes. This keeps the promise to code behavior, not cognition. It needs a plain statement in Milestone 2 that the criterion has been reinterpreted. T. Kim et al. 2025's two axes (division of labor and metacognitive oversight) could serve as a credited analytic map from Q2–Q3 and Q4 to these patterns [abstract only; conceptual paper].
