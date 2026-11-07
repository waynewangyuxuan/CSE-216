# Round 1 coder brief

You are coding real windows with codebook v1.0. Read the whole codebook first: `Final_Project/CSE216_Research_Writing_Codebook_v1.0.md`.
Then code each line of the view file. Read only those two files. Do not open anything else in `Final_Project/` or `.wayne/`, and do not look for other coders' files: your labels must be independent.

Each view line holds: `window_id`, `dataset`, `coverage` (already computed: use it, do not recode), `turn_order`, `prior_turns` (up to 3 earlier exchanges, each cut to 500 characters, for context), `editor_before_request` (NIRVANA only, the essay editor just before this request), `request`, `response`, `next_actions_text` (what happened after the response, up to the next request; "NEXT REQUEST TO AI" or "NEXT USER TURN" is the writer's next chat turn). Long text is marked where it was cut.

Code the focal window only. Apply the rules as written, even if you dislike them. When a rule is hard to apply, pick your best label and say so in `flag_field` and `flag_note`. Those flags are the main point of this round. Do not use outside knowledge of the dataset.

## Output

One JSON object per line in your output file, one per window, all windows, these keys:

| Key | Values |
|---|---|
| `window_id` | as given |
| `domain` | `RESEARCH_EXPLICIT`, `ACADEMIC_STATED`, `ESSAY_TASK`, `OTHER_WRITING`, `DOMAIN_UNKNOWN` (NIRVANA is always `ESSAY_TASK`) |
| `process` | `P`, `T`, `R`, `M`, `PX` |
| `operation` | `O01`...`O16`, `OX` |
| `function` | `F1_EXPLAIN`, `F2_OPTIONS`, `F3_PLAN`, `F4_GENERATE`, `F5_TRANSFORM`, `F6_CRITIQUE`, `F7_FIND_CHECK`, `F8_PROCEDURAL`, `FX_OTHER` |
| `object` | `IDEA`, `SOURCE`, `EVIDENCE`, `CLAIM`, `ARGUMENT`, `STRUCTURE`, `PROSE`, `REFERENCE`, `PROCESS`, `OTHER` |
| `decision` | `D0_NO_DECISION`, `D1_HUMAN_GIVEN`, `D2_AI_PROPOSED_OPEN`, `D3_HUMAN_CHOSE_REVISED`, `D4_AI_PROPOSAL_TAKEN`, `D5_CO_CONSTRUCTED`, `DX_INDETERMINATE` |
| `verification` | `V0_NONE_VISIBLE`, `V1_SURFACE_ONLY`, `V2_AI_SELF_CHECK`, `V3_REASONED_CHALLENGE`, `V4_SOURCE_COMPARISON`, `V5_MULTIPLE_GROUNDS`, `VX_UNOBSERVABLE` |
| `uptake` | `U1_EDITOR_DIRECT`, `U2_EDITOR_SURFACE`, `U3_EDITOR_SUBSTANTIVE`, `U4_CHAT_ITERATE`, `U5_CHAT_ACCEPT`, `U6_REJECT`, `U7_EDITOR_NEW_TEXT`, `UX_NO_TRACE` |
| `confidence` | `HIGH`, `MEDIUM`, `LOW` |
| `prior_own_work` | **Trial field, not in v1.0.** Own work by the writer on this goal that is visible before this request. `VISIBLE_DRAFT` (running text the writer wrote), `VISIBLE_PARTIAL` (notes, fragments, a sketch, or a stated position), `NONE_VISIBLE` (the channel exists and shows none), `UNOBSERVABLE` (the channel cannot show it). Text pasted from the AI is not own work. Absence never means no work was done |
| `u4_subtype` | **Trial note, not in v1.0.** Only when `uptake` is `U4`, else empty. `RESTATE_OR_ELABORATE`, `QUESTION`, `MORE_OUTPUTS`, `STYLE`, `ADD_OR_REMOVE_CONTENT`, `OTHER` |
| `evidence_note` | one short sentence, paraphrase, no long quotes |
| `flag_field` | the field a rule was hard to apply on, else empty |
| `flag_note` | what was hard and why, else empty |

Do not code whether the AI's answer is correct. Validate your file by parsing every line as JSON and checking the count before you finish. Your final message: the count written and the 3 rules you found hardest. Do not include labels in it.
