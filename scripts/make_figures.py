"""Regenerate the family-level evidence map (paper label fig:heatmap) and the map composition (fig:counts)."""
import csv
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "outputs"
OUT.mkdir(exist_ok=True)

COLUMNS = ["input", "poisoning", "semantic", "edit", "privacy", "verification"]
HEADERS = ["Input", "Pois.", "Sem.", "Edit", "Priv.", "Verif."]


def load(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def evidence_map():
    fam = load("family_map.csv")
    counts = Counter(r["family"] for r in load("evidence_map.csv"))
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    for i, row in enumerate(reversed(fam)):
        for j, col in enumerate(COLUMNS):
            v = row[col]
            if v == "full":
                ax.scatter(j, i, s=60, c="black")
            elif v == "partial":
                ax.scatter(j, i, s=60, facecolors="0.6", edgecolors="black")
            else:
                ax.scatter(j, i, s=60, facecolors="white", edgecolors="black")
        ax.text(len(COLUMNS) - 0.2, i, str(counts[row["family"]]), va="center", fontsize=7)
    ax.set_xticks(range(len(COLUMNS)), HEADERS, fontsize=7)
    ax.set_yticks(range(len(fam)), [r["label"] for r in reversed(fam)], fontsize=7)
    ax.axhline(1.5, color="black", lw=0.6)
    ax.set_xlim(-0.6, len(COLUMNS) + 0.2)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("filled = direct, grey = partial, open = none", fontsize=6)
    fig.tight_layout()
    fig.savefig(OUT / "fig_evidence_map.pdf")
    fig.savefig(OUT / "fig_evidence_map.png", dpi=200)


def composition():
    counts = Counter(r["family"] for r in load("evidence_map.csv"))
    order = ["concept", "prototype", "additive", "xbm", "posthoc", "privacy", "secondary"]
    labels = ["Concept", "Prototype", "Additive", "XBM", "Post-hoc", "Privacy", "Secondary"]
    shades = ["0.35"] * 4 + ["0.8"] * 2 + ["white"]
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    vals = [counts[k] for k in order]
    bars = ax.bar(labels, vals, color=shades, edgecolor="black", width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.3, str(v), ha="center", fontsize=6)
    ax.set_ylabel("# works", fontsize=7)
    ax.tick_params(labelsize=6)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "fig_composition.pdf")
    fig.savefig(OUT / "fig_composition.png", dpi=200)


if __name__ == "__main__":
    evidence_map()
    composition()
    print("wrote outputs/fig_evidence_map.* and outputs/fig_composition.*")
