# Proofreading report: main.tex

## Spell-check output

Command: `python3 /Users/wang/CSE-216/Final_Project/paper/scripts/spellcheck.py` (exit 0)

```
checked 1955 distinct words with macOS NSSpellChecker; 2 allowlisted
spellcheck: ok
```

## Status by category

1. Spelling and typos: no misspelled words; 2 hyphenation variants (rows 1-2).
2. Grammar, missing or doubled words, a/an, agreement, broken sentences: 5 findings (rows 3-7). Doubled words: none. Wrong a/an: none. Subject-verb disagreement: none.
3. Punctuation and LaTeX text-level errors: 4 findings (rows 8-11). Wrong quotes: none. Unescaped `%`: none.
4. Inconsistent terms: 9 findings (rows 12-20). WildChat, NIRVANA and surrender-leaning spellings and capitalization: none.
5. Sentences a reader cannot parse: 4 findings (rows 21-24).
6. Outside main.tex, printed in the reference list: 1 finding (row 25).

Author names: every name typed in the prose (Maier, Zhu, T. Kim, Yang, Poquet, Chen, Mysore, Tao, Reza, Risko and Gilbert, Shaw and Nave, Bastani; initials C&R, S&N, R&G) matches refs.bib. Mismatches: none. Every `\cite` key exists in refs.bib.

## Findings

| # | Line | Exact current text | Exact proposed fix | Reason |
|---|------|--------------------|--------------------|--------|
| 1 | 90 | `read second-hand through work` | `read secondhand through work` | Spelling: American dictionaries give the closed form. |
| 2 | 398 | `The over-representation of` | `The overrepresentation of` | Spelling: American dictionaries give the closed form. |
| 3 | 319 | `after a median 57.8 seconds` | `after a median of 57.8 seconds` | Grammar: missing "of". |
| 4 | 321 | `comes after a median 15.5 seconds` | `comes after a median of 15.5 seconds` | Grammar: missing "of". |
| 5 | 678 | `the writer types own sentences` | `the writer types their own sentences` | Grammar: missing determiner. |
| 6 | 261 | `and then one paste of 4,681 characters` | `and then the writer makes one paste of 4,681 characters` | Grammar: the last item of the sentence has no verb and does not attach to the "while" clause. |
| 7 | 457 | `These claims rest on AI-coded logs from two datasets, stated plainly as inferences from behavior.` | `These claims, stated plainly as inferences from behavior, rest on AI-coded logs from two datasets.` | Grammar: misplaced modifier; "stated" attaches to "datasets" but means "claims". |
| 8 | 387 | `Two models can share a bias and a shared set of rules` | `Two models can share a bias, and a shared set of rules` | Punctuation: comma needed between independent clauses; without it "a bias and a shared set of rules" reads as the object of "share". |
| 9 | 204 | `Fable 5.1 vs final labels` | `Fable 5.1 vs.\ final labels` | Punctuation: American English abbreviation takes a period; `refs.bib` also uses "vs.". |
| 10 | 404 | `V2 to V4 occur so rarely` | `\code{V2} to \code{V4} occur so rarely` | LaTeX text-level: these codes are set in `\code` everywhere else and would print in a different font here. |
| 11 | 90, 402, 506, 523, 552, 580 | `windows, a rule-based inference step, and quantitative`; `one request, the AI's response, and the writer's` (90); `weeks, to skill change, or to research` (402); `one request, its AI response, and the writer's` (506); `fragments, an outline, or a stated` (523); `sections, essays, or expanding` (552); `draft, completed text, or added` (580) | Delete the comma before "and"/"or" in each | Punctuation consistency, not an error: most simple lists in the paper omit the serial comma (for example lines 55, 69, 105, 591). |
| 12 | 290 | `against perceived ownership` | `against Perceived Ownership` | Term: line 100 capitalizes the measure, and this same text capitalizes "GPT Final". |
| 13 | 232 | `Delegation in chat is mostly a WildChat pattern.` | `Delegate in chat is mostly a WildChat pattern.` | Term: the archetype is named "Delegate in chat" (lines 235, 246, 256). |
| 14 | 295 | `Of drafting-stage windows` | `Of translating-stage (drafting) windows` | Term: the stage is named "translating" (lines 130, 414, 531); "drafting" is operation `O10`. Glossing it here also covers the later "drafting windows" (lines 295, 394). |
| 15 | 298 | `into surrender-leaning most often` | `into the surrender-leaning category most often` | Term: "surrender-leaning" is an adjective elsewhere; here it stands as a noun. |
| 16 | 314 | `writers leave surrender-leaning in 9 of 17` | `writers leave the surrender-leaning category in 9 of 17` | Term: same as row 15. |
| 17 | 348 | `Quick return (not a trigger)` | `Quick return (not recommended)` | Term: lines 334, 356, 357 and 398 count this as one of four triggers. |
| 18 | 701 | `Neutral, moderate` | `Neutral-mechanical, moderate` | Term: the category is "neutral-mechanical" (lines 165, 392, 686). |
| 19 | 705, 706, 708, 710 | `Surrender, moderate` (705, 710); `Surrender, weak` (706); `Surrender, strong` (708) | `Surrender-leaning, moderate`; `Surrender-leaning, weak`; `Surrender-leaning, strong` | Term: the category is "surrender-leaning" (line 686 and Table 2, lines 159-161). |
| 20 | 714, 715 | `Surrender, moderate` (714); `Surrender, weak` (715) | `Surrender-leaning, moderate`; `Surrender-leaning, weak` | Term: same as row 19. |
| 21 | 105 | `code and translation only were excluded` | `code and translation-only work were excluded` | Parse: "translation only" reads as "only translation was excluded". |
| 22 | 235 | `delegate in chat rests on 2 NIRVANA sessions` | `the Delegate in chat row rests on 2 NIRVANA sessions` | Parse: the lowercase archetype name reads as a verb. |
| 23 | 376 | `so agents did not bypass it and read a working-paper version instead` | `so agents did not bypass it; they read a working-paper version instead` | Parse: "did not" can be read as covering both "bypass" and "read". |
| 24 | 449 | `The addition is making it observable, with the code for whose content it is and the typing that follows, on the same act of pasting.` | `The addition is making it observable on the same act of pasting, through the code for whose content it is and the typing that follows.` | Parse: the interrupting phrase separates "observable" from "on the same act of pasting". |
| 25 | refs.bib 228 | `generative AI -assisted writing` | `generative AI-assisted writing` | Typo outside main.tex that prints in the reference list: stray space before the hyphen. Check against the published title. |

Note, no fix proposed: refs.bib line 138 (`padmakumar2026`) lists surnames only, so that reference will print without given names.

Findings: 25 (24 in main.tex, 1 in refs.bib); 0 misspelled words, 2 hyphenation variants.
