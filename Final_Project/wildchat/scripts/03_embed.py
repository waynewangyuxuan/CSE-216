#!/usr/bin/env python
"""Embed every eligible record's masked user text (first 2,000 characters, user turns only) with a local open model. No LLM.
Model: BAAI/bge-small-en-v1.5 at a pinned revision, through sentence-transformers, max 512 tokens, normalized.
Writes blind/emb.npy (float16, eligible.jsonl order) and results/embed_meta.json. Skips work if emb.npy matches the eligible list."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7
import numpy as np

MODEL = "BAAI/bge-small-en-v1.5"
REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"


def main():
    rows = w7.read_jsonl(os.path.join(w7.BLIND, "embed_text.jsonl"))
    el = w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))
    assert [r["hash"] for r in rows] == [r["hash"] for r in el]
    out = os.path.join(w7.BLIND, "emb.npy")
    if os.path.exists(out) and np.load(out, mmap_mode="r").shape[0] == len(rows) and "--force" not in sys.argv:
        print("emb.npy present, skipping")
        return
    import torch, sentence_transformers
    from sentence_transformers import SentenceTransformer
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    m = SentenceTransformer(MODEL, revision=REVISION, device=dev)
    m.max_seq_length = 512
    texts = [r["text"] for r in rows]
    order = np.argsort([len(t) for t in texts])  # length-sorted batches run faster; order is restored below
    t0 = time.time()
    e = m.encode([texts[i] for i in order], batch_size=128, normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True)
    emb = np.empty_like(e)
    emb[order] = e
    np.save(out, emb.astype(np.float16))
    meta = {"model": MODEL, "revision": REVISION, "sentence_transformers": sentence_transformers.__version__, "torch": torch.__version__,
            "device": dev, "max_seq_length": 512, "normalized": True, "input": "masked user turns joined with ' || ', first 2,000 characters",
            "n": len(rows), "dim": int(emb.shape[1]), "seconds": round(time.time() - t0)}
    json.dump(meta, open(os.path.join(w7.OUT, "embed_meta.json"), "w"), indent=1)
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
