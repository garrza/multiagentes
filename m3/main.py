import pygame
from traffic_light import TrafficLight
from vehicle import Vehicle
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Number of vehicles
h_vehicles = 5  # Horizontal vehicles
v_vehicles = 2  # Vertical vehicles

def draw_lanes():
    """Draw two perpendicular lanes on the screen."""
    lane_width = 50

    # Horizontal lane
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - lane_width // 2, WIDTH, lane_width))

    # Vertical lane
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - lane_width // 2, 0, lane_width, HEIGHT))

def main():
    run = True

    # Create traffic lights
    traffic_light_horizontal = TrafficLight((WIDTH // 2) + 40, (HEIGHT // 2) + 70)
    traffic_light_vertical = TrafficLight((WIDTH // 2) - 70, (HEIGHT // 2) - 40, rotation_angle=90)

    # Create horizontal vehicles
    vehicles_horizontal = []
    for i in range(h_vehicles):
        vehicles_horizontal.append(Vehicle(0, HEIGHT // 2 - 5, BLACK, direction='horizontal'))

    # Create vertical vehicles
    vehicles_vertical = []
    for i in range(v_vehicles):
        vehicles_vertical.append(Vehicle(WIDTH // 2 - 10, 700, WHITE, direction='vertical'))

    while run:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw lanes
        draw_lanes()

        # Update and draw traffic lights
        traffic_light_horizontal.update()
        traffic_light_horizontal.draw(screen)

        traffic_light_vertical.update()
        traffic_light_vertical.draw(screen)

        # Update and draw horizontal vehicles
        for vehicle in vehicles_horizontal:
            vehicle.move(traffic_light_horizontal)
            vehicle.draw(screen)

        # Update and draw vertical vehicles
        for vehicle in vehicles_vertical:
            vehicle.move(traffic_light_vertical)
            vehicle.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
