"""Recompute every count stated in the paper from data/evidence_map.csv and check it."""
import csv
import sys
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# Numbers stated in the paper (abstract, Sec. III, fig:heatmap, fig:counts, tab:evidence-app).
EXPECTED = {
    "total": 66,
    "group": {"built-in": 36, "boundary": 21, "secondary": 9},
    "family": {"concept": 20, "prototype": 7, "additive": 7, "xbm": 2,
               "posthoc": 11, "privacy": 10, "secondary": 9},
    "added_in_update": 5,
}


def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load("evidence_map.csv")
    ok = True
    ok &= check("total works", len(rows), EXPECTED["total"])
    ok &= check("works per group", dict(Counter(r["group"] for r in rows)), EXPECTED["group"])
    ok &= check("works per family", dict(Counter(r["family"] for r in rows)), EXPECTED["family"])
    ok &= check("works added in final update", sum(r["added_in_update"] == "1" for r in rows),
                EXPECTED["added_in_update"])
    keys = [r["bibtex_key"] for r in rows]
    ok &= check("no duplicate keys", len(keys) - len(set(keys)), 0)
    bib = (DATA / "references.bib").read_text(encoding="utf-8")
    missing = [k for k in keys if "{" + k + "," not in bib]
    ok &= check("every key present in references.bib", missing, [])
    not_coded = {r["bibtex_key"] for r in load("not_coded.csv")}
    ok &= check("coded and not-coded lists are disjoint", sorted(not_coded & set(keys)), [])
    sys.exit(0 if ok else 1)


def check(name, got, want):
    passed = got == want
    print(("PASS " if passed else "FAIL ") + f"{name}: {got}" + ("" if passed else f" (expected {want})"))
    return passed


if __name__ == "__main__":
    main()
