import pygame
class VehicleBase:
    def __init__(self, x, y, direction, vehicle_list, road_width):
        self.x = x
        self.y = y
        self.direction = direction
        self.vehicle_list = vehicle_list
        self.road_width = road_width
        self.state = "DRIVING"
        
        # Vehicle characteristics set by child classes
        self._init_characteristics()
        
        # Swap width and height for horizontal vehicles
        if direction == 'horizontal':
            self.width, self.height = self.height, self.width
            
    def _init_characteristics(self):
        # Override in child classes
        pass
        
    def update(self, traffic_light, intersection_pos):
        # Check if approaching intersection
        if self.is_approaching_intersection(intersection_pos):
            if not traffic_light.state == "GREEN":
                self.speed = max(0, self.speed - self.deceleration)
            elif not self.is_vehicle_ahead():
                self.speed = min(self.speed + self.acceleration, self.max_speed)
        else:
            if self.is_vehicle_ahead():
                self.speed = max(0, self.speed - self.deceleration)
            else:
                self.speed = min(self.speed + self.acceleration, self.max_speed)
        
        # Update position
        if self.direction == 'horizontal':
            self.x += self.speed
        else:
            self.y -= self.speed
            
    def is_approaching_intersection(self, intersection_pos):
        buffer = 100  # Detection distance
        if self.direction == 'horizontal':
            return 0 < intersection_pos - (self.x + self.width) < buffer
        else:
            return 0 < self.y - intersection_pos < buffer
            
    def is_vehicle_ahead(self):
        safe_distance = 60
        for other in self.vehicle_list:
            if other == self:
                continue
                
            if self.direction == 'horizontal':
                if other.direction == 'horizontal':
                    if (0 < other.x - (self.x + self.width) < safe_distance and
                        abs(self.y - other.y) < self.height):
                        return True
            else:
                if other.direction == 'vertical':
                    if (0 < (self.y - self.height) - other.y < safe_distance and
                        abs(self.x - other.x) < self.width):
                        return True
        return False
        
    def draw(self, screen):
        # Create rectangle for the vehicle body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Add visual indicators for direction (darker rectangles for front/back)
        if self.direction == 'horizontal':
            # Front of vehicle (right side for horizontal)
            pygame.draw.rect(screen, (50, 50, 50), 
                           (self.x + self.width - 8, self.y + 2, 6, self.height - 4))
            # Back of vehicle (left side for horizontal)
            pygame.draw.rect(screen, (80, 80, 80), 
                           (self.x + 2, self.y + 2, 6, self.height - 4))
        else:
            # Front of vehicle (top for vertical)
            pygame.draw.rect(screen, (50, 50, 50), 
                           (self.x + 2, self.y, self.width - 4, 6))
            # Back of vehicle (bottom for vertical)
            pygame.draw.rect(screen, (80, 80, 80), 
                           (self.x + 2, self.y + self.height - 8, self.width - 4, 6))

class RegularVehicle(VehicleBase):
    def _init_characteristics(self):
        self.width = 20  # This will be vehicle width
        self.height = 40  # This will be vehicle length
        self.color = (0, 0, 0)  # Black
        self.speed = 2
        self.max_speed = 2
        self.acceleration = 0.1
        self.deceleration = 0.2

class FastVehicle(VehicleBase):
    def _init_characteristics(self):
        self.width = 20
        self.height = 45
        self.color = (255, 0, 0)  # Red
        self.speed = 3
        self.max_speed = 3
        self.acceleration = 0.15
        self.deceleration = 0.25

class SlowVehicle(VehicleBase):
    def _init_characteristics(self):
        self.width = 25
        self.height = 50
        self.color = (0, 0, 255)  # Blue
        self.speed = 1.5
        self.max_speed = 1.5
        self.acceleration = 0.08
        self.deceleration = 0.15

class CompactVehicle(VehicleBase):
    def _init_characteristics(self):
        self.width = 15
        self.height = 35
        self.color = (255, 255, 0)  # Yellow
        self.speed = 2.5
        self.max_speed = 2.5
        self.acceleration = 0.12
        self.deceleration = 0.22