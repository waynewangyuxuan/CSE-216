#!/usr/bin/env python3
"""Build paper/refs.bib and paper/CITATIONS.tsv from lit/papers.csv so every cited source is a registry record."""
import csv
import pathlib

PAPER = pathlib.Path(__file__).resolve().parents[1]
LIT = PAPER.parent / "lit"

# key: (paper_id, entry type, venue, overrides). Venues, years and DOIs of published versions come from
# the reference list in lit/related_work.md, which took them from Crossref.
REFS = {
    "alam2026": ("S01", "misc", "arXiv:2609.13155", {}),
    "bastani2025": ("C0327", "article", "Proceedings of the National Academy of Sciences", {"volume": "122", "number": "26", "doi": "10.1073/pnas.2422633122"}),
    "bhat2026": ("C0490", "inproceedings", "Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems", {"doi": "10.1145/3772318.3791529"}),
    "chen2026": ("C0399", "article", "Frontiers in Psychology", {"doi": "10.3389/fpsyg.2026.1906199"}),
    "contractor2026": ("C0227", "misc", "arXiv:2607.08849", {}),
    "davalos2026": ("C0184", "misc", "arXiv:2609.17883", {}),
    "flower1981": ("S05", "article", "College Composition and Communication", {"volume": "32", "number": "4", "pages": "365--387", "doi": "10.2307/356600"}),
    "jelson2026nirvana": ("C0453", "misc", "arXiv:2604.07344", {}),
    "jelson2026chi": ("C0042", "inproceedings", "Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems", {"year": "2026", "doi": "10.1145/3772318.3791056"}),
    "joshi2025": ("C0649", "inproceedings", "Proceedings of the 7th ACM Conference on Conversational User Interfaces", {"year": "2025", "doi": "10.1145/3719160.3736608"}),
    "kim2025arcp": ("A027", "article", "Consumer Psychology Review", {"doi": "10.1002/arcp.70008"}),
    "kim2026fallacy": ("C0577", "misc", "arXiv:2604.14807", {}),
    "kosmyna2025": ("C0653", "misc", "arXiv:2506.08872", {}),
    "lee2025": ("C0568", "inproceedings", "Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems", {"pages": "1--22", "doi": "10.1145/3706598.3713778"}),
    "maier2026": ("C0169", "misc", "arXiv:2609.20143", {}),
    "mallissery2026": ("A017", "misc", "Zenodo", {"doi": "10.5281/zenodo.22847816"}),
    "mysore2025": ("C0486", "inproceedings", "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing", {"pages": "16830--16857", "doi": "10.18653/v1/2025.emnlp-main.852"}),
    "padmakumar2026": ("S13", "misc", "arXiv:2605.29392", {}),
    "park2026": ("C0066", "inproceedings", "Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems", {"doi": "10.1145/3772318.3790276"}),
    "poquet2026": ("C0482", "inproceedings", "Lecture Notes in Computer Science", {"doi": "10.1007/978-3-032-37979-5_34"}),
    "reza2025": ("C0133", "article", "Proceedings of the ACM on Human-Computer Interaction (CSCW)", {"doi": "10.1145/3757566"}),
    "risko2016": ("S15", "article", "Trends in Cognitive Sciences", {"volume": "20", "number": "9", "pages": "676--688", "doi": "10.1016/j.tics.2016.07.002"}),
    "shaw2026": ("A058", "misc", "SSRN working paper; also PsyArXiv", {"doi": "10.2139/ssrn.6097646"}),
    "skulmowski2024": ("C0471", "article", "Educational Psychology Review", {"doi": "10.1007/s10648-024-09894-x"}),
    "tankelevitch2024": ("C0579", "inproceedings", "Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems", {"doi": "10.1145/3613904.3642902"}),
    "tao2026": ("C0596", "misc", "arXiv:2609.23936", {}),
    "wan2024": ("C0134", "inproceedings", "Proceedings of the 2024 Conference on Creativity and Cognition", {"doi": "10.1145/3635636.3664260", "authors": "Ruyuan Wan; Simret Araya Gebreegziabher; Toby Jia-Jun Li; Karla Badillo-Urquiola"}),
    "welzel2026": ("C0462", "inproceedings", "Proceedings of the 2026 ACM Conference on Fairness, Accountability, and Transparency", {"doi": "10.1145/3805689.3812389"}),
    "yang2025": ("C0374", "article", "British Journal of Educational Technology", {"doi": "10.1111/bjet.70031"}),
    "yukita2025": ("C0491", "misc", "arXiv:2505.16254", {}),
    "zhao2024": ("C0642", "inproceedings", "Proceedings of the International Conference on Learning Representations (ICLR)", {"doi": "10.48550/arXiv.2405.01470"}),
    "zhu2026": ("C0455", "article", "Frontiers in Psychology", {"doi": "10.3389/fpsyg.2026.1878629"}),
}

CLEAN = {"‐": "-", "’": "'", "—": "---", "–": "--", "&": r"\&", "_": r"\_"}


def clean(text):
    for old, new in CLEAN.items():
        text = text.replace(old, new)
    return " ".join(text.split())


def authors(raw):
    names = [" ".join(n.split()) for n in raw.split(";")] if ";" in raw else [n.strip() for n in raw.split(",")]
    fixed = []
    for name in names:
        if name.count(",") == 1:
            last, first = [p.strip() for p in name.split(",")]
            name = f"{first} {last}"
        fixed.append(name)
    return " and ".join(clean(n) for n in fixed if n)


def entry(key, row, kind, venue, extra):
    fields = {
        "author": authors(extra.get("authors", row["authors"])),
        "title": "{" + clean(row["title"]) + "}",
        "year": extra.get("year", row["year"]),
    }
    if kind == "article":
        fields["journal"] = venue
    elif kind == "inproceedings":
        fields["booktitle"] = venue
    else:
        fields["howpublished"] = venue
    for name in ("volume", "number", "pages", "doi"):
        if name in extra:
            fields[name] = extra[name].replace("_", r"\_") if name != "doi" else extra[name]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items())
    return f"@{kind}{{{key},\n{body}\n}}\n"


def main():
    rows = {r["paper_id"]: r for r in csv.DictReader(open(LIT / "papers.csv", encoding="utf-8"))}
    bib, table = [], ["key\tpaper_id\ttitle\tidentifier_in_papers_csv\tread_level"]
    for key in sorted(REFS):
        pid, kind, venue, extra = REFS[key]
        row = rows[pid]  # KeyError means the source is not in the registry
        bib.append(entry(key, row, kind, venue, extra))
        table.append("\t".join([key, pid, row["title"], row["identifier"], row["read_level"]]))
    (PAPER / "refs.bib").write_text("\n".join(bib), encoding="utf-8")
    (PAPER / "CITATIONS.tsv").write_text("\n".join(table) + "\n", encoding="utf-8")
    print(f"{len(REFS)} references written")


main()
