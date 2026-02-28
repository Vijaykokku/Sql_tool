import os
import streamlit as st
import requests
from groq import Groq
import json
from dotenv import load_dotenv

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

# -------------------------------
# CONFIG FROM .env
# -------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SQL_API_URL = os.getenv("SQL_API_URL")


client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="SQL AI Console",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS (Professional UI)
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 2rem;
}
.stChatMessage {
    border-radius: 10px;
    padding: 10px;
}
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR (CONTROL PANEL)
# -------------------------------
with st.sidebar:
    st.title("WELCOME😉!")
    st.markdown("### Session Options")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.markdown("### YOU CAN TRY ME FOR..?")
    st.markdown("""                
    • Job Monitoring  
    • Object Validation  
    • Failure Analysis    
    """)

# -------------------------------
# HEADER
# -------------------------------
st.title("🧠 SQL Server Intelligence Console ")
st.markdown("Ask about jobs, databases, tables, validation, failures...")

st.divider()

# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
for idx, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        if message["type"] == "text":
            st.markdown(message["content"])

        elif message["type"] == "sql":
            st.markdown("##### 🧾 Generated SQL")
            st.code(message["content"], language="sql")

        elif message["type"] == "data":

            st.markdown("##### 📊 Query Result")
            st.dataframe(message["content"], use_container_width=True)

            analyze_key = f"analyze_{idx}"

            if st.button("🤖 Analyze & Suggest Improvements", key=analyze_key):

                with st.spinner("AI analyzing result..."):

                    analysis_prompt = f"""
                    You are a senior SQL Server monitoring and optimization expert.

                    Original Question:
                    {message.get('question', '')}

                    Query Result:
                    {json.dumps(message['content'], indent=2)}

                    Provide:
                    1. Key insights
                    2. Potential risks
                    3. Suggested next steps
                    4. Optimization ideas
                    5. If job failures exist, analyze root cause

                    Respond professionally.
                    """

                    analysis = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {"role": "system", "content": "You analyze SQL results and provide enterprise insights."},
                            {"role": "user", "content": analysis_prompt}
                        ],
                        temperature=0.2,
                        max_tokens=1024
                    )

                    analysis_text = analysis.choices[0].message.content

                st.markdown("##### 🧠 AI Insights")
                st.success(analysis_text)

        elif message["type"] == "error":
            st.markdown("##### ⚠ Error")
            st.error(message["content"])

st.divider()

# -------------------------------
# USER INPUT
# -------------------------------
user_input = st.chat_input("Type your SQL Server question here...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------
    # SQL GENERATION
    # -------------------------------
    prompt = f"""
    You are a senior SQL Server Database Engineer and Production DBA.

    You generate SQL queries ONLY for Microsoft SQL Server.

    STRICT RULES:

    1. Database Context:
    - Target database: SQL Server
    - System tables may include msdb.dbo.sysjobs, msdb.dbo.sysjobhistory, sysjobactivity, etc.
    - Always assume SQL Server syntax.

    2. Safety Rules:
    - NEVER generate INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER.
    - Generate READ-ONLY queries (SELECT only).
    - Do not modify data under any circumstances.

    3. SQL Server Intelligence Rules:
    - run_date and run_time columns in sysjobhistory are INT.
    - When performing arithmetic like run_date * 1000000 + run_time:
        ALWAYS CAST run_date to BIGINT to prevent arithmetic overflow.
        Example:
        CAST(run_date AS BIGINT) * 1000000 + run_time
    - Prefer using msdb.dbo.agent_datetime(run_date, run_time)
        instead of manual date math whenever possible.
    - Never assume automatic type promotion in SQL Server.

    4. Query Design Rules:
    - Optimize joins.
    - Use appropriate WHERE clauses.
    - Avoid SELECT *.
    - Use explicit column names.
    - Use proper aliasing.

    5. If user asked about sql jobs:
    - understand the question
    -if it is names of jobs give the names of enabled jobs
    -if it is list of jobs give the count of jobs with names.

    6. Job Monitoring Intelligence:
    - step_id = 0 represents job-level summary.
    - step_id > 0 represents step-level details.
    - run_status values:
        0 = Failed
        1 = Succeeded
        2 = Retry
        3 = Canceled
    - Always decode run_status into readable text using CASE.
    - use this query example for job status or  recent job run status.
        SELECT 
        j.name AS [Job Name],
        msdb.dbo.agent_datetime(jh.run_date, jh.run_time) AS [Last Run DateTime],
        CASE jh.run_status 
            WHEN 0 THEN 'Failed'
            WHEN 1 THEN 'Succeeded'
            WHEN 2 THEN 'Retry'
            WHEN 3 THEN 'Canceled'
            ELSE 'Unknown'
        END AS [Run Status],
        jh.run_duration AS [Duration (HHMMSS)]
        FROM msdb.dbo.sysjobs j
        JOIN msdb.dbo.sysjobhistory jh ON j.job_id = jh.job_id
        WHERE jh.step_id = 0 -- 0 represents the overall job outcome
        ORDER BY [Last Run DateTime] DESC;

    7.for getting error message for faile job run   
     use this query as example to fetch only error message 
     
        SELECT TOP 1
            h.message
        FROM msdb.dbo.sysjobhistory h
        WHERE h.run_status = 0   -- Failed
        AND h.step_id > 0      -- Ignore summary row
        ORDER BY h.run_date DESC, h.run_time DESC;
     YOU are a data base expert 
        

    8. Output Rules:
    - Return ONLY valid SQL query.
    - No explanation.
    - No markdown.
    - No comments.
    - No backticks.
    - Output must be directly executable in SQL Server.

    9. Performance Awareness:
    - Avoid unnecessary subqueries.
    - Avoid arithmetic overflow.
    - Avoid non-SARGable conditions.

    10.Parameter Handling:
   - Do NOT use SQL variables like @VariableName.
   - Do NOT use DECLARE.
   - Do NOT use parameter placeholders.
   - Always inject user-provided values directly into WHERE clauses.
   - Wrap string values in single quotes.

    You are operating in a production environment.
    Accuracy and safety are critical.

    Question:
    {user_input}
    """

    with st.spinner("Generating SQL..."):
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a SQL Server assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=2000
        )

    sql = completion.choices[0].message.content.strip()

    with st.chat_message("assistant"):
        st.markdown("##### 🧾 Generated SQL")
        st.code(sql, language="sql")

    st.session_state.messages.append({
        "role": "assistant",
        "type": "sql",
        "content": sql
    })

    # -------------------------------
    # EXECUTE QUERY
    # -------------------------------
    try:
        response = requests.get(SQL_API_URL, params={"sql": sql})
        data = response.json()

        if response.status_code != 200:
            with st.chat_message("assistant"):
                st.error(str(data))

            st.session_state.messages.append({
                "role": "assistant",
                "type": "error",
                "content": str(data)
            })
        else:
            with st.chat_message("assistant"):
                st.markdown("##### 📊 Query Result")
                st.dataframe(data, use_container_width=True)

            st.session_state.messages.append({
                "role": "assistant",
                "type": "data",
                "content": data,
                "question": user_input
            })

            st.rerun()

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(str(e))

        

