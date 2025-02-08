from fastapi import FastAPI, Query, HTTPException
import sqlite3
import spacy

app = FastAPI()
DB_PATH = "company.db"  # Define database path

# Load NLP model (efficiently)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")

# Predefined departments for faster lookup
DEPARTMENTS = {"Sales", "Engineering", "Marketing"}

def query_db(sql: str, params=()):
    """Executes SQL queries on the database with optimized connection handling."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

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

    return {"response": [dict(zip([col[0] for col in query_db("PRAGMA table_info(Employees);")], row)) for row in result]}

def process_nlp_query(query: str):
    """Converts natural language queries to SQL queries efficiently."""
    doc = nlp(query.lower())
    department = next((token.text.capitalize() for token in doc if token.text.capitalize() in DEPARTMENTS), None)

    if "employees" in query and department:
        return "SELECT * FROM Employees WHERE Department = ?", (department,)

    if "manager" in query and department:
        return "SELECT Manager FROM Departments WHERE Name = ?", (department,)

    if "hired after" in query:
        date = next((token.text for token in doc if token.like_date), None)
        if date:
            return "SELECT * FROM Employees WHERE Hire_Date > ?", (date,)

    if "total salary expense" in query and department:
        return "SELECT COALESCE(SUM(Salary), 0) FROM Employees WHERE Department = ?", (department,)

    return None, None  # If no valid query is detected
