#!/usr/bin/env python
"""Rank every eligible record for formal long-form writing from keywords and embeddings. No LLM; reads cached screen labels.
Usage: 04_rank.py enrich | confirm
 enrich:  score0 = cosine to (mean INCLUDE - mean non-INCLUDE) embedding of the TRAIN half of the seed, plus a keyword score.
          Draws ENRICH_N records at random (key "enrich") from the top ENRICH_POOL by score0, not yet labelled. Training use only.
 confirm: logistic regression on embedding + keyword features, trained on seed-train + enrichment labels (INCLUDE = 1).
          The top CONFIRM_K unused records by score go to the LLM confirm pass (same prompt as the seed).
The seed TEST half is never used to fit anything, so its INCLUDE records give a rough recall of the top-K cut.
Writes blind/ids_<stage>.txt and results/rank_<stage>.tsv (hashes, ranks and scores only)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7
import numpy as np

ENRICH_N, ENRICH_POOL, CONFIRM_K = 600, 6000, 2500
KW = {"genre": r"\b(essays?|research paper|papers?|thesis|dissertation|literature review|reports?|proposals?|articles?|abstract|introduction|conclusion|"
               r"statement of purpose|personal statement|chapter|capstone|manuscript|business plan|case study)\b",
      "verb": r"\b(write|rewrite|re-write|paraphrase|proofread|revise|edit|expand|improve|polish|draft|reword|rephrase|summari[sz]e|elaborate)\b",
      "length": r"\b\d{3,4}\s*-?\s*words?\b|\bword count\b|\bparagraphs?\b",
      "cite": r"\b(apa|mla|harvard|citations?|references|in-text|bibliography|sources|scholarly|peer[- ]reviewed)\b",
      "academic": r"\b(university|course|assignment|module|professor|lecturer|marking|rubric|grade|academic)\b",
      "negative": r"\b(story|stories|poem|poetry|lyrics|song|email|letter|code|python|javascript|sql|script|role-?play|character|midjourney|prompt|game|episode|anime)\b"}
KWR = {k: re.compile(v, re.I) for k, v in KW.items()}


def kw_features(texts):
    f = np.array([[len(KWR[k].findall(t)) for k in KW] + [len(t)] for t in texts], dtype=np.float32)
    return np.log1p(f)


def kw_score(F):
    k = list(KW)
    return F[:, k.index("genre")] + 0.5 * F[:, k.index("verb")] + 0.5 * F[:, k.index("length")] + 0.5 * F[:, k.index("cite")] + 0.3 * F[:, k.index("academic")] - F[:, k.index("negative")]


def load():
    el = w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))
    texts = [r["text"] for r in w7.read_jsonl(os.path.join(w7.BLIND, "embed_text.jsonl"))]
    E = np.load(os.path.join(w7.BLIND, "emb.npy")).astype(np.float32)
    lab = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.OUT, "screen_labels.jsonl"))}
    split = {}
    for l in open(os.path.join(w7.OUT, "seed_ids.tsv")).read().split("\n")[1:]:
        if l:
            h, s, _ = l.split("\t")
            split[h] = s
    return el, texts, E, lab, split


def write(stage, el, score, chosen):
    order = np.argsort(-score, kind="stable")
    rank = np.empty(len(order), dtype=int)
    rank[order] = np.arange(1, len(order) + 1)
    open(os.path.join(w7.BLIND, f"ids_{stage}.txt"), "w").write("\n".join(chosen) + "\n")
    idx = {r["hash"]: i for i, r in enumerate(el)}
    with open(os.path.join(w7.OUT, f"rank_{stage}.tsv"), "w") as f:
        f.write("hash\trank\tscore\n")
        for h in sorted(chosen, key=lambda h: rank[idx[h]]):
            f.write(f"{h}\t{rank[idx[h]]}\t{score[idx[h]]:.5f}\n")
    return rank


def main():
    stage = sys.argv[1]
    el, texts, E, lab, split = load()
    F = kw_features(texts)
    used = np.array([r["used"] for r in el])
    hs = [r["hash"] for r in el]
    y_of = lambda h: 1 if lab[h]["label"] == "INCLUDE" else 0
    if stage == "enrich":
        tr = [i for i, h in enumerate(hs) if split.get(h) == "train" and h in lab]
        pos = [i for i in tr if y_of(hs[i])]
        neg = [i for i in tr if not y_of(hs[i])]
        d = E[pos].mean(0) - E[neg].mean(0)
        s_emb, s_kw = E @ d, kw_score(F)
        score = (s_emb - s_emb.mean()) / s_emb.std() + (s_kw - s_kw.mean()) / s_kw.std()
        score[used] = -np.inf
        pool = [hs[i] for i in np.argsort(-score, kind="stable")[:ENRICH_POOL] if hs[i] not in lab]
        chosen = sorted(pool, key=lambda h: w7.key("enrich", h))[:ENRICH_N]
        write(stage, el, score, chosen)
        print(f"train labelled {len(tr)} (INCLUDE {len(pos)}); enrichment drawn {len(chosen)} from top {ENRICH_POOL}")
    elif stage == "confirm":
        from sklearn.linear_model import LogisticRegression
        enrich = [l.strip() for l in open(os.path.join(w7.BLIND, "ids_enrich.txt")) if l.strip()]
        train = [h for h in hs if split.get(h) == "train" and h in lab] + [h for h in enrich if h in lab]
        idx = {h: i for i, h in enumerate(hs)}
        X = np.hstack([E, F])
        Xt, yt = X[[idx[h] for h in train]], np.array([y_of(h) for h in train])
        m = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced").fit(Xt, yt)
        score = m.decision_function(X)
        score[used] = -np.inf
        top = [hs[i] for i in np.argsort(-score, kind="stable")[:CONFIRM_K]]
        rank = write(stage, el, score, top)
        test = [h for h in hs if split.get(h) == "test" and h in lab]
        tp = [h for h in test if y_of(h)]
        inK = [h for h in tp if rank[idx[h]] <= CONFIRM_K]
        res = {"train_n": len(train), "train_include": int(yt.sum()), "confirm_k": CONFIRM_K, "test_n": len(test), "test_include": len(tp),
               "test_include_in_top_k": len(inK), "test_include_ranks": sorted(int(rank[idx[h]]) for h in tp), "eligible": len(hs)}
        json.dump(res, open(os.path.join(w7.OUT, "rank_confirm_meta.json"), "w"), indent=1)
        print(json.dumps({k: v for k, v in res.items() if k != "test_include_ranks"}))


if __name__ == "__main__":
    main()
