import pygame

# Colors
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (30, 30, 30)

# Dimensions
WIDTH = 30
HEIGHT = 90

class TrafficLight:
    def __init__(self, x, y, rotation_angle=0):
        self.x = x
        self.y = y
        self.state = "RED"  # Initial state
        self.timer = 0
        self.rotation_angle = rotation_angle  # Rotation angle in degrees
        self.waiting_car = False

    def update(self):
        if self.waiting_car:  # If a car requested green, start the timer
            self.timer += 1
            if self.timer > 60:  # Wait 1 second (60 frames)
                self.state = "GREEN"
                self.timer = 0
                self.waiting_car = False  # Reset request
                
    def request_green(self):
        self.waiting_car = True  # A car is waiting and requests a green light

    def draw(self, screen):
        # Create a temporary surface for the traffic light
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # Make the surface transparent

        # Draw the traffic light body
        pygame.draw.rect(temp_surface, BLACK, (0, 0, WIDTH, HEIGHT))

        # Determine the light color based on the state
        color = GREEN if self.state == "GREEN" else RED

        # Draw the lights
        pygame.draw.circle(temp_surface, color, (WIDTH // 2, 20), 10)  # Top light
        pygame.draw.circle(temp_surface, color, (WIDTH // 2, 45), 10)  # Middle light
        pygame.draw.circle(temp_surface, color, (WIDTH // 2, 70), 10)  # Bottom light

        # Rotate the traffic light surface
        rotated_surface = pygame.transform.rotate(temp_surface, self.rotation_angle)

        # Get the new rectangle and center it at the original position
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))

        # Blit the rotated surface onto the screen
        screen.blit(rotated_surface, rotated_rect.topleft)

    def is_green(self):
        return self.state == "GREEN"
