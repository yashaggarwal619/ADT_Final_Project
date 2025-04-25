import sql_query_generator
import sqlite3
import pandas as pd

def query_database(query):
    try:
        conn = sqlite3.connect("student_database.db")  # Replace with your SQLite database file
        df = pd.read_sql_query(query, conn)  # Fetch data as DataFrame
        conn.close()
        return df
    except Exception as e:
        return f"Error: {e}"

types = ["Insert","Update","Delete","View"]

Subject_name = ["Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "History",
    "Economics",
    "Psychology",
    "Political Science",
    "Philosophy"]

subjects_id = [
    "SUBJ001",
    "SUBJ002",
    "SUBJ003",
    "SUBJ004",
    "SUBJ005",
    "SUBJ006",
    "SUBJ007",
    "SUBJ008",
    "SUBJ009",
    "SUBJ010",
    "SUBJ6969"
]

pormpt=""
prompts=[]
for sid in Subject_name:
    prompt="I want to view top ten performers of subject " + "SUBJ006" + "."
    result=sql_query_generator.return_sql_query(prompt)
    prompts.append([result['SQL Query'],sid])


for p in prompts:
    ans = query_database(p[0])
    if ans.shape[0] == 0:
        print(p[0])
    else:
        print(ans)
    
    print(p[1])