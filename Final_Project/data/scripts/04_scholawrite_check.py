#!/usr/bin/env python
"""Vocabulary check for ScholaWrite. No baseline analysis.

Downloaded files are read as text and never imported. If the gated parquet files are in
raw/scholawrite/hf/ (see 00_fetch.sh), fields and labels are confirmed from split all_sorted.
Otherwise the result is PARTIAL: labels from the public paper and repo, fields only as named in code.
Only the set of labels is reported, not their frequencies.
"""
import collections, glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import pyarrow.parquet as pq

PUB = os.path.join(common.RAW, "scholawrite", "public")


def main():
    repo = open(os.path.join(PUB, "labels.py.txt"), encoding="utf-8").read()
    block = re.search(r"WRITING_INTENTIONS: List\[str\] = \[(.*?)\]", repo, re.S).group(1)
    labels = re.findall(r'"([^"]+)"', block)
    paper = html.unescape(re.sub(r"<[^>]+>", " ", open(os.path.join(PUB, "paper_v4.html"), encoding="utf-8").read()))
    paper = re.sub(r"\s+", " ", paper)
    in_paper = {l: l in paper for l in labels}
    code = open(os.path.join(PUB, "small_model_classifier.py.txt"), encoding="utf-8").read()
    named = sorted(set(re.findall(r'"([a-z_]+)"', code)) & {"label", "project", "timestamp"})
    out = {"labels_from_repo": labels, "label_count": len(labels), "all_labels_in_paper": all(in_paper.values()),
           "missing_from_paper": [k for k, v in in_paper.items() if not v],
           "fields_named_in_public_code": named}
    files = sorted(glob.glob(os.path.join(common.RAW, "scholawrite", "hf", "data", "all_sorted-*.parquet")))
    if files:
        out["status"] = "CONFIRMED_FROM_DATA"
        schema = pq.ParquetFile(files[0]).schema_arrow.names
        c, projects = collections.Counter(), set()
        for f in files:
            table = pq.read_table(f, columns=["label", "project"])
            c.update(table.column("label").to_pylist())
            projects.update(table.column("project").to_pylist())
        out.update({"fields_in_data": schema, "labels_in_data": sorted(c), "label_count_in_data": len(c), "data_rows": sum(c.values()),
                    "projects": len(projects), "label_sets_match": set(c) == set(labels),
                    "has_ai_interaction_field": any(k in " ".join(schema).lower() for k in ("gpt", "chat", "llm", "response"))})
    else:
        out["status"] = "PARTIAL_GATED_NO_DATA_SEEN"
    os.makedirs(common.WORK, exist_ok=True)
    json.dump(out, open(os.path.join(common.WORK, "scholawrite_stats.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
