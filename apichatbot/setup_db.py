import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create Departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT UNIQUE NOT NULL,
    Manager TEXT NOT NULL
);
""")

# Create Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    Salary INTEGER NOT NULL,
    Hire_Date TEXT NOT NULL,
    FOREIGN KEY (Department) REFERENCES Departments(Name)
);
""")

# Insert sample data
departments = [
    ("Sales", "Alice"),
    ("Engineering", "Bob"),
    ("Marketing", "Charlie"),
]

employees = [
    ("Alice", "Sales", 50000, "2021-01-15"),
    ("Bob", "Engineering", 70000, "2020-06-10"),
    ("Charlie", "Marketing", 60000, "2022-03-20"),
]

# Insert data into Departments table
cursor.executemany("INSERT OR IGNORE INTO Departments (Name, Manager) VALUES (?, ?)", departments)

# Insert data into Employees table
cursor.executemany("INSERT OR IGNORE INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)", employees)

# Commit and close
conn.commit()
conn.close()

print("Database setup complete.")
