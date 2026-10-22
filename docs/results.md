# Analysis results and tables

These tables reproduce the original final notebook using the included cleaned snapshots. Displayed values are rounded; downloadable CSVs retain numerical precision. All 59 jurisdiction rows remain in the [merged state table](../results/state_analysis.csv). Regression and clustering each use 52 complete observations.

## Tuition relative to household income

Top ten jurisdictions by mean in-state tuition divided by median household income. These means span institution types; they are not individual net-price estimates.

| STABBR | avg_in_tuition | medianHouseholdIncome | tuition_income_ratio |
| --- | --- | --- | --- |
| VT | $41,645.86 | $78,024.00 | 53.38% |
| RI | $34,939.31 | $86,372.00 | 40.45% |
| IA | $23,501.79 | $73,147.00 | 32.13% |
| PR | $7,850.64 | $25,096.00 | 31.28% |
| ME | $22,339.45 | $71,773.00 | 31.13% |
| PA | $23,185.19 | $76,081.00 | 30.47% |
| MI | $21,122.83 | $71,149.00 | 29.69% |
| MA | $29,668.65 | $101,341.00 | 29.28% |
| CT | $24,987.17 | $93,760.00 | 26.65% |
| KY | $16,606.06 | $62,417.00 | 26.61% |

[Download ranking](../results/tuition_burden_top10.csv).

## Private nonprofit versus public tuition

The comparison uses public institutions (`CONTROL = 1`) and private nonprofit institutions (`CONTROL = 2`). Private for-profit institutions are excluded from this sector gap.

| STABBR | public_avg_tuition | private_avg_tuition | private_public_gap |
| --- | --- | --- | --- |
| VT | $11,283.33 | $49,926.55 | $38,643.21 |
| MA | $8,164.19 | $45,982.28 | $37,818.09 |
| CT | $13,850.94 | $47,239.11 | $33,388.17 |
| CA | $2,925.19 | $34,828.53 | $31,903.34 |
| MD | $6,669.43 | $38,279.74 | $31,610.30 |
| CO | $7,251.58 | $38,449.00 | $31,197.42 |
| OR | $7,752.46 | $38,581.30 | $30,828.84 |
| DC | $6,152.00 | $36,536.53 | $30,384.53 |
| RI | $10,906.67 | $40,485.31 | $29,578.64 |
| ME | $7,457.80 | $36,291.00 | $28,833.20 |

[Download ranking](../results/private_public_gap_top10.csv).

## Debt and completion

Across 52 complete observations, the correlation between average institutional debt and completion rate is **0.3576**. The correlation between debt relative to household income and completion rate is **-0.0116**, close to zero. These are aggregate associations.

| STABBR | avg_debt | avg_grad_rate | debt_income_ratio |
| --- | --- | --- | --- |
| PR | $8,058.71 | 54.35% | 32.11% |
| AL | $13,039.09 | 42.99% | 21.02% |
| SD | $14,162.73 | 52.85% | 19.56% |
| PA | $14,302.06 | 60.82% | 18.80% |
| WV | $10,780.14 | 59.80% | 18.61% |
| VT | $14,094.47 | 63.01% | 18.06% |
| MS | $9,889.41 | 52.27% | 18.01% |
| MO | $11,941.69 | 57.75% | 17.33% |
| NE | $12,984.65 | 56.11% | 17.32% |
| IN | $11,933.99 | 57.63% | 17.04% |

[Download debt ranking](../results/debt_burden_top10.csv).

## Regression

The model fits average in-state tuition using median household income and the adult fraction with a bachelor's degree or higher. The intercept is **-$1,247.05** and in-sample R² is **0.329141** across **52 observations**.

| feature | coefficient |
| --- | --- |
| medianHouseholdIncome | -0.004337 |
| bachelors_percent | 53387.196986 |

The attainment feature is a fraction: a 1 percentage point increase corresponds to about $533.87 in fitted tuition, holding income constant. These coefficients describe the fitted model; they do not establish causal effects or feature importance.

[Coefficients](../results/regression_coefficients.csv), [actual values, predictions, and residuals](../results/regression_predictions.csv), and [full model metrics](../results/model_metrics.json).

## K-means clusters

The original model uses three clusters, `random_state=42`, `n_init=10`, and unscaled tuition, debt, income, and attainment. Cluster labels are arbitrary. Dollar-valued features dominate distance calculations; the grouping is exploratory.

| cluster | avg_in_tuition | avg_debt | medianHouseholdIncome | bachelors_percent |
| --- | --- | --- | --- | --- |
| 0.000000 | $20,198.02 | $12,114.69 | $94,522.31 | 42.06% |
| 1.000000 | $11,396.34 | $10,080.66 | $56,321.78 | 26.83% |
| 2.000000 | $17,023.95 | $11,245.28 | $73,843.11 | 33.26% |

Cluster membership counts: 16, 9, and 27 for clusters 0, 1, and 2. [All 52 assignments](../results/cluster_assignments.csv) and [cluster averages](../results/cluster_summary.csv).

## Data behind the three figures

| Figure | Data and interpretation |
| --- | --- |
| [Admission rate versus debt](../figures/visual1.png) | [Jurisdiction values and fitted line](../results/admissions_debt_plot_data.csv). A descriptive relationship between averages. |
| [Income group versus advanced degree attainment](../figures/visual2.png) | [Income-group membership](../results/income_group_assignments.csv) and [group means/counts](../results/income_group_summary.csv). Groups use equal-width income intervals. |
| [Actual versus predicted tuition](../figures/visual3.png) | [Tuition values, fitted predictions, residuals](../results/regression_predictions.csv). Predictions use the model's training observations. |

Income-group upper bounds are $52,159.67 for Low and $79,223.33 for Middle; higher values are High. The original chart uses "graduates" for advanced degree attainment among adult residents.

| income_type | mean | count |
| --- | --- | --- |
| High | 17.64% | 19 |
| Low | 7.93% | 1 |
| Middle | 11.77% | 32 |

The [data guide](data.md) documents missingness, source periods, units, cleaning limitations, and interpretation. The [original poster](poster.pdf) and [presentation](presentation.pdf) preserve the submitted material.
