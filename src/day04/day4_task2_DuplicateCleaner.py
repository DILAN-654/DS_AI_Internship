raw_logs = ["ID01", "ID02", "ID01", "ID05", "ID02", "ID08", "ID01"]
unique_logs = set(raw_logs)

is_prsent = "ID05" in unique_logs
print("is ID05 present in unique logs : ",is_prsent)

print("total log entries : ",len(raw_logs))
print("total unique log entries : ",len(unique_logs))

print("Unique log entries : ",unique_logs)