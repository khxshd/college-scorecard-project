"""Run the original Phase III analysis using the included cleaned datasets."""
import json
import os
import io
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    output = root / "generated"
    output.mkdir(exist_ok=True)
    notebook = json.loads((root / "PhaseIII_DesaiGajjar58.ipynb").read_text(encoding="utf-8"))
    started = False
    namespace = {"__name__": "__main__"}
    figure_count = 0

    def save_figure(*args, **kwargs):
        nonlocal figure_count
        figure_count += 1
        plt.gcf().savefig(output / f"visual{figure_count}.png", dpi=150, bbox_inches="tight")
        plt.close("all")

    plt.show = save_figure
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "markdown" and "SETUP FOR INSIGHTS" in source:
            started = True
        elif started and cell["cell_type"] == "code":
            exec(compile(source, f"PhaseIII_DesaiGajjar58.ipynb:cell-{index}", "exec"), namespace)
    if not started or figure_count != 3:
        raise RuntimeError("Expected the original analysis section and three charts.")
    namespace["state_data"].to_csv(output / "state_analysis.csv", index=False)
    export_tables(namespace, output)
    print(f"Saved {figure_count} charts, analysis tables, and model metrics in {output}")


def export_tables(namespace, output):
    """Export the submitted functions' results without changing their analysis."""
    import numpy as np
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.linear_model import LinearRegression

    with redirect_stdout(io.StringIO()):
        tuition = namespace["insight1"]()
        gap = namespace["insight2"]()
        debt_corr, ratio_corr, debt = namespace["insight3"]()
        coefficients, r2 = namespace["insight4"]()
        clusters = namespace["insight5"]()
    tuition.to_csv(output / "tuition_burden_top10.csv", index=False)
    gap.to_csv(output / "private_public_gap_top10.csv", index=False)
    debt.to_csv(output / "debt_burden_top10.csv", index=False)
    coefficients.to_csv(output / "regression_coefficients.csv", index=False)
    clusters.to_csv(output / "cluster_summary.csv")

    states = namespace["state_data"]
    features = ["avg_in_tuition", "avg_debt", "medianHouseholdIncome", "bachelors_percent"]
    assignments = states[["STABBR"] + features].dropna().copy()
    assignments["cluster"] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(assignments[features])
    assignments.to_csv(output / "cluster_assignments.csv", index=False)

    regression = states[["STABBR", "medianHouseholdIncome", "bachelors_percent", "avg_in_tuition"]].dropna().copy()
    x = regression[["medianHouseholdIncome", "bachelors_percent"]]
    model = LinearRegression().fit(x, regression["avg_in_tuition"])
    regression["predicted_tuition"] = model.predict(x)
    regression["residual"] = regression["avg_in_tuition"] - regression["predicted_tuition"]
    regression.to_csv(output / "regression_predictions.csv", index=False)

    admissions = states[["STABBR", "avg_debt", "avg_adm_rate"]].dropna().copy()
    slope, intercept = np.polyfit(admissions["avg_adm_rate"], admissions["avg_debt"], 1)
    admissions["trendline_debt"] = slope * admissions["avg_adm_rate"] + intercept
    admissions.to_csv(output / "admissions_debt_plot_data.csv", index=False)

    incomes = states[["STABBR", "medianHouseholdIncome", "graduate_percent"]].dropna().copy()
    width = (incomes["medianHouseholdIncome"].max() - incomes["medianHouseholdIncome"].min()) / 3
    low = incomes["medianHouseholdIncome"].min() + width
    high = incomes["medianHouseholdIncome"].max() - width
    incomes["income_type"] = np.where(incomes["medianHouseholdIncome"] <= low, "Low", np.where(incomes["medianHouseholdIncome"] <= high, "Middle", "High"))
    incomes.to_csv(output / "income_group_assignments.csv", index=False)
    incomes.groupby("income_type")["graduate_percent"].agg(["mean", "count"]).to_csv(output / "income_group_summary.csv")

    metrics = {
        "regression_r2_in_sample": float(r2),
        "regression_intercept": float(model.intercept_),
        "regression_observations": len(regression),
        "debt_graduation_correlation": float(debt_corr),
        "debt_income_graduation_correlation": float(ratio_corr),
        "debt_correlation_observations": int(states[["avg_debt", "avg_grad_rate", "debt_income_ratio"]].dropna().shape[0]),
        "cluster_observations": len(assignments),
        "cluster_features_scaled": False,
        "cluster_random_state": 42,
        "income_group_low_upper_bound": float(low),
        "income_group_middle_upper_bound": float(high),
    }
    (output / "model_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
