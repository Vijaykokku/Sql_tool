# 🚀 AI-Powered SQL Server Monitoring & Validation Agent  

## 👥 Team Details  
- **Team Name:** `select * from winners;`  
- **Members:**  
  - Vijay Babu Kokku  
  - Vaishnavi RS  
  - Pantangi Geetha Mohan  
- **Domain Category:** Intelligent Automation / AI for DataOps  
- **Demo Video:** SharePoint URL of MVP Demo  

---

## 🎯 Problem Statement  

Database administrators and data engineers spend significant time:

- Monitoring SQL Server Agent jobs  
- Investigating job failures  
- Writing repetitive monitoring queries  
- Validating tables and objects  
- Checking data consistency  
- Manually analyzing logs  

This process is:

- ❌ Manual  
- ❌ Reactive instead of proactive  
- ❌ Time-consuming  
- ❌ Dependent on SQL expertise  
- ❌ Not self-service  

There is no natural language interface to interact intelligently with SQL Server operations.

---

## 💡 Solution Overview  

We built an **AI-Powered SQL Server Monitoring & Validation Console** that:

1. Converts natural language questions into safe SQL queries  
2. Executes queries securely through a controlled API  
3. Retrieves SQL Agent job details and database insights  
4. Performs AI-based failure analysis  
5. Suggests optimization and remediation steps  

The system acts as an **Intelligent SQL Operations Assistant**.

---

## 🧠 Core Capabilities  

### 🧾 Natural Language to SQL Conversion
- Uses LLM to generate **SELECT-only SQL**
- Handles SQL Agent job monitoring queries
- Uses `msdb` system tables automatically

### 🔐 Secure SQL Execution Layer
- FastAPI-based backend
- Allows only `SELECT` queries
- Blocks `INSERT`, `UPDATE`, `DELETE`, `DROP`, `EXEC`
- Uses Trusted Connection authentication

### 📊 Intelligent Result Rendering
- Displays results in structured dataframe
- Maintains chat session history
- Supports dynamic query exploration

### 🤖 AI-Based Failure Analysis
- Analyzes job failure outputs
- Identifies root causes
- Suggests remediation steps
- Provides optimization insights

---

## 🏗 Architecture  

📁 **Architecture Diagram:** `/architecture/architecture.png`

---

## 🧩 System Components  

- **Frontend:** Streamlit  
- **LLM Integration:** Groq API (openai/gpt-oss-120b)  
- **Backend API:** FastAPI  
- **Database Connectivity:** pyodbc  
- **Data Processing:** Pandas  
- **Database:** SQL Server  

---

## 🔄 System Flow  

1. User enters natural language question  
2. LLM converts question into SAFE SELECT SQL  
3. SQL is displayed to user  
4. Streamlit sends SQL to FastAPI backend  
5. Backend validates query safety  
6. Query executes on SQL Server  
7. Results returned as JSON  
8. Streamlit renders results  
9. Optional AI analysis provides insights  

---

## 🛠 Tech Stack  

| Layer           | Technology                    |
|----------------|--------------------------------|
| Backend API    | FastAPI                       |
| Frontend UI    | Streamlit                     |
| AI Model       | openai/gpt-oss-120b (via Groq)|
| Database       | SQL Server                    |
| Connectivity   | pyodbc                        |
| Data Handling  | Pandas                        |
| Authentication | Windows Trusted Connection    |

---

## 📂 Project Structure  
```
SQL_TOOL/
│
├── README.md              
├── requirements.txt       
├── .env       
├── architecture/                   
|   |── architecture.png 
├── src/                   
│   ├── app.py  
|   |── chat_app_grok.py            
```

## ⚙️ Setup Instructions

## 1️ Verify Required Software

- Programming Language: Python
- Required Version: 3.10.0
- Package Manager: pip

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Vijaykokku/Sql_tool.git
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create `.env` file from `.env.example`

Example:

```
GROQ_API_KEY=
SQL_SERVER=
SQL_DATABASE=
USE_TRUSTED_CONNECTION=True
SQL_API_URL=http://localhost:8000/query
```

---

## ▶️ Entry Point

Run the backend application:

```bash
uvicorn app:app --reload
```
Backend runs at

```
http://127.0.0.1:8000
```

Run the Frontend application:

```bash
streamlit run chat_app_grok.py
```

Application will start at:

```
http://localhost:8501
```

---

## 🧪 How to Test

Once the application is configured and running, the system works as follows:

### 🔐 1️⃣ Secure Connection via .env Configuration

All credentials and connection details are securely passed through the `.env` file:

---

### 🤖 2️⃣ LLM + SQL Server Integration

Once started:

- The application connects to your configured SQL Server instance
- The LLM understands your database context dynamically
- It intelligently analyzes:
  - Databases
  - Tables
  - Views
  - Stored Procedures
  - Functions
  - SQL Server Agent Jobs
  - System tables (like `msdb`)

The LLM does **not modify** your database.  
It only generates **safe SELECT queries** for analysis and monitoring.

---

Example prompts:

- 	`List of Tables`
-	`check Table starts with'xyz'`
-	`check particular column is there are not`
-	`Count of particular Table`
  

---
### ⏱ 3️⃣ SQL Server Agent Job Monitoring

You can monitor SQL Agent Jobs using natural language:

- Track job runs for a specific date
- Check job success or failure trends
- View last execution status
- Identify long-running jobs
- Analyze failure reasons

Example prompts:

- `Show job status for today`
- `Did Job XYZ fail yesterday?`
- `Show last 7 days job execution summary`
- `Why is Job ABC failing frequently?`

The system automatically:
- Queries `msdb` system tables
- Retrieves job history
- Identifies failure patterns
- Provides AI-based root cause insights

---

## ⚠️ Known Limitations

- Requires valid Groq API key access
- Depends on LLM model availability via Groq
- LLM-generated SQL accuracy may vary
- Requires SQL Server ODBC driver installed
- Supports SELECT-only queries (no write operations) 

---

## 🔮 Future Improvements

- 🔐 **Role-Based Access Control (RBAC)**  
  Implement user authentication and authorization to restrict access based on roles (e.g., Admin, DBA, Analyst, Viewer).

- 🧠 **Query Parser-Based Validation**  
  Replace keyword-based filtering with a robust SQL parser to ensure deeper and more secure query validation.

- ⏱ **Query Timeout Control**  
  Add configurable execution time limits to prevent long-running or blocking queries.

- 📝 **Logging & Audit Table**  
  Maintain structured logs for:
  - User prompts  
  - Generated SQL queries  
  - Execution timestamps  
  - Query results status  
  - AI analysis outputs  

- 📧 **Alerting & Email Notifications**  
  Send automated alerts for:
  - Job failures  
  - Long-running jobs  
  - Missed schedules  
  - Data validation mismatches  

---

## 🏆 Project Highlights

- 🚀 **AI-Driven SQL Monitoring**  
  Transforms traditional SQL monitoring into an intelligent, conversational experience.

- 🏗 **Secure Microservice Architecture**  
  Clean separation between frontend (Streamlit) and backend (FastAPI) with controlled query execution.

- 💬 **Natural Language Interface for Database Operations**  
  Enables DBAs and data engineers to interact with SQL Server using simple English prompts.

- 🔍 **Enterprise-Grade Failure Analysis**  
  AI-powered insights into SQL Agent job failures with suggested remediation steps.

- 🧩 **Clear Separation of Concerns**  
  Modular project structure ensuring maintainability and scalability.

- 🛡 **Safe Query Enforcement**  
  Strict SELECT-only execution model to prevent unintended data modifications. 

---
