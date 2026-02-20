import sqlite3
import pandas as pd

conn = sqlite3.connect("D:/1_1_DS_AI_Internship/sqlite/AIML_Dilan.db")
df = pd.read_sql_query("SELECT * FROM students", conn)
print(df)