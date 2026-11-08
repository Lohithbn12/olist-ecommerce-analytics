"""Run the whole pipeline: python run_all.py"""
import subprocess, sys
from pathlib import Path

py = Path(__file__).parent / "python"
for script in ["01_load_to_mysql.py", "02_build_marts.py", "03_rfm_segmentation.py"]:
    print(f"\n=== {script} ===")
    r = subprocess.run([sys.executable, script], cwd=py)
    if r.returncode != 0:
        sys.exit(f"{script} failed")
print("\nAll done. Now open Power BI Desktop and follow powerbi/POWERBI_GUIDE.md")
