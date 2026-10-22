# Data sources and definitions

The repository preserves the project snapshots: published institutional statistics and state aggregates, not individual student records.

## Original College Scorecard snapshot

[`../data/raw/Most-Recent-Cohorts-Institution.csv.gz`](../data/raw/Most-Recent-Cohorts-Institution.csv.gz) contains the complete original CSV: **6,429 rows and 3,306 columns**. The downloaded archive was named `Most-Recent-Cohorts-Institution_10032025.zip`. This identifies the snapshot, not a single observation year for every variable.

The gzip file is about 23.5 MB, compared with 103,114,316 uncompressed bytes. Compression is lossless. Hashes and counts are in the [manifest](../data/manifest.json). Extract from the repository root:

```python
import gzip
import shutil

with gzip.open("data/raw/Most-Recent-Cohorts-Institution.csv.gz", "rb") as source:
    with open("Most-Recent-Cohorts-Institution.csv", "wb") as destination:
        shutil.copyfileobj(source, destination)
```

Decompressed SHA-256:

```text
6840020dc014f874ce497ba7517629ce72cf9c8726fc89a1639becb1522269bc
```

Source and official documentation: [College Scorecard data](https://collegescorecard.ed.gov/data/). Campus locations, institution identifiers, and aggregate demographic measures belong to this public dataset. Raw suppression markers are preserved.

## Cleaned institution snapshot

[`../cleaned_scorecard.csv`](../cleaned_scorecard.csv) has 6,429 rows and 11 fields.

| Field | Meaning and units |
| --- | --- |
| `UNITID` | Institution identifier |
| `INSTNM` | Institution name |
| `STABBR` | Institution state/jurisdiction abbreviation |
| `ZIP` | Institution ZIP code; treat as text |
| `CONTROL` | 1 public, 2 private nonprofit, 3 private for-profit |
| `TUITIONFEE_IN`, `TUITIONFEE_OUT` | In-state/out-of-state tuition and fees in dollars |
| `DEBT_MDN` | Institution-level median debt measure in dollars; analysis averages these medians |
| `ADM_RATE` | Admission rate as a fraction |
| `SAT_AVG` | Average SAT score |
| `GRAD_RATE` | 150%-of-normal-time completion measure: `C150_4` where available, otherwise `C150_L4` |

Cleaning normalizes missing-value tokens, converts numeric columns, trims names, normalizes jurisdiction/ZIP text, removes duplicate `UNITID` values, fills tuition/debt using state-by-control medians, and fills completion rates using state medians. A comment mentions a further state-only tuition fallback, but it is not implemented. Remaining blanks are retained.

The admission/SAT imputation and numeric rounding loops reuse `col` instead of their loop variable `row`. They do not perform the intended operations on all listed columns. The submitted snapshot is preserved. Do not assume all missing admissions/SAT values were imputed or all currency values rounded.

## Census income snapshot

[`../cleaned_census_income.csv`](../cleaned_census_income.csv) has 52 rows: 50 states, Washington, DC, and Puerto Rico.

| Field | Meaning |
| --- | --- |
| `stateName`, `STABBR` | Full jurisdiction name and join abbreviation |
| `medianHouseholdIncome` | `B19013_001E`, median household income in 2023 inflation-adjusted dollars |
| `incomeMarginOfError` | `B19013_001M`, published margin of error in dollars |
| `stateFips` | Two-character Census jurisdiction code |

The collection function queries the **2023 ACS 5-year API**: [variable definition](https://api.census.gov/data/2023/acs/acs5/variables/B19013_001E.json). The original source list links the 2022 variable catalog, but the executed code queries 2023. The analysis does not propagate the included income margins of error into uncertainty intervals.

## Educational attainment snapshot

[`../cleaned_html_data.csv`](../cleaned_html_data.csv) has 52 jurisdictions and these column groups:

| Columns | Meaning |
| --- | --- |
| `State or Territory`, `STABBR` | Full name and join abbreviation |
| `Population over the age of 25` | Population base from the source table |
| `With a High School Diploma or higher(Population)` / `(Percent)` | Count and fraction with high school attainment or higher |
| `With a Bachelor's Degree or higher(Population)` / `(Percent)` | Count and fraction with bachelor's attainment or higher |
| `With an Advanced Degree(Population)` / `(Percent)` | Count and fraction with advanced degrees |

Source: [Wikipedia educational attainment by state](https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_educational_attainment), which attributes the main table to Census ACS data. The CSV is the saved project snapshot. The live table, notes, and reference periods can change; the notebook does not pin a Wikipedia revision. Do not assume its period matches the income or Scorecard data.

Percent fields are fractions (`0.3463` means `34.63%`). The analysis field `graduate_percent` means **adult advanced degree attainment**. `avg_grad_rate` means **mean institutional completion rate**. They measure different things.

## Derived state table and exports

[`../results/state_analysis.csv`](../results/state_analysis.csv) retains 59 jurisdiction codes from institution data, including seven without complete income/attainment matches. A left join preserves these rows. Each analysis drops missing values in the columns it uses; regression and clustering each retain 52 observations.

| Field | Definition |
| --- | --- |
| `STABBR` | Jurisdiction abbreviation |
| `avg_in_tuition`, `avg_out_tuition` | Unweighted mean institutional tuition/fees |
| `avg_debt` | Unweighted mean of institution-level debt medians |
| `avg_adm_rate`, `avg_sat`, `avg_grad_rate` | Unweighted means of available institutional values |
| `school_count` | Institution record count, including institutions missing a particular metric |
| `public_avg_tuition` | Mean in-state tuition for `CONTROL = 1` |
| `private_avg_tuition` | Mean in-state tuition for `CONTROL = 2`; excludes for-profit institutions |
| `medianHouseholdIncome` | Joined Census income estimate |
| `bachelors_percent`, `graduate_percent` | Joined adult attainment fractions |
| `tuition_income_ratio` | `avg_in_tuition / medianHouseholdIncome` |
| `debt_income_ratio` | `avg_debt / medianHouseholdIncome` |
| `private_public_gap` | `private_avg_tuition - public_avg_tuition`, dollars |

Other exports provide rankings, correlations/model metrics, regression coefficients and predictions, cluster summaries/assignments, income-group membership, and the data behind each chart. `run_analysis.py` regenerates these in `generated/`.

## Interpretation and reuse

Tuition is a sticker-price measure, not net price after aid. Aggregate debt/income ratios combine different populations and are not individual debt-service ratios. Institution averages are not enrollment weighted. Completion measures combine institution types. Source years, missingness, imputation, and institution mix affect comparisons.

Regression R² and predictions use training observations; there is no held-out evaluation or causal design. K-means uses unscaled features and three clusters chosen by the project. Dollar-valued features dominate Euclidean distance; labels are arbitrary. Chart income groups are equal-width intervals, not equal-count groups.

Code, notebooks, and submitted reports are credited to Khush Desai and Bhakti Gajjar. Upstream materials retain their source terms; this repository does not grant a new blanket license to third-party materials. Attribute the linked sources when reusing data.
