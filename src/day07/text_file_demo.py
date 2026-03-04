file = open("sample.txt", "w")
file.write("Hello, this is a file handling example.")
file.close()

file = open("sample.txt", "r")
content = file.read()
print(content)
file.close()

with open("sample.txt", "r") as file:
    content = file.read()
    print(content)

try:
    with open("missing.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File not found. Please check the file name and try again.")

import csv
with open("data/Student.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)


import openpyxl
workbook = openpyxl.load_workbook("data/data.xlsx")
sheet = workbook.active
for row in sheet.iter_rows(min_row=2, values_only=True):
    print(row)

