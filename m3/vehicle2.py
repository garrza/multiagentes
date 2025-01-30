import pygame
import random

class Vehicle2: # Agente rapido
    def __init__(self, x, y, direction='horizontal', vehicle_list=None):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 10
        self.color = (255, 255, 255)  # white
        self.speed = 2
        self.max_speed = 2
        self.acceleration = 0.01
        self.deceleration = 0.5
        self.direction = direction
        self.vehicle_list = vehicle_list if vehicle_list is not None else []
        
        # Vehicle states
        self.state = "to_traffic_light"
        self.is_close_to_car = False
        #self.stop_distance = 100
        self.in_intersection = False
        
    def update(self, traffic_light):
        # State transitions
        if self.state == "to_traffic_light":
            if self.is_vehicle_ahead():
                self.speed = max(0, self.speed - self.deceleration)  # Slow down
            else:
                self.speed = min(self.speed + self.acceleration, self.max_speed)  # Speed up normally
            
            if self.is_in_intersection():
                self.state = 'waiting'  # The car can go if the light is green at the intersection
                self.speed = max(0, self.speed - self.deceleration)  # Stop gradually
            
            # Continue moving towards the intersection if not in it
            else:
                if self.direction == 'horizontal':
                    self.x += self.speed
                elif self.direction == 'vertical':
                    self.y -= self.speed
                    
        elif self.state == 'waiting':
            self.request_green(traffic_light)
            if traffic_light.is_green():
                self.state = 'accepted'  # The car can go if the light is green at the intersection
            else:
                self.state = 'waiting'
        
        elif self.state == "accepted":
            # Continue moving at normal speed after acceptance
            if self.direction == 'horizontal':
                self.x += self.speed
            elif self.direction == 'vertical':
                self.y -= self.speed

    def is_vehicle_ahead(self):
        # Check if a vehicle is ahead and return True/False
        for other in self.vehicle_list:
            if other == self:
                continue
            
            # Horizontal movement (rightward)
            if self.direction == 'horizontal':
                if 0 < other.x - self.x < 40:
                    return True
            
            # Vertical movement (upward)
            elif self.direction == 'vertical':
                if 0 < self.y - other.y < 40:
                    return True
        
        return False

    def is_in_intersection(self):
        """Check if any part of the vehicle is in or near the intersection."""
        intersection_x, intersection_y = 325, 390

        if self.direction == 'horizontal':
            return (self.x + self.width >= intersection_x)
        else:
            return (self.y + self.height <= intersection_y)

    def request_green(self, traffic_light):
        if traffic_light.other_light.state == 'loop' or traffic_light.other_light.state == 'pause':
            return
        elif traffic_light.state == 'pause':
            return
        else:
            traffic_light.state = 'loop'
            
    def draw(self, screen):
        if self.direction == 'vertical':
            vehicle_surface = pygame.Surface((self.width, self.height))
            vehicle_surface.fill(self.color)
            rotated_vehicle = pygame.transform.rotate(vehicle_surface, 90)
            rotated_rect = rotated_vehicle.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            screen.blit(rotated_vehicle, rotated_rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
