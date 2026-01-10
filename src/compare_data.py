import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

# --- SETUP & SECURITY ---
load_dotenv()
# Using os.getenv is professional - it reads from your .env file
DB_URL = os.getenv("DB_URL") 
engine = create_engine(DB_URL)

def load_data_from_db():
    print("📡 Connecting to PostgreSQL...")
    reference = pd.read_sql("SELECT * FROM reference_data", engine)
    current = pd.read_sql("SELECT * FROM current_data", engine)
    return reference, current

def generate_and_log_report(reference, current):
    THRESHOLD = 0.2
    timestamp_obj = datetime.now() 
    timestamp_str = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [f"DATA DRIFT REPORT", f"Generated at: {timestamp_str}", f"Threshold: {THRESHOLD * 100:.0f}%\n"]
    drift_found = False
    history_records = [] # This will hold data for the SQL table

    for column in reference.columns:
        if 'timestamp' in column.lower(): continue
        
        ref_mean = reference[column].mean()
        cur_mean = current[column].mean()
        if ref_mean == 0: continue

        change_ratio = abs(cur_mean - ref_mean) / ref_mean
        status = "DRIFT DETECTED" if change_ratio > THRESHOLD else "OK"
        if status == "DRIFT DETECTED": drift_found = True

        # 1. Add to text report
        report_lines.append(f"{column}: ref={ref_mean:.2f}, cur={cur_mean:.2f}, change={change_ratio*100:.1f}%, status={status}")

        # 2. Add to SQL records list
        history_records.append({
            "execution_date": timestamp_obj,
            "feature_name": column,
            "drift_score": round(change_ratio, 4),
            "is_drifted": change_ratio > THRESHOLD
        })

    # --- THE MAGIC STEP: Create/Update the drift_history table ---
    print("💾 Logging results to 'drift_history' table...")
    history_df = pd.DataFrame(history_records)
    # if_exists='append' automatically CREATES the table if it doesn't exist
    history_df.to_sql('drift_history', engine, if_exists='append', index=False)

    overall_status = "\nOVERALL STATUS: DRIFT DETECTED" if drift_found else "\nOVERALL STATUS: NO SIGNIFICANT DRIFT"
    report_lines.append(overall_status)
    return "\n".join(report_lines)

if __name__ == "__main__":
    # 1. Pull
    ref, curr = load_data_from_db()
    
    # 2. Process & Log to DB
    report_content = generate_and_log_report(ref, curr)
    
    # 3. Output
    print(report_content)
    with open("reports/drift_report.txt", "w") as f:
        f.write(report_content)
    print("\n✅ Success: Report saved and Database history updated.")
