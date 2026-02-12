import random

def robo_controller():
    """
    RoboController 1.0
    Automatic robot movement with multiple obstacle detection
    using METERS as distance unit.
    """

    print("=" * 60)
    print("🤖 ROBOCONTROLLER 1.0 - AUTOMATIC ROBOT SIMULATOR")
    print("=" * 60)

    robot_name = input("\nEnter robot's name: ").strip()

    try:
        target_distance = float(input("Enter distance to target (meters): "))
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

        # -------- Decision Making --------
        if obstacle == "human":
            speed = 1.4  # m/s (slow walking speed)
            turn = random.choice(["Slight Left", "Slight Right"])
            action = f"Human detected → slowing down, turning {turn}"

        elif obstacle == "wall":
            speed = 0.8  # m/s (safe turning speed)
            turn = random.choice(["Left", "Right", "U-Turn"])
            action = f"Wall detected → avoiding obstacle, turning {turn}"

        else:
            speed = 4.0  # m/s (normal flow)
            turn = random.choice(["Straight", "Left", "Right"])
            action = "Path clear → moving smoothly"

        print(f"🚧 Obstacle: {obstacle.upper()} | ⚡ Speed: {speed} m/s")
        print(f"➡️  Action: {action}")

        # -------- Distance Calculation --------
        step = min(
            speed * random.uniform(0.4, 1.0),
            target_distance - distance_travelled
        )

        distance_travelled += step

        # -------- Store Checkpoint --------
        checkpoints.append({
            "number": checkpoint_no,
            "distance": round(distance_travelled, 2),
            "obstacle": obstacle,
            "turn": turn
        })

        print(
            f"📍 Checkpoint {checkpoint_no}: "
            f"{round(distance_travelled, 2)} m "
            f"(Obstacle: {obstacle}, Turn: {turn})\n"
        )

        checkpoint_no += 1

    # -------- Trip Summary --------
    avg_speed = round(distance_travelled / checkpoint_no, 2) if checkpoint_no > 1 else 0

    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + "🌟 FINAL TRIP SUMMARY".center(58) + "║")
    print("╠" + "═" * 58 + "╣")
    print(f"║ 🤖 Robot Name        : {robot_name:<32} ║")
    print(f"║ 🎯 Target Distance   : {target_distance} m{' ' * 24}║")
    print(f"║ 📏 Distance Travelled: {round(distance_travelled, 2)} m{' ' * 23}║")
    print(f"║ 📍 Total Checkpoints : {len(checkpoints):<32} ║")
    print(f"║ 📊 Avg Speed Factor  : {avg_speed} m/s{' ' * 21}║")
    print("╠" + "═" * 58 + "╣")

    for cp in checkpoints:
        line = (
            f"CP {cp['number']} | {cp['distance']} m | "
            f"Obstacle: {cp['obstacle']} | Turn {cp['turn']}"
        )
        print(f"║   • {line:<52} ║")

    print("╠" + "═" * 58 + "╣")
    print(f"║ 🚀 Mission Status : {mission_status:<36} ║")
    print("╚" + "═" * 58 + "╝")


if __name__ == "__main__":
    robo_controller()
