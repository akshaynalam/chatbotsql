<<<<<<< HEAD
<<<<<<< HEAD
import joblib
from fastapi import FastAPI, Request
import re
=======
from fastapi import FastAPI, Query, HTTPException
import sqlite3
import spacy
import subprocess
>>>>>>> 89efd5d1f8f4d46b631f7e2b182613f0a32d0642
=======
import joblib
from fastapi import FastAPI, Request
import re
>>>>>>> 6871958e791f8949026c10dbed27c10e4a6e222c

app = FastAPI()

# Load the trained model
intent_model = joblib.load("intent_model.pkl")

# Function to classify intent
def classify_intent(query):
    intent = intent_model.predict([query])[0]
    return intent

@app.post("/chat")
async def chatbot(request: Request):
    data = await request.json()
    query = data.get("query", "").lower()
    intent = classify_intent(query)

    if intent == "get_employees_by_department":
        match = re.search(r"employees in (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return get_employees_by_department(department)

<<<<<<< HEAD
<<<<<<< HEAD
# Load the trained model
intent_model = joblib.load("intent_model.pkl")
=======
>>>>>>> 89efd5d1f8f4d46b631f7e2b182613f0a32d0642

# Function to classify intent
def classify_intent(query):
    intent = intent_model.predict([query])[0]
    return intent

@app.post("/chat")
async def chatbot(request: Request):
    data = await request.json()
    query = data.get("query", "").lower()
    intent = classify_intent(query)

<<<<<<< HEAD
    if intent == "get_employees_by_department":
        match = re.search(r"employees in (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return get_employees_by_department(department)

    elif intent == "get_manager_by_department":
        match = re.search(r"manager of (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return get_manager_by_department(department)

    elif intent == "get_employees_hired_after":
        match = re.search(r"hired after (\d{4}-\d{2}-\d{2})", query)
        if match:
            date = match.group(1)
            return get_employees_hired_after(date)

    elif intent == "get_total_salary_expense":
        match = re.search(r"salary expense for (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return get_total_salary_expense(department)

    return {"response": "I'm not sure I understand. Try asking about employees, managers, hire dates, or salary expenses."}
=======
@app.get("/chat/")
def chat(query: str = Query(..., description="Enter a natural language query")):
    """Process a natural language query and return database results."""
    sql_query, params = process_nlp_query(query)
    
    if not sql_query:
        raise HTTPException(status_code=400, detail="I couldn't understand your query.")

    result = query_db(sql_query, params)
    
    if not result:
        return {"response": "No matching records found."}
    
    return {"response": result}

def process_nlp_query(query: str):
    """Converts natural language queries to SQL queries."""
    doc = nlp(query.lower())

    # Detect department name
    department = None
    for token in doc:
        if token.text.capitalize() in ["Sales", "Engineering", "Marketing"]:
            department = token.text.capitalize()
            break

    # Identify query intent
    if "employees" in query and department:
        return "SELECT * FROM Employees WHERE Department = ?", (department,)
    
    elif "manager" in query and department:
        return "SELECT Manager FROM Departments WHERE Name = ?", (department,)
    
    elif "hired after" in query:
        for token in doc:
            if token.like_date:
                return "SELECT * FROM Employees WHERE Hire_Date > ?", (token.text,)

    elif "total salary expense" in query and department:
        return "SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,)

    return None, None  # If no valid query is detected
>>>>>>> 89efd5d1f8f4d46b631f7e2b182613f0a32d0642
=======
    elif intent == "get_manager_by_department":
        match = re.search(r"manager of (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return get_manager_by_department(department)

    elif intent == "get_employees_hired_after":
        match = re.search(r"hired after (\d{4}-\d{2}-\d{2})", query)
        if match:
            date = match.group(1)
            return get_employees_hired_after(date)

    elif intent == "get_total_salary_expense":
        match = re.search(r"salary expense for (\w+)", query)
        if match:
            department = match.group(1).capitalize()
            return get_total_salary_expense(department)

    return {"response": "I'm not sure I understand. Try asking about employees, managers, hire dates, or salary expenses."}
>>>>>>> 6871958e791f8949026c10dbed27c10e4a6e222c
