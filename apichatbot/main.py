from fastapi import FastAPI, Query, HTTPException
import sqlite3
import spacy
import subprocess

app = FastAPI()
DB_PATH = "company.db"  # Define database path

# Load NLP model



# Try loading the model, if not found, download it
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


def query_db(sql: str, params=()):
    """Executes SQL queries on the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI SQLite Chat Assistant!"}

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
