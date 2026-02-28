import os
import pyodbc
import pandas as pd
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# -------------------------------
# LOAD ENV VARIABLES
# -------------------------------
load_dotenv()

app = FastAPI()

# -------------------------------
# CONFIG FROM .env
# -------------------------------
SERVER = os.getenv("SQL_SERVER")
DATABASE = os.getenv("SQL_DATABASE")
# USERNAME = os.getenv("SQL_USERNAME")
# PASSWORD = os.getenv("SQL_PASSWORD")
USE_TRUSTED = os.getenv("USE_TRUSTED_CONNECTION", "True").lower() == "true"

# -------------------------------
# BUILD CONNECTION STRING
# -------------------------------
if USE_TRUSTED:
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )
else:
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        # f"UID={USERNAME};"
        # f"PWD={PASSWORD};"
    )

# -------------------------------
# SAFETY CHECK
# -------------------------------
def is_safe_query(sql: str):
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "EXEC"]
    sql_upper = sql.upper()
    return not any(word in sql_upper for word in forbidden)

# -------------------------------
# API ENDPOINT
# -------------------------------
@app.get("/query")
def run_query(sql: str):
    if not is_safe_query(sql):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")

    try:
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))