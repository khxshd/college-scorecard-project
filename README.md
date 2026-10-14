# College Scorecard: College Costs and State Education Patterns

A CS2316 data science project by **Khush Desai and Bhakti Gajjar**, completed in Spring 2026.

The project combines institution-level College Scorecard records with state household income and educational attainment to explore tuition, student debt, admissions, graduation rates, and affordability across U.S. states.

## Project materials

- [Final analysis notebook](PhaseIII_DesaiGajjar58.ipynb): five insights, linear regression, K-means clustering, and three visualizations, with original saved outputs.
- [Data collection notebook](phaseII.ipynb): CSV parsing, Census API collection, HTML scraping, and cleaning.
- [One-page poster](docs/poster.pdf) and [presentation](docs/presentation.pdf).
- Three cleaned datasets: 6,429 institution records, 52 income records, and 52 educational attainment records.
- [Recorded presentation](https://youtu.be/fM9PhJFS2rw), as linked in the original notebook.

## Analysis

1. Rank states by average in-state tuition relative to median household income.
2. Compare average public and private tuition within states.
3. Examine debt, debt-to-income ratios, and graduation rates.
4. Model average in-state tuition using income and bachelor's degree attainment.
5. Group states into three clusters using tuition, debt, income, and attainment.

![Actual versus predicted tuition](figures/visual3.png)

## Run locally

Use Python 3.10 or later from the repository directory:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python run_analysis.py
```

The runner executes the original final notebook's analysis cells against the included cleaned CSVs. It skips Colab mounting and live data collection, and writes three charts and `state_analysis.csv` to `generated/`.

To inspect the notebooks interactively, run `jupyter lab`. The original final notebook begins with a Google Colab Drive mount and an absolute Drive directory. For local analysis, skip that mount and the data collection cells, and start at **SETUP FOR INSIGHTS** with the repository as the working directory.

To repeat the raw data collection, obtain `Most-Recent-Cohorts-Institution.csv` from College Scorecard and adjust the original file paths. Live API responses and Wikipedia table layouts can change; the bundled cleaned snapshots support reproducing the submitted analysis.

## Data sources

- [U.S. Department of Education College Scorecard](https://collegescorecard.ed.gov/data/): institution-level tuition, debt, admissions, SAT, and completion data.
- [U.S. Census ACS 5-year API](https://api.census.gov/data.html): median household income (`B19013_001E`) and margin of error (`B19013_001M`). The notebook queries 2023; its original source list links the 2022 variable documentation.
- [Wikipedia educational attainment by state](https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_educational_attainment): bachelor's and advanced degree attainment.

## Reproduction notes

The original notebook analysis and submitted PDFs are preserved. The local runner is an added convenience. The analysis uses state averages and measures associations rather than causal effects. K-means uses the original unscaled features, so its groups are sensitive to measurement units. The original raw-data parser has loop-variable mistakes in some admission/SAT imputation and rounding steps; the runner uses the submitted cleaned snapshots without changing them.

Notebook metadata identifying Colab sessions was removed. Source notebooks, extracted PDF text, repository files, and Git history were checked for credential patterns before upload. Videos, checkpoints, and the large raw CSV are excluded from Git.
