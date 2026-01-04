import pandas as pd

# Load data
reference = pd.read_csv("data/reference_data.csv")
current = pd.read_csv("data/current_data.csv")

# Basic statistics
print("REFERENCE DATA STATS")
print(reference.describe())
print("\nCURRENT DATA STATS")
print(current.describe())

# Compare means
from datetime import datetime

THRESHOLD = 0.2  # 20%
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

report_lines = []
report_lines.append(f"DATA DRIFT REPORT")
report_lines.append(f"Generated at: {timestamp}")
report_lines.append(f"Threshold: {THRESHOLD * 100:.0f}%\n")

drift_found = False

for column in reference.columns:
    ref_mean = reference[column].mean()
    cur_mean = current[column].mean()

    if ref_mean == 0:
        continue

    change_ratio = abs(cur_mean - ref_mean) / ref_mean

    if change_ratio > THRESHOLD:
        status = "DRIFT DETECTED"
        drift_found = True
    else:
        status = "OK"

    report_lines.append(
        f"{column}: "
        f"reference={ref_mean:.2f}, "
        f"current={cur_mean:.2f}, "
        f"change={change_ratio*100:.1f}%, "
        f"status={status}"
    )

if drift_found:
    report_lines.append("\nOVERALL STATUS: DRIFT DETECTED")
else:
    report_lines.append("\nOVERALL STATUS: NO SIGNIFICANT DRIFT")

report_content = "\n".join(report_lines)

# Print to console
print(report_content)

# Save to file
with open("reports/drift_report.txt", "w") as f:
    f.write(report_content)


