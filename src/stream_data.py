import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import load_dotenv

# 1. Setup Connection
load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def simulate_production_data():
    try:
        # 2. Pull the Reference data to see what the 'normal' values look like
        ref_df = pd.read_sql("SELECT * FROM reference_data LIMIT 100", engine)
        
        if ref_df.empty:
            print("❌ No reference data found. Run migrate_to_db.py first!")
            return

        # 3. Generate 50 new rows of 'Current' data
        # We take the reference mean and add some random variation (noise)
        new_rows = []
        for _ in range(50):
            row = {}
            for col in ref_df.columns:
                if 'timestamp' in col.lower():
                    row[col] = datetime.now()
                else:
                    # Get the average of the reference column
                    avg = ref_df[col].mean()
                    # Add 5% to 15% random variation to simulate real-world movement
                    row[col] = avg + np.random.normal(0, avg * 0.1)
            new_rows.append(row)

        # 4. Push to 'current_data' table
        new_data_df = pd.DataFrame(new_rows)
        
        # We use if_exists='append' so the table grows over time!
        new_data_df.to_sql('current_data', engine, if_exists='append', index=False)
        
        print(f"🚀 Successfully injected 50 new rows into 'current_data' at {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"❌ Error streaming data: {e}")

if __name__ == "__main__":
    simulate_production_data()
