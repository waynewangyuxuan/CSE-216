#!/usr/bin/env python3
"""Check the category palette for color-vision-deficiency separation and greyscale order (OKLab, Machado 2009 matrices)."""
import itertools
import math
import sys

PAL = {"SLb": "#D55E00", "SLr": "#F5B27A", "OFF": "#004E89", "AUG": "#56B4E9", "NEU": "#6E6E6E", "IND": "#E3E3E3"}
HATCHED = {"SLr", "NEU"}
CVD = {
    "normal": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def lin(hexc):
    return [((c / 255 / 1.055 + 0.055 / 1.055) ** 2.4 if c / 255 > 0.04045 else c / 255 / 12.92) for c in bytes.fromhex(hexc[1:])]


def apply(m, c):
    return [max(0, min(1, sum(a * b for a, b in zip(r, c)))) for r in m]


def oklab(c):
    r, g, b = c
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (x ** (1 / 3) for x in (l, m, s))
    return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s, 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s]


def main():
    worst = {}
    for name, m in CVD.items():
        worst[name] = min((100 * math.dist(oklab(apply(m, lin(PAL[a]))), oklab(apply(m, lin(PAL[b])))), a, b) for a, b in itertools.combinations(PAL, 2))
    lum = {k: round(0.2126 * lin(v)[0] + 0.7152 * lin(v)[1] + 0.0722 * lin(v)[2], 3) for k, v in PAL.items()}
    grey = sorted((116 * v ** (1 / 3) - 16, k) for k, v in lum.items())
    plain = [g for g in grey if g[1] not in HATCHED]
    gaps = min(b[0] - a[0] for a, b in zip(plain, plain[1:]))
    print("worst pair delta E (OKLab x 100):", {k: (round(v[0], 1), v[1], v[2]) for k, v in worst.items()})
    print("greyscale L*:", [(round(a, 1), b) for a, b in grey], "smallest gap among unhatched colors", round(gaps, 1))
    if gaps < 15 or min(v[0] for v in worst.values()) < 10:
        sys.exit("check_palette: fail")
    print("check_palette: ok")


main()
