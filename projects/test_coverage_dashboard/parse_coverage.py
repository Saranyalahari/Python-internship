import json
import pandas as pd

def get_coverage_data():
    with open("coverage.json") as f:
        data = json.load(f)

    files = data["files"]

    coverage_list = []

    for file, details in files.items():
        percent = details["summary"]["percent_covered"]
        covered = details["summary"]["covered_lines"]
        total = details["summary"]["num_statements"]

        coverage_list.append({
            "File": file,
            "Coverage (%)": percent,
            "Covered Lines": covered,
            "Total Lines": total
        })

    df = pd.DataFrame(coverage_list)
    return df