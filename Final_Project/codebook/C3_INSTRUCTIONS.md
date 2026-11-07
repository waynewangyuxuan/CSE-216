# C3: blind-code the 20 gold windows

**Time: about 90 minutes to 2 hours, not the 1 hour in the plan.** The windows hold about 13,700 words on the page, or about 50 minutes of reading if you read it all, and you also need the codebook and the coding itself. To save time, skim long AI responses for their main claims, and read the request and "What happened next" closely. Earlier turns and the editor are folded, so open them when you need them. You can split this across two sittings. **This cannot be delegated.** Your labels are the only human check on the AI coders, and they must be your own.

## Rules

- Do not open `data/gold.csv`, `data/sample.csv`, `data/windows.jsonl`, `codebook/pilot/`, `codebook/pilot_results/`, `codebook/decisions.tsv`, `codebook/REPORT_AFTER_C3.md` or `.wayne/bets/0004-codebook-pilot-freeze/` until your sheet is saved. Do not ask an AI about a window.
- The sheet and page hold no AI labels. Keep it that way until you have saved your sheet.
- Do not reread or discuss the window after you have coded it, and don't change the IDs.
- A hard window is useful. Pick your best code and say what was hard in `flag_note`.

## Steps

1. Open `CSE216_Research_Writing_Codebook_v1.1.md`. Read sections 1–8 (about 20 minutes).
2. Open `c3_gold_windows.html` in a browser. It shows each window: earlier turns, the editor (NIRVANA), the request, the AI response, what happened next.
3. Open `c3_gold_sheet.csv` in a spreadsheet. Fill one row per window, in order. Save as CSV under the same name, since only that name is kept out of git.
4. Check the sheet. Fix any `PROBLEM` it names. A `REREAD` line asks you to check a rule, and you may keep your code:

```bash
cd /Users/wang/CSE-216/Final_Project/codebook/scripts && ../../data/raw/_venv/bin/python check_c3.py
```

## Columns

Copy each code exactly. `coverage` is given.

| Column | Codes (full names in the codebook) |
|---|---|
| `domain` | `ESSAY_TASK` for NIRVANA. Otherwise `RESEARCH_EXPLICIT`, `ACADEMIC_STATED`, `OTHER_WRITING`, `DOMAIN_UNKNOWN` |
| `prior_own_work` | `VISIBLE_DRAFT`, `VISIBLE_PARTIAL`, `NONE_VISIBLE` (NIRVANA only), `UNOBSERVABLE` (WildChat only) |
| `operation` | `O01`–`O16`, `OX` |
| `function` | `F1_EXPLAIN`, `F2_OPTIONS`, `F3_PLAN`, `F4_GENERATE`, `F5_TRANSFORM`, `F6_CRITIQUE`, `F7_FIND_CHECK`, `F8_PROCEDURAL`, `FX_OTHER` |
| `object` | `IDEA`, `SOURCE`, `EVIDENCE`, `CLAIM`, `ARGUMENT`, `STRUCTURE`, `PROSE`, `REFERENCE`, `PROCESS`, `OTHER` |
| `decision` | `D0_NO_DECISION`, `D1_HUMAN_GIVEN`, `D2_AI_PROPOSED_OPEN`, `D3_HUMAN_CHOSE_REVISED`, `D4_AI_PROPOSAL_TAKEN`, `DX_INDETERMINATE` |
| `verification` | `V0_NONE_VISIBLE`, `V1_SURFACE_ONLY`, `V2_AI_SELF_CHECK`, `V3_REASONED_CHALLENGE`, `V4_SOURCE_COMPARISON`, `VX_UNOBSERVABLE` |
| `uptake` | `U1_EDITOR_DIRECT`, `U2_EDITOR_SURFACE`, `U3_EDITOR_SUBSTANTIVE`, `U4_CHAT_ITERATE`, `U5_CHAT_ACCEPT`, `U6_REJECT`, `U7_EDITOR_NEW_TEXT`, `U8_MOVED_ON`, `UX_NO_TRACE` |
| `confidence` | `HIGH` (explicit direct evidence), `MEDIUM` (coherent but partial trace), `LOW` (ambiguous) |
| `is_research_writing` | **WildChat windows only (6): `yes` or `no`.** Is this truly research writing, meaning a paper, thesis, literature review, methods or research question? Judge from the window only. NIRVANA rows stay `NA` |
| `evidence_note` | One short sentence on what you saw. Required |
| `flag_note` | What was hard, if anything |

## Quick reminders

- **Decision:** is a substantive choice in play? Is the content mostly the writer's (`D1`) or new or from the AI? If AI-origin, the next action decides: said yes, or half or more reused verbatim, is `D4`; selected, rejected, under half pasted, or changed is `D3`; otherwise `D2`. Typed text that only echoes the AI is `D2`. A summary or analysis of supplied material counts as AI-origin.
- **Verification:** only the next action counts. A challenge inside this request belongs to the previous window. Silent content edits are uptake, not `V3`.
- **Uptake:** `U4` touches this output. `U8` is a next turn that doesn't. `UX` is no trace at all.
- **Coverage limits:** `C0` means `VX` and `UX`. `C1` never takes `U1`, `U2`, `U3` or `U7`.
- **Not a judgment on the writer.** You are coding what the trace shows, not what anyone thought. Do not code whether the AI was right.

When the check passes, keep a copy of the sheet somewhere safe, since it is not in git. Then tell the agent session that the sheet is saved. Bet 4 compares your labels with the AI coders' only after that.
