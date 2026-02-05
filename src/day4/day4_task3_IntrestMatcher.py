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
