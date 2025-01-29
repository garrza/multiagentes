import pygame
import random

class Vehicle:
    def __init__(self, x, y, color, direction='horizontal', vehicle_list=None):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 10
        self.color = color
        self.speed = 1
        self.max_speed = 1
        self.acceleration = 0.01
        self.deceleration = 0.1
        self.direction = direction
        self.vehicle_list = vehicle_list if vehicle_list is not None else []  # Avoid mutable default
        self.state = "to_traffic_light"  # Possible states: to_traffic_light, is_waiting, is_accepted
        self.isClose = False

    def find_vehicle_ahead(self):
        """Check if a vehicle is ahead and return True/False"""
        for other in self.vehicle_list:
            if other == self:
                continue  # Skip itself
            
            if self.direction == 'horizontal':
                if other.y == self.y and 0 < (other.x - (self.x + self.width)) < 25:
                    return True  # There is a vehicle ahead
                
            elif self.direction == 'vertical':
                if other.x == self.x and 0 < ((self.y - self.height) - other.y) < 25:
                    return True  # There is a vehicle ahead
                
        return False  # No vehicle ahead

    def update(self, traffic_light):
        # Determine distance to traffic light
        if self.direction == 'horizontal':
            distance_to_light = 345 - self.x
        elif self.direction == 'vertical':
            distance_to_light = self.y - 340

        # Check for vehicles ahead
        wasClose = self.isClose  # Store previous state
        self.isClose = self.find_vehicle_ahead()

        # If vehicle was stopped and no longer has an obstacle, restart acceleration
        if wasClose and not self.isClose:
            self.speed += self.acceleration  # Resume movement

        # Traffic light logic
        if self.state == 'to_traffic_light':
            if distance_to_light < 50:  # Approaching traffic light
                if not traffic_light.is_green():
                    self.speed = max(0, self.speed - self.deceleration)  # Decelerate
                    if self.speed == 0:
                        traffic_light.request_green()
                        self.state = "is_waiting"

        elif self.state == 'is_waiting':
            if traffic_light.is_green():
                self.speed += self.acceleration  # Accelerate when green
                self.state = 'is_accepted'

        elif self.state == 'is_accepted':
            self.speed += self.acceleration  # Gradually increase speed

        # Collision avoidance
        if self.isClose:  # If another vehicle is too close
            self.speed = max(0, self.speed - self.deceleration)
        elif not self.isClose:  # If the road is clear, increase speed
            self.speed = min(self.max_speed, self.speed + self.acceleration)

        # Move the vehicle
        if self.direction == 'horizontal':
            self.x += self.speed
        elif self.direction == 'vertical':
            self.y -= self.speed

    def draw(self, screen):
        if self.direction == 'vertical':
            vehicle_surface = pygame.Surface((self.width, self.height))
            vehicle_surface.fill(self.color)
            rotated_vehicle = pygame.transform.rotate(vehicle_surface, 90)
            rotated_rect = rotated_vehicle.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            screen.blit(rotated_vehicle, rotated_rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
