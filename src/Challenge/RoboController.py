import random

def robo_controller():
    """
    RoboController 1.0
    Automatic robot movement with MULTIPLE obstacle detection
    during the journey.
    """

    print("=" * 60)
    print("🤖 ROBOCONTROLLER 1.0 - AUTOMATIC ROBOT SIMULATOR")
    print("=" * 60)

    robot_name = input("\nEnter robot's name: ").strip()

    try:
        target_distance = float(input("Enter distance to target (km): "))
        if target_distance <= 0:
            print("❌ Distance must be positive!")
            return
    except ValueError:
        print("❌ Invalid distance input!")
        return

    checkpoints = []
    distance_travelled = 0.0
    checkpoint_no = 1
    mission_status = "COMPLETED"

    print("\n🔍 Sensors activated...")
    print("🚀 Journey started...\n")

    # -------- Journey Loop --------
    while distance_travelled < target_distance:
        obstacle = random.choice(["human", "wall", "none"])

        # Decision making
        if obstacle == "human":
            speed = 5
            action = "Human detected → slowing down"

        elif obstacle == "wall":
            speed = 0
            action = "Wall detected → robot stopped"
            mission_status = "STOPPED (WALL ENCOUNTERED)"

        else:
            speed = 15
            action = "Path clear → moving smoothly"

        print(f"🚧 Obstacle: {obstacle.upper()} | ⚡ Speed: {speed} km/h")
        print(f"➡️  Action: {action}")

        if speed == 0:
            break

        step = min(
            speed * random.uniform(0.4, 1.0),
            target_distance - distance_travelled
        )

        distance_travelled += step
        turn = random.choice(["Left", "Right", "Straight"])

        checkpoints.append({
            "number": checkpoint_no,
            "distance": round(distance_travelled, 2),
            "obstacle": obstacle,
            "turn": turn
        })

        print(f"📍 Checkpoint {checkpoint_no}: {round(distance_travelled, 2)} km (Turn {turn})\n")

        checkpoint_no += 1

    # -------- Trip Summary --------
    avg_speed = round(distance_travelled / checkpoint_no, 2) if checkpoint_no > 1 else 0

    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + "🌟 FINAL TRIP SUMMARY".center(58) + "║")
    print("╠" + "═" * 58 + "╣")
    print(f"║ 🤖 Robot Name        : {robot_name:<32} ║")
    print(f"║ 🎯 Target Distance   : {target_distance:<32} ║")
    print(f"║ 📏 Distance Travelled: {round(distance_travelled, 2):<32} ║")
    print(f"║ 📍 Total Checkpoints : {len(checkpoints):<32} ║")
    print(f"║ 📊 Avg Speed Factor  : {avg_speed:<32} ║")
    print("╠" + "═" * 58 + "╣")

    if checkpoints:
        for cp in checkpoints:
            line = (
                f"CP {cp['number']} | {cp['distance']} km | "
                f"Obstacle: {cp['obstacle']} | Turn {cp['turn']}"
            )
            print(f"║   • {line:<52} ║")
    else:
        print("║   • No checkpoints recorded                          ║")

    print("╠" + "═" * 58 + "╣")
    print(f"║ 🚀 Mission Status : {mission_status:<36} ║")
    print("╚" + "═" * 58 + "╝")


if __name__ == "__main__":
    robo_controller()
