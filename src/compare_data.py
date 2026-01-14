import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

# --- SETUP & SECURITY ---
load_dotenv()
# Using os.getenv is professional - it allows the CI/CD environment to inject credentials
DB_URL = os.getenv("DB_URL") 
engine = create_engine(DB_URL)

def load_data_from_db():
    """Fetches reference and current data for comparison."""
    print("📡 Connecting to PostgreSQL...")
    reference = pd.read_sql("SELECT * FROM reference_data", engine)
    current = pd.read_sql("SELECT * FROM current_data", engine)
    return reference, current

def calculate_drift_logic(ref_mean, cur_mean, threshold=0.2):
    """
    Pure mathematical logic for drift detection. 
    Separated from I/O so it can be tested in CI/CD pipelines.
    """
    if ref_mean == 0: 
        return 0.0, False
    
    change_ratio = abs(cur_mean - ref_mean) / ref_mean
    is_drifted = change_ratio > threshold
    return round(change_ratio, 4), is_drifted

def generate_and_log_report(reference, current):
    """Orchestrates the drift analysis and logs results to the database."""
    THRESHOLD = 0.2
    timestamp_obj = datetime.now() 
    timestamp_str = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        f"DATA DRIFT REPORT", 
        f"Generated at: {timestamp_str}", 
        f"Threshold: {THRESHOLD * 100:.0f}%\n"
    ]
    
    drift_found = False
    history_records = []

    for column in reference.columns:
        # Skip metadata columns
        if 'timestamp' in column.lower() or 'id' in column.lower(): 
            continue
        
        # Calculate means
        ref_mean = reference[column].mean()
        cur_mean = current[column].mean()

        # Execute logic
        score, is_drifted = calculate_drift_logic(ref_mean, cur_mean, THRESHOLD)
        
        if is_drifted: 
            drift_found = True
        
        status = "DRIFT DETECTED" if is_drifted else "OK"

        # 1. Prepare text report line
        report_lines.append(
            f"{column}: ref={ref_mean:.2f}, cur={cur_mean:.2f}, "
            f"change={score*100:.1f}%, status={status}"
        )

        # 2. Prepare database record
        history_records.append({
            "execution_date": timestamp_obj,
            "feature_name": column,
            "drift_score": score,
            "is_drifted": is_drifted
        })

    # --- DATABASE LOGGING ---
    if history_records:
        print("💾 Logging results to 'drift_history' table...")
        history_df = pd.DataFrame(history_records)
        history_df.to_sql('drift_history', engine, if_exists='append', index=False)

    overall_status = "\nOVERALL STATUS: DRIFT DETECTED" if drift_found else "\nOVERALL STATUS: NO SIGNIFICANT DRIFT"
    report_lines.append(overall_status)
    
    return "\n".join(report_lines)

if __name__ == "__main__":
    try:
        # 1. Pull data
        ref, curr = load_data_from_db()
        
        # 2. Process & Log to DB
        report_content = generate_and_log_report(ref, curr)
        
        # 3. Output results
        print(report_content)
        
        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)
        with open("reports/drift_report.txt", "w") as f:
            f.write(report_content)
            
        print("\n✅ Success: Report saved and Database history updated.")
    except Exception as e:
        print(f"❌ Error during drift comparison: {e}")
