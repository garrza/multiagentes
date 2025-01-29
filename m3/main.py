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

# Vehicle spawn probability (adjust these to control spawn rates)
H_SPAWN_RATE = 0.01  # 1% chance per frame (~0.6 vehicles per second at 60 FPS)
V_SPAWN_RATE = 0.01  # 1% chance per frame (~0.6 vehicles per second at 60 FPS)

# Vehicle lists
vehicles_horizontal = []
vehicles_vertical = []

def draw_lanes():
    """Draw two perpendicular lanes on the screen."""
    lane_width = 50

    # Horizontal lane
    pygame.draw.rect(screen, GRAY, (0, HEIGHT // 2 - lane_width // 2, WIDTH, lane_width))

    # Vertical lane
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - lane_width // 2, 0, lane_width, HEIGHT))

def spawn_vehicle():
    """Randomly spawns vehicles at defined positions based on probability."""
    # Spawn horizontal vehicles from the left
    if random.random() < H_SPAWN_RATE:
        new_vehicle = Vehicle(0, HEIGHT // 2 - 5, BLACK, 'horizontal', vehicles_horizontal)
        vehicles_horizontal.append(new_vehicle)

    # Spawn vertical vehicles from the bottom
    if random.random() < V_SPAWN_RATE:
        new_vehicle = Vehicle(WIDTH // 2 - 10, HEIGHT, WHITE, 'vertical', vehicles_vertical)
        vehicles_vertical.append(new_vehicle)

def main():
    run = True

    # Create traffic lights
    traffic_light_vertical = TrafficLight((WIDTH // 2) + 40, (HEIGHT // 2) + 70)
    traffic_light_horizontal = TrafficLight((WIDTH // 2) - 70, (HEIGHT // 2) - 40, rotation_angle=90)
    
    # Connect traffic lights to each other
    traffic_light_vertical.set_other_light(traffic_light_horizontal)
    traffic_light_horizontal.set_other_light(traffic_light_vertical)

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
        traffic_light_vertical.update()
        
        # Clean up vehicles that have left the screen
        vehicles_horizontal[:] = [v for v in vehicles_horizontal if v.x < WIDTH]
        vehicles_vertical[:] = [v for v in vehicles_vertical if v.y > 0]

        # Draw traffic lights after cleaning up vehicles
        traffic_light_horizontal.draw(screen)
        traffic_light_vertical.draw(screen)

        # Spawn new vehicles
        spawn_vehicle()

        # Update and draw horizontal vehicles
        for vehicle in vehicles_horizontal:
            vehicle.update(traffic_light_horizontal)
            vehicle.draw(screen)

        # Update and draw vertical vehicles
        for vehicle in vehicles_vertical:
            vehicle.update(traffic_light_vertical)
            vehicle.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
