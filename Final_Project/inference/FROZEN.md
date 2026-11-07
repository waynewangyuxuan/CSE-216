# Frozen: codebook v1.2 inference layer

**Current freeze (freeze 2)**, Nov 7, 2026, in the commit that changes this paragraph. Do not change either file below. A change needs v1.3 and a logged rerun.

- `scripts/apply_rules.py` sha256 95ca331603b27eeacc1e4c275a5adb23199238606e1832011b70370fdeb46ac1
- `CSE216_Writing_Codebook_v1.2.md` sha256 de6663da55fa9385a81e5b8d576fb3a337b00b2efd07721b05767f6ac65b6a5f

`scripts/check.py` fails if `apply_rules.py` no longer matches the first hash above.

**Freeze 1 (superseded)** was commit 771ebf3 (`apply_rules.py` sha256 prefix 48d4cd9d, recorded in that commit's FROZEN.md). The gate critic found wording errors in §9 and two logic gaps: a dead `U3` clause in R07, and v1.1-forbidden code combinations getting real categories. They were fixed and re-frozen **before any Bet 6–7 label was read by this bet**, as freeze 1 also was. Categories on the 100 calibration windows are identical under both freezes. The changes are in `decisions.tsv`.

## Freeze came before any Bet 6–7 label was read

- No file under `Final_Project/sessions/` or `Final_Project/wildchat/` was opened by this bet or by its three review agents (their briefs forbid it).
- One exposure, file names only: commit ff704c6 (this bet's first checkpoint) swept in 27 `Final_Project/wildchat/` files that Bet 7 had staged in the shared index. The commit printed their names and line counts. Their contents were not opened. The parent session checked them and found ids, hashes, labels and scripts only.
- The rules were not shared with Bet 6–7 coders.
- Commits touching those folders when this freeze was made (git order is the record):

```
66fdc21 Save both coders' labels for all 347 NIRVANA windows and the transcript audit
ff704c6 Draft inference rules from opened sources, before calibration review
8f9dec9 Set up whole-session coding of NIRVANA: rules, part builder, label gate
c00b797 Freeze the WildChat writing definition before screening
```
