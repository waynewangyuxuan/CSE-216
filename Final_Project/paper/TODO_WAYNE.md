# TODO for Wayne

Everything below needs you. Items marked in the source as `% TODO(Wayne):` are listed in section 1; `scripts/check_todos.py` fails if one is missing here.

## 1. In `main.tex` (search for `TODO(Wayne)`)

1. **Affiliation.** Replace the affiliation line with your institution, city, country and preferred email.
2. **NIRVANA consent and compensation.** Open arXiv:2604.07344 and add its recruitment, consent and compensation details if it states them. This draft says the sections read left no record, because no download was allowed here.
3. **IRB.** Add a determination sentence if you obtained one. None is recorded in the project.
4. **Method citations.** Standard citations for Cohen's kappa, Spearman, optimal matching and silhouette are not in `lit/`, and the draft was limited to `lit/`. The rubric says to cite the analysis method. Approve adding them or leave as is.
5. **Codebook v1.0.** Confirm who wrote it. It says it is a reconstruction dated Nov 2. The repository cannot show the author.
6. **Barriers.** An agent drafted this section, including every "What I learned" sentence. Rewrite any lesson that is not yours.
7. **AI Use Statement: your review.** Add what you personally reviewed and when: your read of M2 (planned Nov 14), your read and edits of this paper, your own full proofread. None has happened as of this draft, and none is claimed.
8. **AI Use Statement: other tools.** State whether you used AI for the proposal and Milestone 1, and whether any other tool (ChatGPT, Grammarly, editor autocomplete) touched this work.
9. **Chat logs sentence.** Confirm it once the logs are exported.

## 2. Compiling

No TeX is installed on this machine, and nothing was downloaded. **Decide how to compile**: Overleaf is the simplest (upload `main.tex`, `refs.bib`, `figures/`; class `acmart` is available there). The source has never been compiled, so expect to fix small errors. After compiling, check that the length is near 20 pages (estimate 17.5, excluding references and appendix), that tables fit the margins, and that `\citet` and the longtables render. Confirm the current official ACM CHI template settings at submission time.

## 3. Proofreading

- **Your own full proofread is required by the assignment** and cannot be done by an agent. It has not been done.
- Rerun the checks after your edits, then fix anything they report:

```bash
cd /Users/wang/CSE-216/Final_Project/paper && python3 scripts/spellcheck.py && python3 scripts/check_tex.py && python3 scripts/check_todos.py
```

## 4. M2 feedback (to fold in later)

M2 is due Nov 15. Feedback arrives after that and should be folded in here before Dec 7.

- [ ] M2 instructor feedback: _(none yet)_
- [ ] Nov 19 and Nov 24 professor meetings: _(none yet)_. Pending questions from earlier bets: what "conceptual analysis" meant, and whether the success criterion may be read as this paper reads it.
- [ ] Decide whether to do a v1.3 logged rerun (paper's Discussion lists the changes). Not done, because this bet added no new analysis.
- [ ] Decide whether to code 20 windows blind yourself. It would be the only human check on the codes, and the paper would have to be updated if you do.
- [ ] Decide on mockups for the two triggers. None built.

## 5. Supplementary materials

See `SUPPLEMENT.md` sections 2 and 3. Three decisions wait for you: how to hand over transcripts, whether local-only evidence moves into the repository, and whether the repository stays public.

## 6. Fixing proofreading and critic findings

`PROOFREAD.md` and `CRITIC.md` record what agents found and fixed in this draft.
