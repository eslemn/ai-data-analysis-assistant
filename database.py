import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "vehicle_analysis.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            vehicle_id TEXT,
            health_score REAL,
            status TEXT,
            failure_risk_score REAL,
            risk_level TEXT,
            predicted_fault TEXT,
            maintenance_recommendation TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_results(df):
    conn = sqlite3.connect(DB_NAME)
    
    # Save required columns to match the DB schema
    cols_to_save = [
        "vehicle_id", "health_score", "status", 
        "failure_risk_score", "risk_level", 
        "predicted_fault", "maintenance_recommendation"
    ]
    
    # In case any column is missing, handle gracefully
    df_to_save = df[[col for col in cols_to_save if col in df.columns]].copy()
    
    # Add timestamp
    df_to_save['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write to SQL
    df_to_save.to_sql('analysis_results', conn, if_exists='append', index=False)
    conn.close()

def load_results():
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM analysis_results ORDER BY timestamp DESC"
    try:
        df = pd.read_sql(query, conn)
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df
