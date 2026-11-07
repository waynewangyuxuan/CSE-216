# Theses (Bet 9)

Four theses about these 106 sessions (NIRVANA 71, WildChat 35), each followed by the claims it rests on. Every number is in `results/mining.md` (section given as §) or, where marked, in Bet 8's results. Tokens: SLr = surrender-leaning by R16 (request only), SLb = surrender-leaning by any other rule (behavior basis). "Support" = offloading or augmenting. A fresh skeptic checked every claim (`SKEPTIC_T.md`); this version takes in its rewordings, listed at the end. Caveats are collected at the end, not repeated per claim.

## T1 (RQ1, the boundary). AI use stays on the support side when the content is the writer's own or passes through the writer's hands. It substitutes when AI-generated prose goes into the draft whole, or is only polished, and the writer moves on.

| # | Claim | Number | Source |
|---|---|---|---|
| C1 | Pasting is not the line. In NIRVANA, writers paste in about the same share of offloading and behavior-based surrender windows | any paste: OFF 65.5%, SLb 63.8% | §5 |
| C2 | What differs is whose content was pasted and what follows. After pasting an AI proposal whole (`D4`) the writer types almost nothing and is back in the chat in about a minute; after a partial take (`D3`) the writer keeps typing for minutes | D4 pastes 42 (SLb 39): median typed after 6 chars, dwell 70.5 s. D3 pastes 32 (OFF 28): typed 304.5, dwell 288.1 s. D1 pastes (own text back) 29 (OFF 28): dwell 150.1 s | §5 |
| C3 | The same line shows in the finished essays. Sessions with more behavior-based surrender end with more AI text in the essay and lower felt ownership; request-only surrender tracks the AI share only weakly | SLb share vs GPT Final %: rho 0.603 (p 0.0005); vs ownership −0.546 (p 0.0005). Multi-window sessions only: 0.536, −0.493. SLr share vs GPT Final %: 0.191 (p 0.117) | §8, §10 |
| C4 | Sessions with any behavior-based surrender window end with a median essay mostly by the AI; sessions without one, with a median essay with no AI text | median GPT Final % 0.806 (34 sessions) vs 0.0 (37) | §8 |
| C5 | Substitution sits with requests for generated prose. In these codes that is the drafting stage: almost every drafting window is a generation request. Requests that are not for generated prose are rarely surrender-leaning at any stage | 192 of 195 drafting windows are `F4`. SL share: drafting 0.795; non-`F4` planning 0.071, non-`F4` reviewing 0.098; `F4` while planning 0.556 | §4, §10 |
| C6 | Planning requests come earlier in sessions and reviewing requests later than chance | P mean position 0.412 vs 0.5 (p 0.0005); R 0.562 (p 0.0005) | §4 |
| C7 | Entering surrender-leaning most often lands on asking for generation and iterating in chat; leaving it most commonly lands on the writer revising AI text in the editor | into SL: D2/U4 18 of 29; out of SL: D3/U3 8 of 29 (the plurality) | §3 |
| C8 | Six archetypes describe the sessions. The two paste archetypes end with essays almost wholly by the AI; the two support archetypes do not | Paste into the draft 12 sessions, median GPT Final % 0.971; One-shot paste 7, 1.0; Short support visit (NIRVANA 25) 0.0; Long working session (NIRVANA 19) 0.176 | §1, §8 |

## T2 (RQ1 across sessions, and RQ3). The writer's own text is the anchor. Sessions that start from it lean to the support side, and a visible own draft predicts that the next request stays there too.

| # | Claim | Number | Source |
|---|---|---|---|
| C9 | Across NIRVANA sessions, more text in the editor at the first request goes with a larger support share. The link is between sessions, and about half as strong once one-window sessions are set aside | rho 0.401, p 0.0005 (65 sessions); multi-window only 0.256, p 0.075 (54); minutes before first ask 0.242, p 0.043 | §5, §10 |
| C10 | First window's own work and the session's support share | NIRVANA none visible 0.497 (30), notes 0.708 (17), draft 0.767 (18). WildChat unseen 0.07 (19; 18 have SL), draft 1.0 (7; none has SL) | §5 |
| C11 | A visible draft predicts lower odds that the next substantive window is surrender-leaning, with the current window's category, chat uptake, dataset and position in the model | odds ratio 0.225 [0.074, 0.441]; next-SL rate 0.213 with a draft vs 0.647 without | §3 |
| C12 | In NIRVANA, writers leave surrender-leaning more often when their own draft is visible, and enter it more often when they have only notes | leaving SL: draft 9/17, notes 14/34, none visible 4/21. Entering SL from support: notes 16/41, draft 10/59 (fig21 pools both datasets) | §3 NIRVANA rows |
| C13 | In WildChat (chat only), sessions that become surrender-leaning rarely come back; in NIRVANA most do | return to support after the first SL window: WildChat 2 of 21, NIRVANA 17 of 29 | §6 |
| C14 | The writer's document grows through the session | NIRVANA median editor characters at request, position bins 0–4: 101, 342, 1156.5, 1369, 2157 | §5 |

## T3 (RQ1 and RQ2). In NIRVANA, surrender-leaning windows leave no work on the text: the writer types little and is back in the chat within about a minute. The copy is not faster; the difference is the typing that follows.

| # | Claim | Number | Source |
|---|---|---|---|
| C15 | NIRVANA dwell (response to next request) is under half as long for surrender-leaning windows, in every position bin and within most sessions | median 57.8 s vs 152.2 s (within-session shuffle p 0.0005); SLb alone 65.4 s (p 0.0035). By position bin SL 40.6–69.2 s, support 118.4–219.0 s. Shorter in 13 of 17 sessions that have both | §7, §10 |
| C16 | The gap is typing time. With under 50 characters typed, behavior-based surrender and support windows have the same dwell | under 50 typed: SLb 44.1 s, support 43.5 s; 50+ typed: 156.1 vs 308.3 | §10 |
| C17 | Typing after the response separates the sides; time to the first copy does not | median typed after: SLb 0, OFF 108, AUG 256. First copy: SLb 15.5 s vs support 10.35 s (p 0.616); OFF 10.3 s | §5, §7 |
| C18 | Checks that would show deliberation are nearly absent | V3 13 windows in 6 sessions, V4 0, V2 5 | §10; Bet 8 `patterns.md` §1 |
| C19 | Felt ownership is lower in sessions with either kind of surrender, mostly between sessions with any behavior-based surrender and those with none | ownership vs SLb share −0.546; vs SLr share −0.332 (p 0.004); among the 34 sessions with any SLb, −0.206 (p 0.246) | §8, §10 |
| C20 | WildChat's only clock (AI reply to next AI reply) does not separate SL from support | 232 s vs 332 s, p 0.39 | §7 |

RQ2 argument (analytic). Shaw & Nave define surrender by absent deliberation. The log cannot show deliberation, but it shows its usual by-product, work on the text: typing after the response is near zero exactly where AI substance is taken over (C2, C17), and reasoned checks are nearly absent (C18). Writers do register origin, since felt ownership is lower where AI text was taken in (C19; Joshi & Vogel 2025). So the substitution writers can see is that the text is not theirs. What they are unlikely to see is that its argument was never worked through (H. Kim et al. 2026). The least visible substitutions keep the writer typing: ideas from a generation request written up in the writer's own words (`D2 U7`, augmenting in 37 of 52 windows, Bet 8 `patterns.md` §1), where ownership need not fall (Jelson et al. 2026b; Bhat et al. 2026 report unnoticed influence), and surface-only iteration on an AI draft (30 windows), which feels like editing.

## T4 (RQ3, signals). A writing tool can see substitution risk from two log events, without reading content: a request sent on a near-empty page, and a large paste with little typing after it. Together they catch about two-thirds of surrender-leaning windows.

| # | Trigger (fires when) | Evidence | Source |
|---|---|---|---|
| C21 | Large paste, little typing: 200+ characters pasted, under 50 typed before the next request | fires on 55 of 347 windows; SL among fired 0.64 vs base 0.395; catches 0.464 of SLb; session fire rate vs ownership rho −0.414 (p 0.001) | §9 |
| C22 | Ask on a near-empty page: request sent while the editor holds under 200 characters | fires on 101; SL among fired 0.587; catches 0.449 of SL; fire rate vs ownership −0.281 (p 0.018) | §9 |
| C23 | Together (either fires) | 140 of 347 windows; SL among fired 0.559; catches 0.633 of SL and 0.696 of SLb | §10 |
| C24 | Speed alone is not a trigger: a quick return to chat has modest precision and no relation to outcome | SL among fired 0.548; vs GPT Final % rho 0.139 (p 0.24) | §9 |

Proposed feedback, each tied to its trigger (mockup level): on a near-empty page, before showing generated prose, ask the writer for the claim they want to make (C22, C9–C11); after a large paste with no typing, ask which sentence of it the writer would defend or change (C21, C2). In chat-only tools, where neither event exists, the nearest analogue is a run of generation follow-ups with no own text supplied (WildChat sessions that become SL rarely return, C13; runs of SLr are only slightly over-represented, 46 vs 40.47, p 0.025, one of 40 tests).

## Caveats (collected)

- No human coded anything; all agreement is AI-to-AI. Categories are inferences from behavior, not measurements of thinking.
- Some links are partly built into the codes. `D3` and `D4` are defined partly by how much was pasted and changed, so "typed after" in C2 restates the codes; dwell does not. C5 is close to definitional: `F4` requests feed the SL rules, and drafting is `F4`. GPT Final % measures AI text surviving in the essay, so its link to pasting (C3, C21) is expected; felt ownership is a separate self-report.
- C9, C11 and C19 are mostly between-session. Bet 8's shuffle found no turn-to-turn stickiness once a session's make-up is fixed; "predicts" means across sessions.
- Archetype structure is weak (best silhouette 0.25 at k = 6), though stable: 89–98% of session pairs are grouped the same at k = 4, 5 and 7.
- Many tests were run (40 category n-grams, 29 signature n-grams, 20 latency contrasts, 12 outcome correlations, 4 triggers), uncorrected.
- WildChat has no editor and stamps only AI turns; C1–C4, T3 and T4 rest on NIRVANA alone.

## What the skeptic changed

C3 "does not track" → "tracks only weakly". C5 restated as generation requests, with the within-`F4` numbers. C7 "most often" → "most commonly" (plurality). C9 adds the multi-window figure. C11 and C19 "lowers/falls" → "predicts/is lower". C12 restricted to NIRVANA; C13 credited to the dataset, not the editor. T2 headline "strongest predictor" dropped (current SLr has a larger odds ratio, 7.9). T3 restated around typing, not speed (C16). T4 reduced to the two log events that work; the n-gram run demoted to a note.
