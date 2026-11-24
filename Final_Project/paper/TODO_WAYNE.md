# TODO for Wayne

Everything below needs you. Items marked in the source as `% TODO(Wayne):` are listed in section 1; `scripts/check_todos.py` fails if one is missing here.

## 1. In `main.tex` (search for `TODO(Wayne)`)

1. **Barriers.** An agent drafted this section, including every "What I learned" sentence. The longer version is in `supplement_details.tex`, so check both. Rewrite any lesson that is not yours. The assignment asks for it: Barriers is about the process (what did not go as planned, why, what you would change, what you learned) and ends with what you learned about doing research.
2. **AI Use Statement: your review.** Add what you personally reviewed and when: your read of M2, your read and edits of this paper, your own full proofread.
3. **AI Use Statement: other tools.** State whether you used AI for the proposal and Milestone 1, and whether any other tool (ChatGPT, Grammarly, editor autocomplete) touched this work.
4. **Chat logs sentence.** Confirm it once the logs are exported.

Done on Nov 23 from your answers: affiliation (UCSD, San Diego, email); NIRVANA recruitment and compensation, taken from the preprint's section 3.3 (it states no consent or ethics procedure); no IRB review sought, since no people were involved; codebook v1.0 written by you with AI help; seven standard method citations added and checked against Crossref.

## 2. Compiling

`sh build.sh` builds `main.pdf` with `tectonic` and the current ACM class in `template/`. `python3 scripts/check_build.py` confirms a clean compile and the page count (11 body pages, the target set on Nov 8; 21 total). `main.pdf` is not tracked, so keep it out of git until it is the final file. On Nov 23 every reference was checked against Crossref, DataCite and the arXiv API, and missing authors, pages, volumes and publishers were added in `scripts/build_refs.py`. 13 warnings remain: four journals number articles instead of pages, and ICLR 2024 has no page numbers. One cited Zenodo record (Mallissery 2026) had been deleted, so its citation and the clause it supported were removed.

## 3. Proofreading

- **Your own full proofread is required by the assignment** and cannot be done by an agent. It has not been done.
- Rerun the checks after your edits, then fix anything they report:

```bash
cd /Users/wang/CSE-216/Final_Project/paper && python3 scripts/spellcheck.py && python3 scripts/check_tex.py && python3 scripts/check_build.py && python3 scripts/check_todos.py
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

## 6. Agent review

`PROOFREAD.md`, `CRITIC.md` and `CRITIC_RECHECK.md` record what agents found and what happened to it.

## 7. Smaller calls that are yours

- **Title.** The critic suggests "Mapping Where AI Assistance May Substitute for Thinking", since the paper does not measure thinking.
- **Serial commas.** The paper mixes the two styles in a few simple lists. Proofreading treated this as consistency, not an error, and it was left.
- **Barriers wording.** The motive "to save two hours" was removed because no file records it. Add it back if it is true.
