# Artifact: SoK — Interpretable by Design, Secure by Design?

Artifact for the IEEE EuroS&P 2027 submission *"SoK: Interpretable by Design, Secure by Design? Security Properties of Models That Explain Themselves"*.

It contains the 66-work evidence map with per-work coding, the family-level evidence map, the codebook, the list of cited works that were not coded, and scripts that reproduce every count, both data figures, and every number in the worked examples.

## Contents

```
data/
  evidence_map.csv     66 coded works: family, group, evidence type, stage, properties, takeaway
  family_map.csv       family-level evidence map (paper: fig:heatmap, tab:evidence-app)
  not_coded.csv        cited works deliberately not coded (background, method definitions)
  references.bib       BibTeX for every key used above
codebook.md            coding definitions
scripts/
  check_counts.py      recomputes all counts in the paper (66 / 36 / 21 / 9; per family) and checks them
  make_figures.py      evidence map and map composition         -> outputs/fig_evidence_map.*, fig_composition.*
  worked_examples.py   every number in Examples 1-2 and the extraction check of Prop. 2 (numpy only)
  make_all.sh          runs everything
outputs/               generated files (recreated by make_all.sh)
```

## Reproducing

Requires Python 3.9+.

```bash
pip install -r requirements.txt
bash scripts/make_all.sh
```

`check_counts.py` exits with a non-zero status if any count in the data disagrees with the paper. `worked_examples.py` uses synthetic parameters only; its output is saved to `outputs/worked_examples_output.txt`.

## Counts

| Group | Family | Works |
|---|---|---|
| built-in (36) | concept / SENN | 20 |
| | prototype | 7 |
| | additive | 7 |
| | explanation bottleneck | 2 |
| boundary (21) | post-hoc | 11 |
| | privacy / extraction | 10 |
| secondary (9) | surveys and SoKs | 9 |

Five works (`added_in_update = 1`) were added in the final update of the map.

## Contesting a coding decision

Change the row in `data/evidence_map.csv` or `data/family_map.csv` and rerun `make_all.sh`; the count check shows which statements in the paper would be affected. Counts describe the coded map, not field-wide prevalence, and attack success rates are never pooled across threat models.

## License

Code: MIT (`LICENSE`). Data and codebook: CC BY 4.0 (`LICENSE-DATA`).
