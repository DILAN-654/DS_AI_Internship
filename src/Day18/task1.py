import sqlite3
import pandas as pd

conn=sqlite3.connect("internship.db")
df=pd.read_sql_query("SELECT * FROM INTERNS", conn)
print(f"All data Retreived :\n{df}")

gt5000=pd.read_sql_query("select * from interns where track='Data Science' and stipend>5000;",conn)
print(f"\nData Science interns with Greater than 5000 stipend: \n{gt5000}")

gp_track=pd.read_sql_query("select track, avg(stipend) as Average_Stipend from interns group by track",conn)
print(f"\nAverage Stipend for each track: \n{gp_track}")

cnt_track=pd.read_sql_query("SELECT track, COUNT(*) AS intern_count FROM interns GROUP BY track;",conn)
print(f"\Count of Employees / Interns for each track: \n{cnt_track}")



