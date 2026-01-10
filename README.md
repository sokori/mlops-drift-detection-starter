# 🚀 MLOps Data Drift Monitoring System (V1.0)

A professional monitoring pipeline that detects statistical drift in production data using **PostgreSQL**, **Docker**, and **Python**.

## 🏗️ Architecture
- **Storage:** PostgreSQL (Running in Docker)
- **Infrastructure:** Docker Compose
- **Simulation:** Automated data injector (`stream_data.py`)
- **Monitoring:** Statistical drift detection engine (`compare_data.py`)

## 🛠️ Quick Start

### 1. Start the Database
```bash
docker compose up -d
2. Initialize Data
Move your baseline CSV data into the SQL Warehouse:


python3 migrate_to_db.py
3. Run Monitoring Loop
Simulate new incoming production data and check for drift:


# Inject 50 new rows into the 'current_data' table
python3 src/stream_data.py

# Analyze drift and log results to the 'drift_history' table
python3 src/compare_data.py
📊 Database Schema
The system maintains a drift_history table in PostgreSQL to track model health over time, allowing for long-term trend analysis.


---
