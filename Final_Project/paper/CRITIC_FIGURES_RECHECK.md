# Figure critic recheck

Independent recheck of the figures in `main.tex` and `main.pdf` at commit 856228d, against `CRITIC_FIGURES.md` (B1 to B9, M1 to M16). I edited nothing except this file. No dataset text is quoted here.

**Verdict: PASS.** 0 blocking problems, 4 minor problems. All 9 blocking and all 16 minor findings are fixed.

## 1. Per-finding table

| ID | Status | Is the fix correct? | Evidence |
|---|---|---|---|
| B1 | FIXED | Yes | Fig 11 caption, Section 4.7 and Section 7.3 all state the determinate denominator. Recomputed from `mine.load()`: precision 32/50, 44/75, 62/111, 40/73, 14/21 |
| B2 | FIXED | Yes | Caption definitions of both rules match `mining.md` s9 |
| B3 | FIXED | Yes | "528 request windows" is shaded and "Final codes" is dashed. Only the two top boxes are now plain, as the caption says |
| B4 | FIXED | Yes | Caption keeps the 3 capped conversations in the session measures and excludes only the 30 earlier windows |
| B5 | FIXED | Yes | Fig 3 wording now agrees with `report/narratives.md` s5 and with the code "none visible" |
| B6 | FIXED | Yes | Box reads 72 windows, 48 request-only, 21 behavior. Overlap sentence is in the caption, and `\Description` is updated. Rules recomputed: R16 48, R15 21 |
| B7 | FIXED | Yes | Lower-left corner is unshaded, and "Writer's text reworded" sits wholly in the blue area. `\Description` is updated |
| B8 | FIXED | Yes | `HATCH` covers SLr and NEU. On the greyscale pages the Fig 5 segments and Fig 6 tiles separate, including the 2 neutral and 5 surrender-leaning tiles of One-shot paste |
| B9 | FIXED | Yes | Figures row added; Analysis row now says "first versions". See section 4 |
| M1 | FIXED | Yes | Caption defines support share, unseen and the excluded sessions. Recomputed: 65 of 71 and 31 of 35 shown |
| M2 | FIXED | Yes | WildChat box prints C0 32, C1 119; matches the data |
| M3 | FIXED | Yes | 57 D0 windows, 53 neutral-mechanical |
| M4 | FIXED | Yes | Section 4.3 reworded; caption covers indeterminate |
| M5 | FIXED | Yes | yes and no labels and a dashed outline are present. See N4 for a side effect |
| M6 | FIXED | Yes | Caption gives 2 and 3, which match the unlabeled segments |
| M7 | FIXED | Partly | The dwell sentence is correct. The first-copy disclosure added with it gives the wrong population for two medians, see N1 |
| M8 | FIXED | Yes | Markers sized by count; caption states 58 of 71 and explains marker size |
| M9 | FIXED | Yes | Reference moved to "The gap is typing time" |
| M10 | FIXED | Yes | Fig 11 is on page 14, before the Section 5 heading |
| M11 | FIXED | Yes | Caption says "a chat-only window" |
| M12 | FIXED | Yes | Fig 1 uses the script fill, Fig 11 signals use `INK`, and `#444444` no longer appears in the script |
| M13 | FIXED | Yes | Exit 0 now; a scratch copy with hatching removed exits 1 |
| M14 | FIXED | Yes | Caption sentence added |
| M15 | FIXED | Yes | Median labels sit to the right of each strip, with a white background |
| M16 | FIXED | Yes | Section 3.7 carries the disclosure the critic offered as an alternative |

## 2. New and changed numbers

Recomputed from `mine.load()`, the results files and the codebook, using a scratch script outside the repository.

| Item | Result |
|---|---|
| Base rate | 98 of 248 = 39.5%; correct. 29 + 69 = 98 and 87 + 63 = 150 |
| Precision, either rule | 62 of 111 = 55.9%; recall 62 of 98 = 63.3%; behavior-based recall 48 of 69 = 69.6%; 140 fired. All correct |
| Fig 11 fired, precision, recall | 55, 64, 33; 101, 59, 45; 122, 55, 41; 23, 67, 14. All correct |
| Fig 11 rule definitions against `mining.md` s9 | All four match the table's "Fires when" text and `LOG_TRIGGERS` |
| Fig 11 rho | −0.41, −0.28, −0.11, −0.23 match s9 |
| D0 windows | 57, of which 53 neutral-mechanical (R02); correct |
| Request-only share zero | 58 of 71 sessions; correct |
| Draft requested, kept in chat | 72 windows: R16 48, R15 21, others 3; correct |
| Overlap with surface-only iteration | 22 windows; correct |
| Dwell n for D4, D3, D1 pasted windows | 21, 23, 20; medians 70.5, 288.1, 150.05; correct |
| Pasted windows and majority category | 42 and 39; 32 and 28; 29 and 28; correct |
| Other Fig 4 counts | 68 and 46; 52 and 37; 13 and 13; 46 and 37; 30 and 21; 32 and 30; indeterminate 103. All correct |
| First-copy medians in Fig 7 | 15.3, 17.2, 8.75 correct. The stated populations are not those of the medians, see N1 |
| Excluded sessions in Fig 9 | NIRVANA 6 with no surrender or support window; WildChat 3, plus 1 unsettled. Correct |
| Page count in `TODO_WAYNE.md` | 20 body, 27 total; matches the build |

The 11 figure PDFs and `figure_text.txt` were regenerated into a scratch folder and are byte-identical to the committed files.

## 3. Page review

Pages 5 to 14 were read in color and greyscale, and pages 19 and 20 for the AI Use Statement.

- **Overlaps and clipped text:** no text is clipped. The only collision is N4.
- **Float placement:** every figure is on or after the page of its first citation, and references appear in numeric order. No figure falls inside the wrong section.
- **Hatching legibility:** legible at print size in both modes, including the small Fig 6 tiles. The Fig 5 labels "48" and "5" stay readable on their backing boxes.
- **Color consistency:** one lapse, N3.
- **Captions standing alone:** all do, apart from N1 and N2 in Fig 7.

Checked, with no action needed:
- The white label backing in Fig 10 may cover at most a dot or two of the neighboring strip.
- The "support" bars in Fig 10 use the opposite hatch direction, with a legend, so they do not read as request-only.
- Section 4.5 says "no own work visible" for the sessions labeled "unseen" in Fig 9. That is literally true.

## 4. Checks and integrity

| Check | Result |
|---|---|
| `check_palette.py` | ok, exit 0. Worst pairs: normal 14.7, protan 11.4, deutan 13.4, tritan 12.8. Smallest unhatched greyscale gap 15.6 |
| `check_tex.py` | ok, exit 0. 11 figures, 3 tables |
| `spellcheck.py` | ok, exit 0. 2,066 distinct words, 2 allowlisted |
| `check_todos.py` | exit 0. 9 TODOs, 9 listed |
| `check_build.py` | ok, exit 0. **20 body pages (limit 20)**, 27 total, 0 overfull lines over 2 pt. The body ends about halfway down page 20, so the margin is about half a page |
| `check_supplement.py` | exit 0. 95 paths: 84 tracked, 11 local, 0 missing |
| AI Use Statement | True as it stands, including the Figures row. Six tables were replaced (`tab:triggers`, `data`, `framework`, `categories`, `archetypes`, `paste`), commits carry the Opus 5.5 attribution, the rerun and the palette and overlap checks were run, and this file is the recheck the row names |
| `Final_Project/report/M2_draft.md` | Untouched: no diff from e4c6ee1, and modified Nov 7 |
| `Reflection/` | Untouched since e4c6ee1: no commit since then changes it, and both modified files were last written on Nov 7, before that commit (Nov 8). `method_reflection.pdf` and `.txt` do differ from e4c6ee1 as uncommitted edits that predate this figure work and were already present at the start of this session |
| 8-word overlap (scratch script, logic from `check_no_text.py`; 499 source files, 1,202,598 source runs) | `main.tex` 0 of 14,031 runs; with LaTeX removed 0 of 12,420; `figure_text.txt` 0 of 1,099; joined across lines 0 of 1,099 |

## 5. New problems

No blocking problems. All four below are minor.

**N1. Fig 7 caption gives window counts that are not the counts behind two first-copy medians.** The caption gives 35, 45 and 52. Those are the sizes of the signatures in `mining.md` s7. The medians rest on the windows with a first copy: 35, 35 and 36.

**N2. Fig 7 typed labels use a different population from the dwell bars, and the new sentence hides this.** Typed medians use all pasted windows (42, 32, 29), while dwell uses 21, 23 and 20. On the dwell windows alone the typed medians are 14, 286 and 148, so the "typed 25 chars" label on the D1 bar is six times lower than its same-window value. The D4 against D3 contrast that the text relies on holds on both populations.

Fix for N1 and N2 together, replacing the last two sentences of the Fig 7 caption:

`Dwell uses the 21, 23 and 20 windows that have a next request; typed medians use all pasted windows in each row. First-copy times come from the matching code signatures, not only pasted windows (\code{D4} with \code{U1}, 35 windows with a first copy; \code{D3}, 35; \code{D1}, 36).`

**N3. Neutral-mechanical is cross-hatched in Figs 5 and 6 but plain in Fig 4.** In greyscale the plain box is close to the surrender-leaning boxes (L* 46.4 and 54.2).
Fix in `fig_concept`, replacing the final `box(...)` call:

```python
box(ax, 0.62, 0.56, 1.72, 0.56, "", fc=COL["NEU"], hatch=HATCH["NEU"], ec="white")
ax.text(0.62 + 0.86, 0.84, "No substantive decision\n(D0), 57 windows, 53 neutral-\nmechanical, outside both axes", ha="center", va="center", fontsize=7.1, color="white", linespacing=1.15, bbox=dict(fc=COL["NEU"], ec="none", pad=1.2))
```

In the caption, change "Hatching marks the signature that is mostly request-only surrender-leaning." to "Diagonal hatching marks the signature that is mostly request-only surrender-leaning, and cross-hatching marks neutral-mechanical, as in Figures 5 and 6."

**N4. Two small alignments in Fig 4.** The left edge of "Surface-only iteration" (x = 2.72) lies on the dashed surrender-leaning boundary (x = 2.71), a side effect of the M5 outline. The "no" label also sits left of the axis, while "yes" sits on it.
Fix in `fig_concept`: use `(2.80, 1.25, 1.42, 0.56, ...)` for the surface-only item, and draw "no" at x = 0.3 instead of 0.14.

After applying any of these, rebuild and rerun `check_build.py`, because the body is at the 20-page limit. Also add to the Figures row of the AI Use Statement that corrections made after the recheck were not rechecked, as the Editing row already does.
