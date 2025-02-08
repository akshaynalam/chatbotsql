from fastapi import FastAPI, Query
import sqlite3

app = FastAPI()

DB_PATH = "database/company.db"  # Define database path directly

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

@app.get("/employees/")
def get_employees(department: str = Query(..., description="Department Name")):
    """Fetch employees from a department."""
    sql = "SELECT * FROM Employees WHERE Department = ?"
    result = query_db(sql, (department,))
    return {"employees": result if result else "No employees found"}

@app.get("/manager/")
def get_manager(department: str = Query(..., description="Department Name")):
    """Fetch the manager of a department."""
    sql = "SELECT Manager FROM Departments WHERE Name = ?"
    result = query_db(sql, (department,))
    return {"manager": result[0][0] if result else "Department not found"}

@app.get("/hired_after/")
def get_employees_hired_after(date: str = Query(..., description="Hire Date (YYYY-MM-DD)")):
    """Fetch employees hired after a specific date."""
    sql = "SELECT * FROM Employees WHERE Hire_Date > ?"
    result = query_db(sql, (date,))
    return {"employees": result if result else "No employees found"}

@app.get("/salary_expense/")
def total_salary_expense(department: str = Query(..., description="Department Name")):
    """Calculate total salary expense for a department."""
    sql = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
    result = query_db(sql, (department,))
    return {"total_salary_expense": result[0][0] if result[0][0] else 0}
