import pandas as pd
from sqlalchemy import create_engine
import os

# Connection to your running Docker container
DB_URL = "postgresql://sokori:postgres@localhost:5432/drift_data"
engine = create_engine(DB_URL)

def migrate():
    # Define the paths based on your file tree
    data_files = {
        'reference_data': 'data/reference_data.csv',
        'current_data': 'data/current_data.csv'
    }
    
    for table_name, file_path in data_files.items():
        if os.path.exists(file_path):
            print(f"Reading {file_path}...")
            df = pd.read_csv(file_path)
            # Push to SQL
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"✅ Table '{table_name}' created in PostgreSQL.")
        else:
            print(f"❌ Error: File {file_path} not found.")

if __name__ == "__main__":
    migrate()
