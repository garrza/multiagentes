import pygame
import random

class Vehicle:
    def __init__(self, x, y, color, direction='horizontal'):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 5
        self.color = color
        self.speed = 10
        self.acceleration = 0.05
        self.deceleration = 0.1
        self.direction = direction

    def move(self, traffic_light):
        # Si el semáforo está en verde, acelerar
        if traffic_light.is_green():
            self.speed += self.acceleration
        else:  # Si está en rojo, frenar
            self.speed -= self.deceleration

        # Limitar velocidad
        self.speed = max(0, min(self.speed, 5))

        # Mover dependiendo de la dirección
        if self.direction == 'horizontal':
            self.x += self.speed
        elif self.direction == 'vertical':
            self.y -= self.speed

    def draw(self, screen):
        # Rotar el vehículo si la dirección es vertical
        if self.direction == 'vertical':
            vehicle_surface = pygame.Surface((self.width, self.height))  # Create a new surface for rotation
            vehicle_surface.fill(self.color)  # Fill the surface with the vehicle's color
            rotated_vehicle = pygame.transform.rotate(vehicle_surface, 90)  # Rotate the surface by 90 degrees
            rotated_rect = rotated_vehicle.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))  # Recalculate the new position of the rotated vehicle
            screen.blit(rotated_vehicle, rotated_rect.topleft)  # Draw the rotated vehicle
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))  # Draw the horizontal vehicle
