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
    # Class variable to track the currently green light
    current_green = None
    safety_delay = 60  # 1 second at 60 FPS
    initial_state_set = False
    max_wait_time = 300  # 5 seconds max wait time threshold

    def __init__(self, x, y, rotation_angle=0):
        self.x = x
        self.y = y
        self.state = "RED"  # Default to RED initially
        self.timer = 0
        self.rotation_angle = rotation_angle
        self.waiting_cars = 0
        self.total_wait_time = 0
        self.cars_passed = 0
        self.last_green_time = pygame.time.get_ticks()
        self.other_light = None
        
        # Dynamic timing parameters
        self.base_green_duration = 120   # 2 seconds base
        self.min_green_duration = 90     # 1.5 seconds minimum
        self.max_green_duration = 600    # 10 seconds maximum
        self.yellow_duration = 60        # 1 second
        
    def set_other_light(self, other_light):
        """Set reference to the other traffic light for coordination"""
        self.other_light = other_light
        
        # Only set initial state when both lights are connected
        if not TrafficLight.initial_state_set and other_light is not None:
            self.state = "GREEN"
            TrafficLight.current_green = self
            TrafficLight.initial_state_set = True
            other_light.state = "RED"
        
    def update(self):
        self.timer += 1
        
        if self.state == "GREEN":
            self.cars_passed += 1
            duration = self._calculate_green_duration()
            
            if self.timer >= duration:
                self.state = "YELLOW"
                self.timer = 0
                self.last_green_time = pygame.time.get_ticks()
                
        elif self.state == "YELLOW":
            if self.timer >= self.yellow_duration:
                self.state = "SAFETY_DELAY"
                self.timer = 0
                TrafficLight.current_green = None
                
        elif self.state == "SAFETY_DELAY":
            if self.timer >= self.safety_delay:
                self.state = "RED"
                self.timer = 0
                if self.other_light.state == "RED":
                    if self._should_switch_to_other_light():
                        self.other_light.state = "GREEN"
                        TrafficLight.current_green = self.other_light
                        self.other_light.timer = 0
                        self.other_light.waiting_cars = max(0, self.other_light.waiting_cars)
                        self.other_light.total_wait_time = 0
        
        # Update waiting time for cars at red light
        if self.state == "RED" and self.waiting_cars > 0:
            self.total_wait_time += 1

    def _calculate_green_duration(self):
        """Calculate optimal green duration based on traffic flow"""
        # Start with base duration
        duration = self.base_green_duration
        
        # Add time based on waiting cars (20 frames per car)
        duration += self.waiting_cars * 20
        
        # Check traffic flow efficiency
        flow_rate = self.cars_passed / max(1, self.timer)
        if flow_rate > 0.5:  # Good flow rate (more than 1 car per 2 seconds)
            duration += 60    # Add 1 second
            
        # Reduce duration if other light has many waiting cars
        if self.other_light.waiting_cars > 0:
            other_wait_factor = min(1.5, self.other_light.waiting_cars / 5)
            duration = duration / other_wait_factor
            
        # Ensure duration stays within bounds
        return max(self.min_green_duration, min(duration, self.max_green_duration))

    def _should_switch_to_other_light(self):
        """Determine if traffic conditions warrant switching to other light"""
        # Switch if no cars waiting at this light
        if self.waiting_cars == 0:
            return True
            
        # Switch if other light has been waiting too long
        if (self.other_light.waiting_cars > 0 and 
            self.other_light.total_wait_time >= self.max_wait_time):
            return True
            
        # Switch if other light has significantly more traffic
        if self.other_light.waiting_cars > self.waiting_cars * 1.5:
            return True
            
        return False

    def request_green(self):
        """Called when a vehicle arrives at the light"""
        self.waiting_cars += 1
        
    def is_green(self):
        """Returns True if the light is green"""
        return self.state == "GREEN"

    def draw(self, screen):
        # Create a temporary surface for the traffic light
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # Make the surface transparent

        # Draw the traffic light body
        pygame.draw.rect(temp_surface, BLACK, (0, 0, WIDTH, HEIGHT))

        # Determine the light color based on the state
        if self.state == "GREEN":
            color = GREEN
        elif self.state == "YELLOW":
            color = (255, 255, 0)  # Yellow color
        else:  # RED or SAFETY_DELAY
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
