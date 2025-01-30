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
    current_green = None
    def __init__(self, x, y, rotation_angle=0):
        self.x = x
        self.y = y
        self.timer = 0
        self.color = "RED"  # Default to RED initially
        self.rotation_angle = rotation_angle
        self.state = "waiting"
        self.other_light = None
        
    def set_other_light(self, other_light):
        """Set reference to the other traffic light for coordination"""
        self.other_light = other_light
        
    def update(self):        
        if self.state == 'waiting':
            self.color = 'RED'

        elif self.state == 'loop':
            self.color = 'GREEN'
            self.timer += 1
            
            if self.timer >= 300:  
                self.color = 'RED'
                self.state = 'pause'  # Enter pause state
                self.timer = 0  

        elif self.state == 'pause':
            self.color = 'RED'
            self.timer += 1
            
            if self.timer >= 60:  # 2-second pause (assuming 60 FPS)
                self.state = 'waiting'  
                
                if self.other_light and self.other_light.state == 'waiting':
                    self.other_light.state = 'loop'
                    self.other_light.color = 'GREEN'
                    self.other_light.timer = 0  # Reset the other light’s timer
        
    def is_green(self):
        # Returns true if the light is green
        return self.color == "GREEN"

    def draw(self, screen):
        # Create a temporary surface for the traffic light
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # Make the surface transparent

        # Draw the traffic light body
        pygame.draw.rect(temp_surface, BLACK, (0, 0, WIDTH, HEIGHT))

        # Set the color based on the state
        if self.state == "loop":  # Green light
            color = GREEN
        elif self.state == "pause":  # Yellow light (for the pause state)
            color = (255, 255, 0)  # Yellow
        else:  # RED or waiting state
            color = RED

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
