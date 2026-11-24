#!/usr/bin/env python3
"""Build paper/refs.bib and paper/CITATIONS.tsv from lit/papers.csv so every cited source is a registry record."""
import csv
import pathlib

PAPER = pathlib.Path(__file__).resolve().parents[1]
LIT = PAPER.parent / "lit"

# Authors, pages, volumes and publishers were checked against Crossref, DataCite and the arXiv API on 2026-11-23.
# key: (paper_id, entry type, venue, overrides). Venues, years and DOIs of published versions come from
# the reference list in lit/related_work.md, which took them from Crossref.
REFS = {
    "alam2026": ("S01", "misc", "arXiv:2609.13155", {}),
    "bastani2025": ("C0327", "article", "Proceedings of the National Academy of Sciences", {"volume": "122", "number": "26", "articleno": "e2422633122", "doi": "10.1073/pnas.2422633122"}),
    "bhat2026": ("C0490", "inproceedings", "Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems", {"pages": "1--21", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3772318.3791529"}),
    "chen2026": ("C0399", "article", "Frontiers in Psychology", {"volume": "17", "articleno": "1906199", "doi": "10.3389/fpsyg.2026.1906199"}),
    "contractor2026": ("C0227", "misc", "arXiv:2607.08849", {}),
    "davalos2026": ("C0184", "misc", "arXiv:2609.17883", {}),
    "flower1981": ("S05", "article", "College Composition and Communication", {"volume": "32", "number": "4", "pages": "365--387", "doi": "10.2307/356600"}),
    "jelson2026nirvana": ("C0453", "misc", "arXiv:2604.07344", {"authors": "Andrew Jelson; Daniel Manesh; Sangwook Lee; Alice Jang; Daniel Dunlap; Tamara Maddox; Young-Ho Kim; Sang Won Lee"}),
    "jelson2026chi": ("C0042", "inproceedings", "Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems", {"year": "2026", "pages": "1--26", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3772318.3791056"}),
    "joshi2025": ("C0649", "inproceedings", "Proceedings of the 7th ACM Conference on Conversational User Interfaces", {"year": "2025", "pages": "1--17", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3719160.3736608"}),
    "kim2025arcp": ("A027", "article", "Consumer Psychology Review", {"authors": "Tae Woo Kim; Umair Usman; Aaron M. Garvey; Adam Duhachek", "volume": "9", "number": "1", "pages": "142--164", "doi": "10.1002/arcp.70008"}),
    "kim2026fallacy": ("C0577", "misc", "arXiv:2604.14807", {}),
    "kosmyna2025": ("C0653", "misc", "arXiv:2506.08872", {"authors": "Nataliya Kosmyna; Eugene Hauptmann; Ye Tong Yuan; Jessica Situ; Xian-Hao Liao; Ashly Vivian Beresnitzky; Iris Braunstein; Pattie Maes"}),
    "lee2025": ("C0568", "inproceedings", "Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems", {"authors": "Hao-Ping Lee; Advait Sarkar; Lev Tankelevitch; Ian Drosos; Sean Rintel; Richard Banks; Nicholas Wilson", "pages": "1--22", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3706598.3713778"}),
    "maier2026": ("C0169", "misc", "arXiv:2609.20143", {}),
    "mysore2025": ("C0486", "inproceedings", "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing", {"pages": "16830--16857", "publisher": "Association for Computational Linguistics", "address": "Suzhou, China", "doi": "10.18653/v1/2025.emnlp-main.852"}),
    "padmakumar2026": ("S13", "misc", "arXiv:2605.29392", {"authors": "Vishakh Padmakumar; Lujain Ibrahim; Zora Zhiruo Wang; Jennifer Wang; Q. Vera Liao; Diyi Yang"}),
    "park2026": ("C0066", "inproceedings", "Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems", {"pages": "1--18", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3772318.3790276"}),
    "poquet2026": ("C0482", "incollection", "Mindful TEL: Learning Technologies Shaped with Intention", {"series": "Lecture Notes in Computer Science", "pages": "499--514", "publisher": "Springer", "address": "Cham", "doi": "10.1007/978-3-032-37979-5_34"}),
    "reza2025": ("C0133", "article", "Proceedings of the ACM on Human-Computer Interaction", {"volume": "9", "number": "7", "pages": "1--37", "doi": "10.1145/3757566"}),
    "risko2016": ("S15", "article", "Trends in Cognitive Sciences", {"volume": "20", "number": "9", "pages": "676--688", "doi": "10.1016/j.tics.2016.07.002"}),
    "shaw2026": ("A058", "misc", "SSRN working paper", {"doi": "10.2139/ssrn.6097646"}),
    "skulmowski2024": ("C0471", "article", "Educational Psychology Review", {"volume": "36", "number": "2", "articleno": "58", "doi": "10.1007/s10648-024-09894-x"}),
    "tankelevitch2024": ("C0579", "inproceedings", "Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems", {"authors": "Lev Tankelevitch; Viktor Kewenig; Auste Simkute; Ava Elizabeth Scott; Advait Sarkar; Abigail Sellen; Sean Rintel", "pages": "1--24", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3613904.3642902"}),
    "tao2026": ("C0596", "misc", "arXiv:2609.23936", {}),
    "wan2024": ("C0134", "inproceedings", "Proceedings of the 2024 Conference on Creativity and Cognition", {"pages": "504--511", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3635636.3664260", "authors": "Ruyuan Wan; Simret Araya Gebreegziabher; Toby Jia-Jun Li; Karla Badillo-Urquiola"}),
    "welzel2026": ("C0462", "inproceedings", "Proceedings of the 2026 ACM Conference on Fairness, Accountability, and Transparency", {"pages": "5941--5958", "publisher": "Association for Computing Machinery", "address": "New York, NY, USA", "doi": "10.1145/3805689.3812389"}),
    "yang2025": ("C0374", "article", "British Journal of Educational Technology", {"authors": "Kaixun Yang; Yixin Cheng; Linxuan Zhao; Mladen Raković; Zachari Swiecki; Dragan Gašević; Guanliang Chen", "volume": "57", "number": "2", "pages": "508--534", "doi": "10.1111/bjet.70031"}),
    "yukita2025": ("C0491", "misc", "arXiv:2505.16254", {"title": "Human-AI Writing as Distributed Cognition: Reassessing Collaborative Writing Theories in the Age of LLMs"}),
    "zhao2024": ("C0642", "inproceedings", "The Twelfth International Conference on Learning Representations (ICLR)", {"publisher": "OpenReview.net", "address": "Vienna, Austria", "doi": "10.48550/arXiv.2405.01470"}),
    "zhu2026": ("C0455", "article", "Frontiers in Psychology", {"volume": "17", "articleno": "1878629", "doi": "10.3389/fpsyg.2026.1878629"}),
}

# Standard method citations added on 2026-11-23 at Wayne's approval. They are not in lit/papers.csv;
# every field below was checked against Crossref on that date. Cited for the method only, not read for this project.
METHOD_REFS = {
    "cohen1960": ("article", {"author": "Jacob Cohen", "title": "{A Coefficient of Agreement for Nominal Scales}", "year": "1960", "journal": "Educational and Psychological Measurement", "volume": "20", "number": "1", "pages": "37--46", "doi": "10.1177/001316446002000104"}),
    "spearman1904": ("article", {"author": "C. Spearman", "title": "{The Proof and Measurement of Association between Two Things}", "year": "1904", "journal": "The American Journal of Psychology", "volume": "15", "number": "1", "pages": "72--101", "doi": "10.2307/1412159"}),
    "good2005": ("book", {"author": "Phillip I. Good", "title": "{Permutation, Parametric and Bootstrap Tests of Hypotheses}", "year": "2005", "edition": "3rd", "series": "Springer Series in Statistics", "publisher": "Springer", "address": "New York, NY", "doi": "10.1007/b138696"}),
    "efron1994": ("book", {"author": "Bradley Efron and R. J. Tibshirani", "title": "{An Introduction to the Bootstrap}", "year": "1994", "publisher": "Chapman and Hall/CRC", "address": "New York, NY", "doi": "10.1201/9780429246593"}),
    "abbott2000": ("article", {"author": "Andrew Abbott and Angela Tsay", "title": "{Sequence Analysis and Optimal Matching Methods in Sociology}", "year": "2000", "journal": "Sociological Methods \\& Research", "volume": "29", "number": "1", "pages": "3--33", "doi": "10.1177/0049124100029001001"}),
    "rousseeuw1987": ("article", {"author": "Peter J. Rousseeuw", "title": "{Silhouettes: A graphical aid to the interpretation and validation of cluster analysis}", "year": "1987", "journal": "Journal of Computational and Applied Mathematics", "volume": "20", "pages": "53--65", "doi": "10.1016/0377-0427(87)90125-7"}),
    "hsieh2005": ("article", {"author": "Hsiu-Fang Hsieh and Sarah E. Shannon", "title": "{Three Approaches to Qualitative Content Analysis}", "year": "2005", "journal": "Qualitative Health Research", "volume": "15", "number": "9", "pages": "1277--1288", "doi": "10.1177/1049732305276687"}),
}

NOTES = {
    "alam2026": "records conflict: lit/papers.csv says relevant sections, inference/sources.tsv says abstract only; the paper uses only what the abstract states",
    "bastani2025": "PMC abstract and introduction read at the literature stage (lit/citation_check.csv); PMC later blocked by reCAPTCHA, so the working-paper version on a third-party host was read for the rules (abstract, pp. 11, 13-15; cited pp. 2, 14, 15, per inference/sources.tsv); PNAS version of record not read in full",
    "contractor2026": "also pp. 22-23, 68, 77, per inference/sources.tsv",
    "jelson2026chi": "bib year is the published CHI 2026 version; registry year is the 2025 preprint",
    "yukita2025": "bib title is arXiv v4; v1-v3, read at screening, were titled Reassessing Collaborative Writing Theories and Frameworks in the Age of LLMs",
    "joshi2025": "bib year is the published 2025 version; registry year is the 2024 preprint",
}

CLEAN = {"‐": "-", "’": "'", "—": "---", "–": "--", "&": r"\&", "_": r"\_"}


def clean(text):
    for old, new in CLEAN.items():
        text = text.replace(old, new)
    return " ".join(text.split()).replace("AI -assisted", "AI-assisted")


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
        "title": "{" + clean(extra.get("title", row["title"])) + "}",
        "year": extra.get("year", row["year"]),
    }
    if kind == "article":
        fields["journal"] = venue
    elif kind in ("inproceedings", "incollection"):
        fields["booktitle"] = venue
    else:
        fields["howpublished"] = venue
    for name in ("series", "volume", "number", "articleno", "pages", "publisher", "address", "note", "doi"):
        if name in extra:
            fields[name] = extra[name].replace("_", r"\_") if name != "doi" else extra[name]
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items())
    return f"@{kind}{{{key},\n{body}\n}}\n"


def main():
    rows = {r["paper_id"]: r for r in csv.DictReader(open(LIT / "papers.csv", encoding="utf-8"))}
    bib, table = [], ["key\tpaper_id\ttitle\tidentifier_in_papers_csv\tread_level\tnote"]
    for key in sorted(set(REFS) | set(METHOD_REFS)):
        if key in METHOD_REFS:
            kind, fields = METHOD_REFS[key]
            body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items())
            bib.append(f"@{kind}{{{key},\n{body}\n}}\n")
            table.append("\t".join([key, "-", fields["title"].strip("{}"), "doi:" + fields["doi"], "not read; standard method citation", "not in lit/papers.csv; fields checked against Crossref 2026-11-23"]))
            continue
        pid, kind, venue, extra = REFS[key]
        row = rows[pid]  # KeyError means the source is not in the registry
        bib.append(entry(key, row, kind, venue, extra))
        table.append("\t".join([key, pid, row["title"], row["identifier"], row["read_level"], NOTES.get(key, "")]))
    (PAPER / "refs.bib").write_text("\n".join(bib), encoding="utf-8")
    (PAPER / "CITATIONS.tsv").write_text("\n".join(table) + "\n", encoding="utf-8")
    print(f"{len(REFS) + len(METHOD_REFS)} references written")


main()
