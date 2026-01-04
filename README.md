# Data Drift Detection – MLOps V0

## Overview

Machine learning systems assume that future data looks like past data.
In real production environments, this assumption often breaks.

This project demonstrates a **simple, explainable data drift detection system**
that compares historical (reference) data with current data and reports
significant changes.

This is a foundational MLOps capability and a common real-world pain point.

---

## What Problem Does This Solve?

Data drift occurs when incoming data changes over time while systems continue
to operate normally.

This leads to:
- Silent model degradation
- Incorrect business decisions
- Delayed detection of issues

Traditional monitoring (CPU, memory, logs) does NOT detect this.

---

## What This Project Does

- Loads reference and current datasets
- Computes basic statistics per feature
- Measures percentage change in feature distributions
- Applies a configurable threshold
- Generates a human-readable drift report

No machine learning model is required.

---

## Project Structure

mlops-data-drift/
├── data/
│ ├── reference_data.csv
│ └── current_data.csv
├── src/
│ └── compare_data.py
├── reports/
│ └── drift_report.txt
└── README.md


---

## How to Run

### Requirements
- Python 3.8+
- pandas

Install dependencies:
```bash
pip install pandas
Run drift detection:


python3 src/compare_data.py
The drift report will be generated at:


reports/drift_report.txt
Example Output
==============
age: reference=35.00, current=62.44, change=78.4%, status=DRIFT DETECTED
income: reference=39800.00, current=62500.00, change=57.0%, status=DRIFT DETECTED

OVERALL STATUS: DRIFT DETECTED
