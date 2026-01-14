import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv

# Load credentials
load_dotenv(find_dotenv())
engine = create_engine(os.getenv("DB_URL"))

with engine.connect() as conn:
    # 1. Delete the 'raw data' table that is blocking the UI
    conn.execute(text("DROP TABLE IF EXISTS drift_history;"))
    conn.commit()
    print("✅ Old 'drift_history' table deleted.")

print("🚀 Now running the monitor to create the CORRECT table...")
