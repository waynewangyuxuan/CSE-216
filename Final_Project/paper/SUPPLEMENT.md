# Supplementary materials plan

Every piece of work the paper describes, mapped to where its evidence lives, plus what Wayne still has to do. Paths are relative to the repository root. `scripts/check_supplement.py` verifies that each path below exists and reports whether git tracks it.

Status key: **public** = tracked on branch `final-project`; some are in commits not yet pushed. **local** = exists only on this machine (git-excluded), so an instructor cannot see it through the repository.

## 1. Evidence for each piece of work

| Paper section | Work described | Evidence | Status |
|---|---|---|---|
| Method: data | NIRVANA windows and counts | `Final_Project/data/REPORT.md`, `Final_Project/data/counts.json`, `Final_Project/data/scripts`, `Final_Project/data/decisions.tsv` | public |
| Method: data | NIRVANA and WildChat raw files and derived windows | `Final_Project/data/raw`, `Final_Project/data/windows.jsonl`, `Final_Project/data/sample.csv`, `Final_Project/data/gold.csv` | local, contains dataset text; do not submit |
| Method: data | WildChat definition, funnel, screen, audit, sample | `Final_Project/wildchat/DEFINITION.md`, `Final_Project/wildchat/REPORT.md`, `Final_Project/wildchat/results/screen_labels.jsonl`, `Final_Project/wildchat/results/audit_labels.jsonl`, `Final_Project/wildchat/results/selected_conversations.tsv`, `Final_Project/wildchat/scripts` | public |
| Method: codebook | v1.0, v1.1, pilot agreement, change log | `Final_Project/CSE216_Research_Writing_Codebook_v1.0.md`, `Final_Project/codebook/CSE216_Research_Writing_Codebook_v1.1.md`, `Final_Project/codebook/REPORT.md`, `Final_Project/codebook/REPORT_AFTER_C3.md`, `Final_Project/codebook/decisions.tsv`, `Final_Project/codebook/pilot_results` | public |
| Method: coding | First sample: briefs, labels, adjudication, agreement | `Final_Project/coding/REPORT.md`, `Final_Project/coding/coder_brief.md`, `Final_Project/coding/adjudicator_brief.md`, `Final_Project/coding/results/labels_ab.csv`, `Final_Project/coding/results/final_labels.csv`, `Final_Project/coding/results/adjudication_log.csv`, `Final_Project/coding/results/access_audit.json` | public |
| Method: coding | NIRVANA whole sessions | `Final_Project/sessions/REPORT.md`, `Final_Project/sessions/coder_brief.md`, `Final_Project/sessions/results/final_labels_nirvana.csv`, `Final_Project/sessions/results/adjudication_log.csv`, `Final_Project/sessions/results/access_audit.json`, `Final_Project/sessions/results/agreement.json` | public |
| Method: coding | WildChat whole conversations | `Final_Project/wildchat/results/final_labels_wildchat.csv`, `Final_Project/wildchat/results/labels_ab_wildchat.csv`, `Final_Project/wildchat/results/adjudication_log_wildchat.csv`, `Final_Project/wildchat/results/agents.tsv`, `Final_Project/wildchat/results/access_audit.json` | public |
| Method: coding | Fable 5.1 gold-set labels and comparison | `Final_Project/codebook/gold_agent/fable_labels.csv`, `Final_Project/coding/results/fable_comparison.md` | public |
| Method: coding | Coder views and rulings text | `Final_Project/coding/blind`, `Final_Project/sessions/blind`, `Final_Project/wildchat/blind` | local, contains dataset text; do not submit |
| Method: inference | v1.2 rule table, freeze, calibration | `Final_Project/inference/CSE216_Writing_Codebook_v1.2.md`, `Final_Project/inference/FROZEN.md`, `Final_Project/inference/REPORT.md`, `Final_Project/inference/decisions.tsv`, `Final_Project/inference/scripts/apply_rules.py`, `Final_Project/inference/calibration` | public |
| Method: log facts | Timing, typing, essay outcomes (numbers only) | `Final_Project/analysis/derived/timing_nirvana.csv`, `Final_Project/analysis/derived/timing_wildchat.csv`, `Final_Project/analysis/derived/outcome_nirvana.csv`, `Final_Project/analysis/scripts/extract_raw.py` | public |
| Results: all numbers | Rerunnable analysis | `Final_Project/analysis/scripts/run_all.sh`, `Final_Project/analysis/results/mining.md`, `Final_Project/analysis/results/out_of_sample.md`, `Final_Project/analysis/results/patterns.md` | public |
| Results: theses | Theses and the checks on them | `Final_Project/analysis/THESES.md`, `Final_Project/analysis/SKEPTIC_T.md`, `Final_Project/analysis/SKEPTIC.md`, `Final_Project/analysis/GATE_T.md`, `Final_Project/analysis/FINDINGS.md` | public |
| Results: narratives | Paraphrased sessions e41, e24, e70 | `Final_Project/report/narratives.md` | public |
| Results: figures | Figures 1 to 5 | `Final_Project/paper/figures`, built by `Final_Project/paper/scripts/sync_figures.py` from `Final_Project/analysis/figures` | public |
| Related work | Search protocol, log, registry, screening reliability | `Final_Project/lit/protocol.md`, `Final_Project/lit/search_log.csv`, `Final_Project/lit/papers.csv`, `Final_Project/lit/citation_check.csv`, `Final_Project/lit/related_work.md`, `Final_Project/lit/scripts` | public |
| Related work | Search results and screener raw output | `Final_Project/lit/raw`, `Final_Project/lit/screening` | local, contains publisher abstracts |
| Related work | Each citation's read level | `Final_Project/paper/CITATIONS.tsv` | public |
| Discussion | Framework comparison, 11 case pairs | `Final_Project/lit/framework_comparison.md`, `Final_Project/lit/critic_report.md`, `Final_Project/lit/critic_recheck.md`, `Final_Project/report/M2_draft.md` | public |
| Barriers | Plan, reversal, checkpoints | `Final_Project/PACING.md`, `Final_Project/codebook/C3_INSTRUCTIONS.md` | public |
| Barriers | Proposal quote, Milestone 1 counts, lost files | `Final_Project/BRIEF.md` (the proposal and Milestone 1 themselves are not in the repository; add them if you can) | public |
| Barriers | Decisions and events | `.wayne/steering/product.md`, `.wayne/bets` (each bet's `log.tsv` and `gate/` critic reports) | local |
| Barriers | Shared-index commit | commit `ff704c6`, `Final_Project/inference/FROZEN.md` | public |
| Barriers | PMC reCAPTCHA | `Final_Project/inference/sources.tsv` | public |
| AI Use Statement | Models used | session transcripts (section 3), `Final_Project/wildchat/results/agents.tsv`, `Final_Project/coding/results/access_audit.json`, `Final_Project/sessions/results/access_audit.json` | transcripts local |
| Appendix | Full codebook | `Final_Project/codebook/CSE216_Research_Writing_Codebook_v1.1.md`, `Final_Project/inference/CSE216_Writing_Codebook_v1.2.md` | public |
| This paper | Source and checks | `Final_Project/paper/main.tex`, `Final_Project/paper/refs.bib`, `Final_Project/paper/scripts/check_tex.py`, `Final_Project/paper/scripts/spellcheck.py`, `Final_Project/paper/scripts/check_build.py`, `Final_Project/paper/PROOFREAD.md`, `Final_Project/paper/CRITIC.md`, `Final_Project/paper/CRITIC_RECHECK.md` | public once committed |

## 2. What Wayne still has to do

1. **Export the AI chat logs as PDFs.** Links are not accepted, and the logs must match the AI Use Statement. Nothing has been exported or uploaded. See the decision in section 3.
2. **Push `final-project`, then confirm section 1 matches what the remote shows.** The parent session pushes after verifying.
3. **Give the instructor and TA access to the repository** (GitHub, branch `final-project`). Do this only after confirming the branch holds what section 1 says. Nothing has been shared.
4. **Decide about local-only evidence.** The bet logs and gate critic reports under `.wayne/` are not in the repository, and they are the main evidence for several Barriers. Section 3 raises this.
5. **Upload the final paper PDF and supplementary materials to Canvas** by Monday, December 7, 8:00pm.

## 3. Decisions for Wayne

**Decision A: how to hand over transcripts.** This needs your call, and I did nothing about it. The session transcripts are in `~/.claude/projects/-Users-wang-CSE-216/` (about 115 session and subagent files, 181 MB, as of Nov 8). They contain dataset text, because coder agents read NIRVANA and WildChat windows, and agent output, including file contents the agents read. The rubric asks for chat logs as PDFs for any AI use. The project has kept dataset text out of its public record. WildChat text may contain personal details, and the NIRVANA OSF node showed no license through its API (`Final_Project/data/REPORT.md`).

| Option | What it gives | Risk |
|---|---|---|
| Export main session logs in full, and subagent coder logs with dataset text redacted by a script (recommended) | Complete view of what agents were told and did, with no dataset text | Requires a redaction script and a check of its output |
| Export everything as PDFs and submit only through Canvas | Most complete | Dataset text leaves this machine; PDF size is large |
| Export main session logs only, and list subagent sessions as omitted | Simple | Under-reports the coding, which the statement says was AI's |

Recommendation: the first option, and tell the instructor what was redacted and why. Ask the instructor if that does not satisfy "AI chat logs".

**Decision B: local-only evidence.** Copy `.wayne/bets/*/gate/` and each bet's `log.tsv` into a repository folder, after scanning them for dataset text, or submit them with the supplement. Recommendation: copy them, because the rubric gives no credit for work without evidence.

**Decision C: does the repository stay public?** The `final-project` branch is public. It holds no dataset text by project rule, but the coded labels and window ids describe real conversations. Decide whether to keep it public or restrict it to the instructor and TA.
