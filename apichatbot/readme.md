**Chat Assistant - SQLite IntegrationOverview**
This chat assistant is a FastAPI-powered application that enables users to interact with an SQLite database using natural language queries. It processes user queries, converts them into SQL statements, and retrieves the relevant data from the database.
#How It WorksUser Input
The user sends a natural language query (e.g., "Who are the employees in the Sales department?").
Query Processing
The assistant parses the input and maps it to an SQL query based on predefined logic.
Database Interaction
The assistant executes the generated SQL query on an SQLite database containing Employees and Departments tables.
Response Generation
The retrieved data is formatted into a human-readable response and sent back to the user.
Technology StackBackend: FastAPI (Python)
Database: SQLite
Query Handling: Natural Language Processing (NLP) + SQL Query Generation
Deployment: Hosted on Render
Example Queries & SQL Mapping
User Query                                                       Generated SQL Query 
"List all employees in Sales."                             SELECT * FROM Employees WHERE Department = 'Sales';
"Who manages the Engineering department?"                  SELECT Manager FROM Departments WHERE Name = 'Engineering';
Setup & Running Locally
Clone the Repositorygit clone https://github.com/akshaynalam/chatbotsql.git
cd chatbotsql
2. Install Dependencies
pip install -r requirements.txt
3.Run the Assistant
uvicorn apichatbot.main:app --host 0.0.0.0 --port 8000
4.Test the APIOpen a browser and go to:
http://127.0.0.1:8000/docsUse the Swagger UI to interact with the API.
##Deployment on RenderThis 
project is deployed on Render, and it automatically updates with each push to GitHub.
Push Changes to GitHub
git add .
git commit -m "Updated chatbot logic"
git push origin mainGo to Render Dashboard → chatbot sql
Click "Manual Deploy" → "Clear Build Cache & Redeploy"
------------------------------------------------------------------------------------------------------------
