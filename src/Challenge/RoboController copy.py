import pygame
import random
import sys
import time

# ---------- Initialize ----------
pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RoboController 1.0 - GUI Mode")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

# ---------- Colors ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)

# ---------- Robot ----------
robot_x = 100
robot_y = HEIGHT // 2
robot_size = 40

# ---------- Game Variables ----------
distance = 0
speed = 5
obstacle = "none"
status = "Moving"

# ---------- Main Loop ----------
running = True
obstacle_timer = 0

while running:
    screen.fill(WHITE)
    clock.tick(60)

    # ---------- Events ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------- Random Obstacle ----------
    obstacle_timer += 1
    if obstacle_timer > 120:  # change obstacle every 2 seconds
        obstacle = random.choice(["human", "wall", "none"])
        obstacle_timer = 0

        if obstacle == "human":
            speed = 2
            status = "Human ahead → Slow"

        elif obstacle == "wall":
            speed = 0
            status = "Wall ahead → STOP"

        else:
            speed = 5
            status = "Path clear → Flow"

    # ---------- Movement ----------
    robot_x += speed
    distance += speed * 0.05

    if robot_x > WIDTH:
        robot_x = 100

    # ---------- Draw Robot ----------
    pygame.draw.rect(
        screen,
        BLUE if obstacle == "none" else GREEN if obstacle == "human" else RED,
        (robot_x, robot_y, robot_size, robot_size)
    )

    # ---------- UI Text ----------
    texts = [
        f"Obstacle : {obstacle.upper()}",
        f"Speed    : {speed} km/h",
        f"Distance : {round(distance, 2)} km",
        f"Status   : {status}"
    ]

    for i, txt in enumerate(texts):
        label = font.render(txt, True, BLACK)
        screen.blit(label, (20, 20 + i * 30))

    pygame.display.update()
