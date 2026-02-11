import random

# ---- Robot Initialization ----
robot_name = input("Enter robot name: ")

distance_to_target = int(input("Enter distance to target (in meters): "))

obstacle_input = input("Is there an obstacle ahead? (yes/no): ").lower()
obstacle_ahead = True if obstacle_input == "yes" else False

# ---- Speed & Movement Decision ----
if distance_to_target <= 0:
    print("Invalid distance. Mission aborted.")
else:
    if obstacle_ahead:
        if distance_to_target < 20:
            speed = "Slow"
            movement = "Careful Forward"
        else:
            speed = "Medium"
            movement = "Obstacle Avoidance Mode"
    else:
        if distance_to_target > 50:
            speed = "Fast"
            movement = "Direct Forward"
        else:
            speed = "Medium"
            movement = "Normal Forward"

# ---- Journey Tracking ----
checkpoints = ["Start Point"]

# Simulate checkpoints
for i in range(1, 4):
    direction_change = random.choice(["Left", "Right", "Straight"])
    checkpoint = f"Checkpoint {i} - Turn {direction_change}"
    checkpoints.append(checkpoint)

# Optional update: remove last checkpoint (simulating reroute)
remove_last = input("Remove last checkpoint due to reroute? (yes/no): ").lower()
if remove_last == "yes":
    removed = checkpoints.pop()
    print(f"Removed: {removed}")

# Add final destination
checkpoints.append("Target Reached")

# ---- Trip Summary ----
print("\n===== ROBOT TRIP SUMMARY =====")
print(f"Robot Name        : {robot_name}")
print(f"Distance Travelled: {distance_to_target} meters")
print(f"Obstacle Detected : {obstacle_ahead}")
print(f"Speed Mode        : {speed}")
print(f"Movement Style    : {movement}")
print(f"Final Checkpoints : {checkpoints}")
print("===== MISSION COMPLETE =====")