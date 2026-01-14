import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
engine = create_engine(os.getenv("DB_URL"))

with engine.connect() as conn:
    # This deletes the table so compare_data.py can build it correctly
    conn.execute(text("DROP TABLE IF EXISTS drift_history;"))
    conn.commit()
    print("✅ Table 'drift_history' dropped successfully!")
