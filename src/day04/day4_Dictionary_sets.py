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

#print(marks.get("math"))
#print(marks.get("history"))

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
n=int(input("Enter number of customers: "))
user_purchases={}

for _ in range(n):
    name=input("Enter customer name: ")
    amount=float(input("Enter purchase amount: "))
    user_purchases[name]=amount
print("Customer Purchases: ",user_purchases)

#ex5
top_customers=max(purchases, key=purchases.get)
print("Top spending customer:", top_customers)

#ex6
a={1,2,3}
b={3,4,5}
print("Union:", a | b)
print("Intersection:", a & b)
print(3 in a)


#task1_personalContact.py
contacts = {
    "Adithya": 9876543210,
    "Bhavish": 9123456789,
    "Karthik": 9988776655
}
print("Contact Book : ",contacts)

contacts["Dilan"] = 9606375321
print("Initial Contacts:", contacts)
contacts["Karthik"] = 7337863449
print("Updated Contacts:", contacts)

existing_contact = contacts.get("Karthik", "Contact not found")
missing_contact = contacts.get("Havyas", "Contact not found")

print("\n Existing Contact:", existing_contact)
print("\n Missing Contact:", missing_contact)

print("\nContact List:")
for name, phone in contacts.items():
    print(f"Contact: {name} | Phone: {phone}")



#task2_DuplicateCleaner.py
raw_logs = ["ID01", "ID02", "ID01", "ID05", "ID02", "ID08", "ID01"]
unique_logs = set(raw_logs)

is_prsent = "ID05" in unique_logs
print("is ID05 present in unique logs : ",is_prsent)

print("total log entries : ",len(raw_logs))
print("total unique log entries : ",len(unique_logs))

print("Unique log entries : ",unique_logs)

#task3_IntrestMatcher.py
friend_a = {"Python", "Cooking", "Hiking", "Movies"}
friend_b = {"Hiking", "Gaming", "Photography", "Python"}

print("INTEREST MATCHER - RECOMMENDATION ENGINE")
print(f"Friend A's Interests: {friend_a}")
print(f"Friend B's Interests: {friend_b}")

shared_interests = friend_a & friend_b
print(f"Shared Interests (& operator): {shared_interests}")
all_interests = friend_a | friend_b
print(f"All Unique Interests (| operator): {all_interests}")

unique_to_friend_a = friend_a - friend_b
print(f"Unique to Friend A (- operator): {unique_to_friend_a}")

print("\n" + "=" * 50)
print("RECOMMENDATION SUMMARY")
print("=" * 50)
print(f"Things they can do together: {shared_interests}")
print(f"Total unique interests to explore: {len(all_interests)} ({all_interests})")
print("=" * 50)
