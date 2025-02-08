import joblib
import json
import re
import sqlite3
from fastapi import FastAPI, Request, Query, HTTPException

app = FastAPI()

DB_PATH = "company.db"  # Database path
intent_model = joblib.load("intent_model.pkl")  # Load trained intent model

# Function to connect to database
def query_db(sql: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Function to classify intent
def classify_intent(query: str):
    return intent_model.predict([query])[0]

# Process natural language query and generate SQL query
def process_query(query: str):
    query = query.lower()
    intent = classify_intent(query)

    if intent == "get_employees_by_department":
        match = re.search(r"employees in (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return "SELECT * FROM Employees WHERE Department = ?", (department,)

    elif intent == "get_manager_by_department":
        match = re.search(r"manager of (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return "SELECT Manager FROM Departments WHERE Name = ?", (department,)

    elif intent == "get_employees_hired_after":
        match = re.search(r"hired after (\d{4}-\d{2}-\d{2})", query)
        if match:
            date = match.group(1)
            return "SELECT * FROM Employees WHERE Hire_Date > ?", (date,)

    elif intent == "get_total_salary_expense":
        match = re.search(r"salary expense for (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return "SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,)

    return None, None  # No valid query detected

# POST API: Accept JSON body
@app.post("/chat")
async def chatbot_post(request: Request):
    try:
        data = await request.json()
        query = data.get("query", "")
        if not query:
            raise ValueError("Query is missing or empty.")

        sql_query, params = process_query(query)
        if not sql_query:
            raise HTTPException(status_code=400, detail="I couldn't understand your query.")

        result = query_db(sql_query, params)
        return {"response": result if result else "No matching records found."}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format. Please send a valid JSON body.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# GET API: Accept query parameters
@app.get("/chat")
async def chatbot_get(query: str = Query(..., description="Enter your query")):
    sql_query, params = process_query(query)
    if not sql_query:
        raise HTTPException(status_code=400, detail="I couldn't understand your query.")

    result = query_db(sql_query, params)
    return {"response": result if result else "No matching records found."}
