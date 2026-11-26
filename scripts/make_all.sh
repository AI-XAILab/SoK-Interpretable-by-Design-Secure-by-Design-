#!/usr/bin/env bash
# Reproduce every count, figure and worked-example number in the paper.
set -euo pipefail
cd "$(dirname "$0")"
python3 check_counts.py
python3 make_figures.py
python3 worked_examples.py | tee ../outputs/worked_examples_output.txt
