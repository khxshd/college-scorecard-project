"""Run the original Phase III analysis using the included cleaned datasets."""
import json
import os
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
    print(f"Saved {figure_count} charts and state_analysis.csv in {output}")


if __name__ == "__main__":
    main()
