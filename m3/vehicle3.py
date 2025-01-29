import pygame
import random

class Vehicle3:
    def __init__(self, x, y, direction='horizontal', vehicle_list=None):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 10
        self.color = (0, 255, 255) # cyan
        self.speed = 1
        self.max_speed = 1
        self.acceleration = 0.01
        self.deceleration = 0.2
        self.direction = direction
        self.vehicle_list = vehicle_list if vehicle_list is not None else []
        self.state = "to_traffic_light"
        self.isClose = False
        self.stop_distance = 80
        self.in_intersection = False

    def find_vehicle_ahead(self):
        """Check if a vehicle is ahead and return True/False"""
        for other in self.vehicle_list:
            if other == self:
                continue
            
            if self.direction == 'horizontal':
                if other.y == self.y and 0 < (other.x - (self.x + self.width)) < 25:
                    return True
                
            elif self.direction == 'vertical':
                if other.x == self.x and 0 < ((self.y - self.height) - other.y) < 25:
                    return True
                
        return False

    def find_vehicle_in_intersection(self):
        """
        Check if there's a perpendicular vehicle in or approaching the intersection.
        Uses the same buffer zone as is_in_intersection.
        """
        for other in self.vehicle_list:
            if other == self:
                continue
                
            # Only check vehicles moving in the perpendicular direction
            if other.direction == self.direction:
                continue
                
            # Check if the other vehicle is in or near the intersection
            if other.is_in_intersection(None):
                return True
        return False

    def is_in_intersection(self, traffic_light):
        """
        Check if any part of the vehicle is in or near the intersection.
        Includes a buffer zone of 1 pixel around the intersection.
        """
        # Intersection constants
        intersection_x = 345
        intersection_y = 340
        intersection_width = 30
        buffer = 1  # 1 pixel buffer zone
        
        # Calculate intersection boundaries with buffer
        intersection_left = intersection_x - (intersection_width/2 + buffer)
        intersection_right = intersection_x + (intersection_width/2 + buffer)
        intersection_top = intersection_y - (intersection_width/2 + buffer)
        intersection_bottom = intersection_y + (intersection_width/2 + buffer)
        
        if self.direction == 'horizontal':
            # For horizontal vehicles, check if any part from front to back is in the intersection
            vehicle_left = self.x
            vehicle_right = self.x + self.width
            
            # Check if any part of the vehicle overlaps with the buffered intersection zone
            return (intersection_left <= vehicle_right <= intersection_right or  # Front in intersection
                    intersection_left <= vehicle_left <= intersection_right or   # Back in intersection
                    (vehicle_left <= intersection_left and vehicle_right >= intersection_right))  # Spanning intersection
        else:  # vertical
            # For vertical vehicles, check if any part from front to back is in the intersection
            vehicle_top = self.y - self.height  # Subtract height because vertical vehicles move upward
            vehicle_bottom = self.y
            
            # Check if any part of the vehicle overlaps with the buffered intersection zone
            return (intersection_top <= vehicle_bottom <= intersection_bottom or  # Front in intersection
                    intersection_top <= vehicle_top <= intersection_bottom or     # Back in intersection
                    (vehicle_top <= intersection_top and vehicle_bottom >= intersection_bottom))  # Spanning intersection

    def update(self, traffic_light):
        if self.direction == 'horizontal':
            distance_to_light = 345 - self.x
            passed_light = self.x > 345
        elif self.direction == 'vertical':
            distance_to_light = self.y - 340
            passed_light = self.y < 340

        self.in_intersection = self.is_in_intersection(traffic_light)
        
        wasClose = self.isClose
        self.isClose = self.find_vehicle_ahead()
        
        # Check for vehicles in intersection
        intersection_blocked = self.find_vehicle_in_intersection()

        if wasClose and not self.isClose:
            self.speed = min(self.speed + self.acceleration, self.max_speed)

        if not self.isClose:
            if not passed_light:
                if self.in_intersection:
                    self.speed = min(self.speed + self.acceleration, self.max_speed)
                # Only proceed if light is green AND intersection is clear OR we're far from light
                elif (traffic_light.is_green() and not intersection_blocked) or distance_to_light > self.stop_distance:
                    self.speed = min(self.speed + self.acceleration, self.max_speed)
                else:
                    self.speed = max(0, self.speed - self.deceleration)
                    if self.speed == 0 and traffic_light.is_green():
                        # Don't request green if we're just waiting for intersection to clear
                        if not intersection_blocked:
                            traffic_light.request_green()
            else:
                self.speed = min(self.speed + self.acceleration, self.max_speed)

        if self.isClose:
            self.speed = max(0, self.speed - self.deceleration)
        elif self.state != 'is_waiting':
            self.speed = min(self.speed + self.acceleration, self.max_speed)

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
