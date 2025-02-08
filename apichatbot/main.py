import joblib
from fastapi import FastAPI, Request
import re

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
