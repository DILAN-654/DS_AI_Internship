Students={"Name":"Adithya",
          "Rollno":2,
          "place":"puttur"}
print("Students Lists : ",Students)

#example1
student = {"name": "Amit",
           "age": 21,
           "course": "Engineering"}
print(student["name"])
student["age"] = 22
student["city"] = "Delhi"
print(student)


#ex2
marks = {"math": 80, "science": 75, "english": 85}

print(marks.get("math"))
print(marks.get("history"))

for subject, score in marks.items():
    print(subject, score)
print(marks)
marks.update({"History":100})
print("\nAfter updating values: ",marks)
marks.pop("math")
print("\n After poping values: ",marks)

#ex3
purchases={"Alice":250,"BOB":400,"Charlie":150}
for name,amount in purchases.items():
    print(f"{name} made a purchase of {amount}")

print("Total customers:", len(purchases))
print("Customers name : ",purchases.keys())

print("Alice's purchase amount:", purchases.get("Alice", 0))

#ex4
'''n=int(input("Enter number of customers: "))
user_purchases={}

for _ in range(n):
    name=input("Enter customer name: ")
    amount=float(input("Enter purchase amount: "))
    user_purchases[name]=amount
print("Customer Purchases: ",user_purchases)
'''

#ex5
top_customers=max(purchases, key=purchases.get)
print("Top spending customer:", top_customers)