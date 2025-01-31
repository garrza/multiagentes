import pygame

class TrafficLight:
    def __init__(self, x, y, rotation_angle=0):
        # Colors
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.BLACK = (30, 30, 30)
        
        # Position and rotation
        self.x = x
        self.y = y
        self.rotation_angle = rotation_angle
        
        # Dimensions
        self.WIDTH = 20
        self.HEIGHT = 60
        
        # State management
        self.state = "RED"
        self.timer = 0
        self.other_light = None
        
        # Timing configuration (in frames at 60 FPS)
        self.GREEN_DURATION = 300  # 5 seconds
        self.YELLOW_DURATION = 60  # 1 second
        self.RED_DURATION = 60     # 1 second after red before switching

    def set_other_light(self, other_light):
        self.other_light = other_light

    def update(self):
        self.timer += 1
        
        if self.state == "GREEN" and self.timer >= self.GREEN_DURATION:
            self.state = "YELLOW"
            self.timer = 0
            
        elif self.state == "YELLOW" and self.timer >= self.YELLOW_DURATION:
            self.state = "RED"
            self.timer = 0
            
        elif self.state == "RED" and self.timer >= self.RED_DURATION:
            if self.other_light and self.other_light.state == "RED":
                self.state = "GREEN"
                self.timer = 0

    def draw(self, screen):
        # Create surface for rotation
        surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        
        # Draw light housing
        pygame.draw.rect(surface, self.BLACK, (0, 0, self.WIDTH, self.HEIGHT))
        
        # Define light positions
        positions = [(self.WIDTH//2, 10), (self.WIDTH//2, 30), (self.WIDTH//2, 50)]
        colors = [self.RED, self.YELLOW, self.GREEN]
        
        # Draw each light
        for pos, color in zip(positions, colors):
            if (color == self.RED and self.state == "RED") or \
               (color == self.YELLOW and self.state == "YELLOW") or \
               (color == self.GREEN and self.state == "GREEN"):
                pygame.draw.circle(surface, color, pos, 8)
            else:
                pygame.draw.circle(surface, self.GRAY, pos, 8)
        
        # Rotate and position
        rotated = pygame.transform.rotate(surface, self.rotation_angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect.topleft)
