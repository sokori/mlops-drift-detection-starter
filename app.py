import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Database Connection
DB_URL = "postgresql://sokori:postgres@localhost:5432/drift_data"
engine = create_engine(DB_URL)

st.set_page_config(page_title="Data Drift Dashboard", page_icon="📊")

st.title("🚀 MLOps Data Drift Monitor")
st.markdown("This dashboard tracks statistical drift in production data vs. our training baseline.")

# 2. Fetch Data from Postgres
try:
    df = pd.read_sql("SELECT * FROM drift_history ORDER BY execution_date DESC", engine)

    if not df.empty:
        # --- NEW: SIDEBAR FILTER ---
        st.sidebar.header("Dashboard Settings")
        features = df['feature_name'].unique()
        selected_feature = st.sidebar.selectbox("Select Feature to Visualize", features)

        # Filter the dataframe based on the sidebar selection
        filtered_df = df[df['feature_name'] == selected_feature]
        # ----------------------------

        # 3. Key Metrics (Based on selected feature)
        latest = filtered_df.iloc[0]
        col1, col2, col3 = st.columns(3)
        
        col1.metric(f"Latest Score ({selected_feature})", f"{latest['drift_score']:.4f}")
        col2.metric("Data Points", len(filtered_df))

        status = "🔴 DRIFT" if latest['is_drifted'] else "🟢 HEALTHY"
        col3.write(f"### Status: {status}")

        # 4. Drift Trend Graph (Now using filtered data)
        st.subheader(f"Drift Trend for: {selected_feature}")
        st.line_chart(filtered_df.set_index('execution_date')['drift_score'])

        # 5. Raw Data Table (Showing all logs for transparency)
        st.subheader("All Detection Logs")
        st.dataframe(df)
    else:
        st.warning("Database is connected, but the drift_history table is empty.")

except Exception as e:
    st.error(f"Error: {e}")
