# maxmin3-records

Configurations of n = 31–50 points in 3D that minimise the ratio of the maximum to the minimum pairwise distance, extending Erich Friedman's table [Minimizing the Ratio of Maximum to Minimum Distance in 3 Dimensions](https://erich-friedman.github.io/packing/maxmin3/), which lists n ≤ 30. The page accepts extensions up to n = 50.

## Run

```sh
python3 -m venv .venv && .venv/bin/pip install numpy scipy pillow
./pipeline.sh 4          # 4 workers; resumable, skips n that have logs/done_nN
.venv/bin/python report.py
.venv/bin/python make_submission.py
```

`pipeline.sh` runs, for each n from 30 to 50, 6 minutes of random multistart (`search.py`) and 14 minutes of basin hopping (`improve.py`) per worker, then a 5-minute pass over every n that still fails the convergence sign. The whole run takes about 7.5 hours on 4 cores. Progress is in `logs/pipeline.log`.

## Files

| File | What it does |
|---|---|
| `common.py` | Objective, SLSQP polisher, and the `bests/` store (a file is replaced only by a strictly better configuration) |
| `search.py` | Random multistart |
| `improve.py` | Basin hopping from the current best, plus seeds from the best n−1 and n+1 sets |
| `verify.py` | Exact check: coordinates rounded to a 10⁻¹² grid, r² as an exact fraction, claim truncated at 5 decimals with the page's "+" |
| `report.py` | Value and contact counts per n; after stripping loose points, `active ≥ 3k−5` on the rigid core is a necessary sign of a local optimum (`report.txt` holds the current output) |
| `stress.py` | Tries to beat each n from its neighbours (delete a point from n+1, add one to n−1, re-optimise) |
| `symmetry.py` | Highest-order rotation axis of a configuration, for the page's symmetry note |
| `render.py` | Picture in the style of the existing page (min distances cyan, max distances red) |
| `make_submission.py` | `out/mmN.gif`, `out/coords_nN.txt` and `out/email.md` |

## Checks

The same code reproduces the page's current values for n = 12 (icosahedron, 3.61803), n = 13 (3.94714) and n = 30 (8.03171).

## Submission

Submitted to Erich Friedman on 2026-09-29, credited to Limin Ge (`out/email.md`, attachments in `out/maxmin3.zip`). Awaiting inclusion on the page.

## Article

How this came about, and what it says about doing "research" with AI: [OpenAI Published a Batch of Math Results, and So Did I](https://liminge.space/blog/openai-math-results-so-did-i) ([中文](https://liminge.space/cn/blog/openai-math-results-so-did-i)).
