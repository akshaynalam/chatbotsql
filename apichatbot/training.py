import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

# Define the model save path
model_path = r"C:\Users\aksha\Desktop\sql\apichatbot\intent_model.pkl"

# Sample dataset for intent classification
data = {
    "query": [
        "Show me all employees in Sales",
        "Who is the manager of Engineering?",
        "List all employees hired after 2022-01-01",
        "What is the total salary expense for Marketing?",
        "How much do we pay in Engineering?",
        "Tell me the employees in Marketing",
        "Which employees joined after 2021-06-10?"
    ],
    "intent": [
        "get_employees_by_department",
        "get_manager_by_department",
        "get_employees_hired_after",
        "get_total_salary_expense",
        "get_total_salary_expense",
        "get_employees_by_department",
        "get_employees_hired_after"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Create a text classification pipeline
model = Pipeline([
    ("vectorizer", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train the model
model.fit(df["query"], df["intent"])

# Ensure directory exists
os.makedirs(os.path.dirname(model_path), exist_ok=True)

# Save the model
joblib.dump(model, model_path)

print(f"Model trained and saved at: {model_path}")
