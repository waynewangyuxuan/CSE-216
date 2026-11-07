# Round 3 coder brief

You are coding real windows with codebook v1.1-rc2. Read the whole codebook first: `Final_Project/codebook/CSE216_Research_Writing_Codebook_v1.1.md`.
Then code each line of the view file. Read only those two files. Do not open anything else in `Final_Project/` or `.wayne/`, and do not look for other coders' files: your labels must be independent.

Each view line holds: `window_id`, `dataset`, `coverage` (given, do not recode), `turn_order`, `prior_turns` (up to 3 earlier exchanges, each cut to 500 characters), `editor_before_request` (NIRVANA only), `request`, `response`, `next_actions_text` (what happened after the response; "NEXT REQUEST TO AI" or "NEXT USER TURN" is the writer's next chat turn). Long text is marked where it was cut.

Apply the rules as written. When a rule is hard to apply, pick your best label and say so in `flag_field` and `flag_note`. Do not code whether the AI's answer is correct. Do not use outside knowledge of the dataset.

## Output

One JSON object per line, one per window, keys: `window_id`, `domain`, `prior_own_work`, `operation`, `function`, `object`, `decision`, `verification`, `uptake`, `confidence`, `u4_subtype` (only when `uptake` is `U4`, else empty), `evidence_note` (one short paraphrased sentence), `flag_field`, `flag_note`. Use the code values exactly as in the codebook's tables, in full form such as `D2_AI_PROPOSED_OPEN`, `V0_NONE_VISIBLE`, `U8_MOVED_ON`, `F5_TRANSFORM`.

Validate your file by parsing every line and checking the count before you finish. Final message: the count written and the 3 rules you found hardest. No labels in it.

## Second file: constructed cases

After the windows, code `vignettes.jsonl` in the same way and write `vignette_labels.jsonl` beside your labels file. These short cases are constructed, not real data. Same keys. `prior_turns` may be empty, and `editor_before_request` may be absent.
