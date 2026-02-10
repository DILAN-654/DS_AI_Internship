import random

def robo_controller():
    """
    RoboController 1.0: Simulate a robot's movement with decision making,
    checkpoint management, and trip summary.
    """
    
    # Get user inputs
    print("=" * 50)
    print("ROBOCONTROLLER 1.0 - Robot Movement Simulator")
    print("=" * 50)
    
    robot_name = input("\nEnter robot's name: ").strip()
    
    try:
        distance_to_target = float(input("Enter distance to target (km): "))
        if distance_to_target <= 0:
            print("Distance must be positive!")
            return
    except ValueError:
        print("Invalid distance input!")
        return
    
    has_obstacle = input("Is there an obstacle ahead? (yes/no): ").lower() in ['yes', 'y', 'true']
    
    # Initialize variables
    checkpoints = []
    distance_travelled = 0.0
    total_distance_to_travel = distance_to_target
    
    # Decision logic for speed and movement based on conditions
    print("\n" + "=" * 50)
    print("ANALYZING CONDITIONS AND DETERMINING SPEED...")
    print("=" * 50)
    
    # Nested if-elif-else for speed and movement decision
    if has_obstacle:
        if distance_to_target > 50:
            speed = 2  # Slow speed due to obstacle and long distance
            movement = "Cautious movement with frequent scans"
        elif distance_to_target > 20:
            speed = 3  # Medium-slow speed
            movement = "Moderate movement with safety checks"
        else:
            speed = 1  # Very slow speed for short distance with obstacle
            movement = "Very cautious, inch-by-inch movement"
    else:
        if distance_to_target > 50:
            speed = 8  # Fast speed, no obstacles, long distance
            movement = "Full speed ahead"
        elif distance_to_target > 20:
            speed = 5  # Medium speed
            movement = "Steady movement"
        else:
            speed = 3  # Moderate speed for short distance
            movement = "Normal movement"
    
    print(f"\nRobot Speed: {speed} km/h")
    print(f"Movement Type: {movement}")
    print(f"Obstacle Status: {'Yes - Taking extra precautions' if has_obstacle else 'No - Clear path'}")
    
    # Simulate robot movement with checkpoint management
    print("\n" + "=" * 50)
    print("STARTING JOURNEY...")
    print("=" * 50)
    
    checkpoint_number = 1
    
    while distance_travelled < total_distance_to_travel:
        # Calculate remaining distance
        remaining_distance = total_distance_to_travel - distance_travelled
        
        # Simulate movement for this segment
        segment_distance = min(speed * random.uniform(0.5, 1.5), remaining_distance)
        distance_travelled += segment_distance
        
        # Create checkpoint
        checkpoint = {
            'number': checkpoint_number,
            'distance': round(distance_travelled, 2),
            'status': 'Active'
        }
        checkpoints.append(checkpoint)
        print(f"Checkpoint {checkpoint_number}: {checkpoint['distance']} km reached")
        checkpoint_number += 1
        
        # Simulate random unexpected direction change
        if random.random() > 0.7:  # 30% chance of direction change
            direction_change = random.choice(['Left', 'Right', 'Slight deviation'])
            print(f"  ⚠️  Unexpected direction change: {direction_change}")
    
    # Interactive checkpoint management
    print("\n" + "=" * 50)
    print("CHECKPOINT MANAGEMENT")
    print("=" * 50)
    
    while True:
        print("\nCurrent checkpoints:")
        for cp in checkpoints:
            print(f"  Checkpoint {cp['number']}: {cp['distance']} km")
        
        print("\nOptions:")
        print("1. Add custom checkpoint")
        print("2. Remove last checkpoint")
        print("3. View trip summary")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            try:
                cp_distance = float(input("Enter checkpoint distance (km): "))
                if 0 < cp_distance <= total_distance_to_travel:
                    new_cp = {
                        'number': len(checkpoints) + 1,
                        'distance': cp_distance,
                        'status': 'Custom'
                    }
                    checkpoints.append(new_cp)
                    checkpoints.sort(key=lambda x: x['distance'])
                    # Re-number checkpoints
                    for i, cp in enumerate(checkpoints, 1):
                        cp['number'] = i
                    print("✓ Checkpoint added successfully!")
                else:
                    print("Please enter a valid distance within the target range.")
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        elif choice == '2':
            if checkpoints:
                removed = checkpoints.pop()
                print(f"✓ Removed checkpoint {removed['number']} at {removed['distance']} km")
                # Re-number checkpoints
                for i, cp in enumerate(checkpoints, 1):
                    cp['number'] = i
            else:
                print("No checkpoints to remove!")
        
        elif choice == '3':
            # Display trip summary
            print("\n" + "=" * 50)
            print("TRIP SUMMARY")
            print("=" * 50)
            
            print(f"\n🤖 Robot Name: {robot_name}")
            print(f"📏 Total Distance Travelled: {round(distance_travelled, 2)} km")
            print(f"🎯 Target Distance: {total_distance_to_travel} km")
            print(f"⚡ Robot Speed: {speed} km/h")
            print(f"🚧 Obstacle Status: {'Present - Navigation was careful' if has_obstacle else 'None - Clear path taken'}")
            
            print(f"\n📍 Final Checkpoints ({len(checkpoints)} total):")
            if checkpoints:
                for cp in checkpoints:
                    print(f"   • Checkpoint {cp['number']}: {cp['distance']} km ({cp['status']})")
            else:
                print("   No checkpoints recorded")
            
            # Journey statistics
            journey_time = round(distance_travelled / speed, 2) if speed > 0 else 0
            print(f"\n⏱️  Estimated Journey Time: {journey_time} hours")
            print(f"✓ Mission Status: {'COMPLETED' if distance_travelled >= total_distance_to_travel else 'IN PROGRESS'}")
            
            # Summary with f-strings
            summary = f"\n{'='*50}\n"
            summary += f"🤖 FINAL REPORT:\n"
            summary += f"Robot '{robot_name}' has travelled {distance_travelled:.2f}km out of {total_distance_to_travel}km\n"
            summary += f"Obstacle encountered: {has_obstacle}\n"
            summary += f"Total checkpoints: {len(checkpoints)}\n"
            summary += f"{'='*50}\n"
            
            print(summary)
        
        elif choice == '4':
            print("\nExiting RoboController. Safe travels! 🚀")
            break
        
        else:
            print("Invalid choice! Please enter 1-4.")


if __name__ == "__main__":
    robo_controller()
