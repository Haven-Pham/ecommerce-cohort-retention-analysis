"""Execute the analysis notebook top to bottom and save it with fresh outputs.

    python scripts/run_notebook.py            # run and overwrite outputs
    python scripts/run_notebook.py --check    # run without saving (used in CI)
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "cohort_retention_profitability.ipynb"


def main() -> None:
    nb = nbformat.read(NOTEBOOK, as_version=4)
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
    if "--check" in sys.argv:
        print(f"OK: {NOTEBOOK.name} executed without errors")
        return
    nbformat.write(nb, NOTEBOOK)
    print(f"Executed and saved {NOTEBOOK.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
