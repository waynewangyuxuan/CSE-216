#!/usr/bin/env python3
"""Copy the paper's figures from analysis/figures; fig24 loses a title that overstates a result, the caption replaces it."""
import pathlib
import shutil

from PIL import Image

PAPER = pathlib.Path(__file__).resolve().parents[1]
SRC = PAPER.parent / "analysis" / "figures"
DST = PAPER / "figures"
COPY = ["fig16_archetype_sequences.png", "fig19_own_work_first.png", "fig23_dwell_latency.png", "fig25_log_triggers.png"]
CROP_TOP_PX = {"fig24_outcome.png": 46}


def main():
    DST.mkdir(exist_ok=True)
    for name in COPY:
        shutil.copyfile(SRC / name, DST / name)
    for name, top in CROP_TOP_PX.items():
        with Image.open(SRC / name) as image:
            image.crop((0, top, image.width, image.height)).save(DST / name)
    print("figures synced:", len(COPY) + len(CROP_TOP_PX))


main()
