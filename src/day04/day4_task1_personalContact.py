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

