# Skeptic check of THESES.md (Bet 9)

Every number below was recomputed from `mine.load()` with scratch code (not committed). All of `mining.md`'s figures that THESES cites matched exactly. Standard used: direct findings about these 106 sessions, without extra hedging. A claim is downgraded only when its wording says more than the number does, or when a simple confound explains the finding.

## (i) Claim table

| Claim | Verdict | What I checked | Number I got | Suggested wording (if not SUPPORTED) |
|---|---|---|---|---|
| C1 | SUPPORTED | any-paste share by token, NIRVANA | OFF 0.655 (87), SLb 0.638 (69) | |
| C2 | SUPPORTED | paste-by-decision table | D4 42: SLb 39, typed 6, dwell 70.5 s (dwell n=21, 29 sessions; no session has more than 4). D3 32: OFF 28, 304.5, 288.1 s. D1 29: OFF 28, 150.05 s (dwell n=20) | (Token columns restate R13/R-paste rules. Dwell is the part that isn't built in.) |
| C3 | SUPPORTED-REWORD | rho, leave-one-out, multi-window only, drop top-5 SLb | 0.603/−0.546/0.191 match. LOO range 0.59–0.63 and −0.53 to −0.60. Multi-window (56): 0.536, −0.493, SLr 0.24 (p 0.09). Drop top 5: 0.558, −0.519 | "...request-only surrender tracks the AI share only weakly (rho 0.19, n.s.)". "Does not track" says too much. |
| C4 | SUPPORTED | split medians | 0.806 (34) vs 0.0 (37). Essays over 50% AI: 68% vs 24% | |
| C5 | SUPPORTED-REWORD (mostly definitional) | stage share within F4 and within D2 | All 195 T windows are F4/O10, so T = generation request. Non-F4 windows are rarely SL in any stage: P 0.071 (56), R 0.098 (82). Within F4: P 0.556 (27), T 0.795 (166), R 0.80 (10). Within D2: P 0.21, T 0.96, R 0.33 | "Substitution sits with requests for generated prose, which is what the drafting stage is in these codes. Generation requests made while planning or reviewing are also mostly SL (F4: P 0.56, R 0.80). Non-generation requests are almost never SL (under 10%)." |
| C6 | SUPPORTED | mean positions | P 0.412, T 0.498, R 0.562 | |
| C7 | SUPPORTED-REWORD | landing codes | out: D3/U3 8 of 29 (next D2/U4 5). 27 of 29 exits are NIRVANA. in: D2/U4 18 of 29 | "Leaving SL most commonly (8 of 29, a plurality) lands on...". "Most often" overstates 28%. |
| C8 | SUPPORTED | archetype medians, k = 3–8 | Medians match. Short support (35), Long working (21) and One-shot (7) are identical for k = 4–7. Paste into the draft (12, 0.971) holds at k = 6–8. At k = 5 it merges into 32 sessions (median 0.873) | |
| C9 | SUPPORTED-REWORD | drop D1 windows; drop R13; multi-window only; within-session | Base 0.401. Without D1: 0.445 (p 0.0015). Without R13: 0.392. **Multi-window sessions only (54): 0.256, p 0.075.** Within sessions, SL windows don't have less editor text than support windows (SL lower in 8 of 21, median diff 0) | "Across NIRVANA sessions, more text at the first request goes with a larger support share (rho 0.40). Part of this comes from 11 single-window sessions, and the link is between sessions, not request by request." |
| C10 | SUPPORTED | group means | All match | |
| C11 | SUPPORTED-REWORD | model rates; within-session contrast | Matches. NIRVANA only: 0.237 vs 0.505. In the 16 sessions where the draft flag varies: next-SL 0.176 (51) vs 0.259 (27) | "A visible draft predicts lower odds..." ("lowers" implies a cause). Most of the effect is between sessions. |
| C12 | SUPPORTED-REWORD | switch counts | All match | Say NIRVANA: draft 10/18 vs notes 14/42 vs none 4/21. The "unobservable 1/39" is WildChat, a different dataset, so it isn't an own-work contrast. |
| C13 | SUPPORTED-REWORD | return counts | NIRVANA 17 of 29 with a later window (36 SL sessions), WildChat 2 of 21. Even with SLr-first only: NIRVANA 7/11 vs WildChat 2/21 | "In WildChat (chat only), sessions that become SL rarely come back." "Without an editor" credits the editor, but the datasets differ in many ways. |
| C14 | SUPPORTED | medians by bin | 101, 342, 1156.5, 1369, 2157 | |
| C15 | SUPPORTED-REWORD | dwell by side, position bins, session length, last-window share, session fixed effects, typing | 57.8 vs 152.2 matches (ratio 0.38). SL is shorter in all 5 position bins and all 3 session-length bands. Last-window share is equal (0.21 vs 0.22). Within session: shorter in 13 of 17 sessions with both. Session fixed-effects ratio 0.61. **With under 50 characters typed: SLb 44.1 s vs support 43.5 s; with 50+ typed: 156 vs 308.** SLr is 26/29 U4 (iterate in chat), so its short dwell is built in | "NIRVANA dwell is under half as long for SL windows (median 58 vs 152 s; behavior-based SL 65 s). The gap is time spent typing: at equal low typing, dwell is the same." |
| C16 | SUPPORTED | first copy | 15.5 vs 10.3. Within 10 s: 20/52 copied vs 31/64 | |
| C17 | SUPPORTED | V distribution | V3 13 windows in 6 sessions, V4 0, V2 5. V0 376 of 498 | |
| C18 | SUPPORTED-REWORD | rho | −0.546, −0.332 match. Among sessions with any SLb (34), SLb share vs ownership is −0.21 (p 0.25) | "Felt ownership is lower in sessions with more of either kind of surrender." "Falls" implies change within a person. The ownership link is mostly any SLb vs none. |
| C19 | SUPPORTED | | 232 vs 332, p 0.39 | |
| C20 | SUPPORTED | trigger recompute | 55 fired, precision 0.64 (50 determinate). 30 of 55 fired windows are D4 | (The 0.827 GPT Final rho is expected, because it measures pasted text.) |
| C21 | SUPPORTED | trigger; first vs later windows | Precision 0.587. First windows 0.63 vs not-fired 0.18. Later windows 0.56 vs 0.33 | |
| C22 | SUPPORTED | | 0.548. rho 0.139 (GPT), −0.105 (ownership) | |
| C23 | WEAK | n-gram test | 46 vs 40.47 (p 0.025), SLr×4 p 0.049. These are 2 of 40 uncorrected tests, about the number expected by chance | "Runs of generation follow-ups are somewhat more common than chance (p 0.025, one of 40 uncorrected tests)." Or drop it as a trigger. |

## (ii) Per thesis

**T1.** C1–C2 restate the rule table (D4 paste maps to SLb, D1/D3 to OFF), and dwell is their only non-definitional content. The outcome links survive every robustness check (C3: LOO, single-window sessions removed, top-5 removed). C5 is mostly definitional. The drafting stage equals F4 (192/195), and F4 is what triggers SL rules. Non-F4 windows are SL under 10% of the time in planning and reviewing. Even inside F4, stage matters little: R 0.80 and T 0.795 are the same, and only P is lower (0.56, n=27). Within D2, stage still separates (0.21/0.96/0.33). That is because T-stage D2 means "asked for prose". The headline is fair. Saying substitution is "where the writer requests prose" would be truer than naming the Flower & Hayes stage.

**T2.** The R13 confound (d) does not hold: dropping D1 or R13 windows leaves rho at 0.445 or 0.392. The single-window confound does matter. On multi-window sessions alone, rho drops to 0.256 (p 0.075), because the 11 single-window sessions are bimodal: an empty page gives support share 0, and text gives 1. Within a session, SL windows do not come at lower editor length (8/21). The C11 lagged effect shrinks within session (0.18 vs 0.26). **Headline overreach:** "its absence is the strongest observable predictor". In the model, current-SLr has OR 7.9, larger than the draft effect (1/0.225 = 4.4), and relative position has OR 7.8. Suggested: "...and its absence is a strong predictor (OR 0.23 for a visible draft), across sessions more than within them."

**T3.** Dwell differences are not explained by position, session length or last-window blanks (a). But they are explained by typing. At under 50 characters typed, SLb and support dwell are the same (44 vs 44 s). The thesis's last sentence already says this ("what is missing is time spent on the text"). It follows that dwell adds no signal beyond typed characters. The RQ2 argument should not treat dwell as a separate proxy for deliberation. SLr dwell is short by construction (U4 = next request in chat). Use SLb vs support (65 vs 152 s, p 0.0035) as the clean test. The headline should say NIRVANA ("within about a minute" = 58 s; support median 2.5 min).

**T4.** **Headline overreach.** "A generation request on a near-empty page" and "without reading content": C21 fires on any request with under 200 characters, and nothing in the logs knows the request type. C23 uses codes (SLr), not log events, and is weak. C22 is weak. So two log events carry the signal. Together (C20 or C21) they fire on 140 of 347 windows, with precision 0.559 vs base 0.395, catching 0.633 of SL and 0.696 of SLb. Suggested: "A writing tool can see substitution risk from two log events, without reading content: a request on a near-empty page and a large paste with little typing after it. Together they catch about two-thirds of SL windows."

## (iii) Strongest and weakest

Strongest: C3 (SLb vs GPT Final and ownership, robust to LOO, single-window removal and top-5 removal), C4, C14, C16, C19, C20, C21, C15 (as a typing-driven gap that holds across position, length and within session), C1, C6.

Weakest: C23 (multiple-testing level), C5 (mostly definitional), C9 (half the strength and n.s. without single-window sessions), C11 (mostly between-session), and the headline phrases "strongest observable predictor" (T2) and "generation request ... without reading content" (T4).
