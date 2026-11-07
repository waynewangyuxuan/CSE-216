# Frozen: codebook v1.2 inference layer

Frozen Nov 7, 2026, in the commit that adds this file. Do not change either file below. A change needs v1.3 and a logged rerun.

- `scripts/apply_rules.py` sha256 48d4cd9de0dc6806431d54b58cd98fa7c6943fbfc0afce44048ebc02ffb4d90d
- `CSE216_Writing_Codebook_v1.2.md` sha256 2ad2fe39b04a67a65e794a013c303dc503ec233397a5cfdcecea0fd5357d80a9

`scripts/check.py` fails if `apply_rules.py` no longer matches the hash above.

## Freeze came before any Bet 6–7 label was read

- No file under `Final_Project/sessions/` or `Final_Project/wildchat/` was opened by this bet or by its three review agents (their briefs forbid it).
- One exposure, file names only: commit ff704c6 (this bet's first checkpoint) swept in 28 `Final_Project/wildchat/` files that Bet 7 had staged in the shared index. The commit printed their names and line counts. Their contents were not opened. The parent session checked them and found ids, hashes, labels and scripts only.
- The rules were not shared with Bet 6–7 coders.
- Commits touching those folders when this freeze was made (git order is the record):

```
66fdc21 Save both coders' labels for all 347 NIRVANA windows and the transcript audit
ff704c6 Draft inference rules from opened sources, before calibration review
8f9dec9 Set up whole-session coding of NIRVANA: rules, part builder, label gate
c00b797 Freeze the WildChat writing definition before screening
```
