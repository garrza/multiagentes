# models/agents.py
import os
import random
from typing import List, Tuple

import agentpy as ap
from OpenGL.GL import *

from models.vehicles import Vehicle
from objects.objloader import OBJ


class VehicleAgent(ap.Agent):
    def setup(self):
        """Initialize agent attributes during creation"""
        self.vehicle = Vehicle.AUTO
        self.speed = 0.5
        self.position = [0.0, 0.0, 0.0]
        self.direction = "N"  # N, S, E, W
        self.lane = 0  # 0 for right lane, 1 for left lane
        self.path = []
        self.waiting_at_light = False
        self.crossing_intersection = False  # New flag
        self.model = None
        self.scale = 4.0
        self.rotation = 0.0
        self.assigned_light = None  # Track specific traffic light
        self.length = 15.0  # Vehicle length for collision detection
        self.safe_distance = 30.0  # Minimum safe distance between vehicles

        # Load vehicle model
        self.load_vehicle_model()
        self.assign_spawn_point()
        self.calculate_path()

    def load_vehicle_model(self):
        """Load 3D model for the vehicle."""
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "models", "Car.obj"
        )
        self.model = OBJ(model_path, swapyz=True)
        self.model.generate()

    def assign_spawn_point(self):
        """Assign a random spawn location and initial direction."""
        spawn_points = {
            "N": {"pos": [-57, 0, -135], "rot": 180},  # Facing South
            "S": {"pos": [63, 0, 135], "rot": 0},  # Facing North
            "E": {"pos": [140, 0, -10], "rot": 90},  # Facing East
            "W": {"pos": [-140, 0, 5], "rot": 270},  # Facing West
        }

        self.direction = random.choice(list(spawn_points.keys()))
        spawn_data = spawn_points[self.direction]
        self.position = spawn_data["pos"]
        self.rotation = spawn_data["rot"]
        self.lane = random.choice([0, 1])

    def calculate_path(self):
        """Calculate waypoints based on spawn position and direction"""
        if self.direction in ["N", "S"]:
            self.calculate_vertical_path()
        else:
            self.calculate_horizontal_path()

    def calculate_vertical_path(self):
        """Calculate path for north-south movement"""
        current_z = self.position[2]
        target_z = -current_z  # Opposite end of the road

        self.path = []
        if self.direction == "N":
            self.path.append((self.position[0], 0, 30))  # Traffic light position
            self.path.append((self.position[0], 0, target_z))
        else:
            self.path.append((self.position[0], 0, -30))  # Traffic light position
            self.path.append((self.position[0], 0, target_z))

    def calculate_horizontal_path(self):
        """Calculate path for east-west movement"""
        current_x = self.position[0]
        target_x = -current_x  # Opposite end of the road
        self.path = []
        if self.direction == "E":
            self.path.append((90, 0, self.position[2]))  # Traffic light position
            self.path.append((target_x, 0, self.position[2]))
        else:
            self.path.append((-90, 0, self.position[2]))  # Traffic light position
            self.path.append((target_x, 0, self.position[2]))

    def check_traffic_light(self, traffic_lights):
        """Check if vehicle should stop at its assigned traffic light"""

        # Assign a traffic light only once
        if self.assigned_light is None:
            for light in traffic_lights:
                if (
                    self.direction in ["N", "S"]
                    and light.controls_direction == "NS"
                    and abs(self.position[2] - light.z) < 15
                ):
                    self.assigned_light = light
                    break

                elif (
                    self.direction in ["E", "W"]
                    and light.controls_direction == "EW"
                    and abs(self.position[0] - light.x) < 15
                ):
                    self.assigned_light = light
                    break

        # If no light was assigned, keep moving
        if self.assigned_light is None:
            return False

        # If the vehicle is already crossing, ignore the red light
        if self.crossing_intersection:
            return False

        # If the vehicle is near the light and it's red, stop
        distance_to_light = (
            abs(self.position[0] - self.assigned_light.x)
            if self.direction in ["E", "W"]
            else abs(self.position[2] - self.assigned_light.z)
        )

        if distance_to_light < 5 and self.assigned_light.is_red():
            self.waiting_at_light = True
            return True  # Stop before entering

        # Green light, proceed
        self.waiting_at_light = False
        return False

    def is_collision_ahead(self, other_vehicles) -> bool:
        """Check if there's a vehicle ahead in the same lane"""
        if not other_vehicles:
            return False

        # Get vehicle's current lane and direction info
        my_lane_pos = (
            self.position[2] if self.direction in ["E", "W"] else self.position[0]
        )

        for other in other_vehicles:
            if other is self:
                continue

            # Skip vehicles not in same direction
            if other.direction != self.direction:
                continue

            # Get other vehicle's lane position
            other_lane_pos = (
                other.position[2] if self.direction in ["E", "W"] else other.position[0]
            )

            # Check if vehicles are in the same lane (within tolerance)
            lane_tolerance = 5.0
            if abs(my_lane_pos - other_lane_pos) > lane_tolerance:
                continue

            # Check relative positions based on direction
            if self.direction == "E":
                if (
                    other.position[0] > self.position[0]
                    and other.position[0] - self.position[0] < self.safe_distance
                ):
                    return True
            elif self.direction == "W":
                if (
                    other.position[0] < self.position[0]
                    and self.position[0] - other.position[0] < self.safe_distance
                ):
                    return True
            elif self.direction == "N":
                if (
                    other.position[2] > self.position[2]
                    and other.position[2] - self.position[2] < self.safe_distance
                ):
                    return True
            elif self.direction == "S":
                if (
                    other.position[2] < self.position[2]
                    and self.position[2] - other.position[2] < self.safe_distance
                ):
                    return True

        return False

    def move(self, traffic_lights, should_stop=False):
        """Move the vehicle along its path, respecting traffic signals and other vehicles"""
        if should_stop:
            return

        if not self.path:
            return  # No path to follow

        # Get current target waypoint
        target = self.path[0]
        dx = target[0] - self.position[0]
        dz = target[2] - self.position[2]
        distance = (dx**2 + dz**2) ** 0.5

        # If vehicle reaches target, move to next waypoint
        if distance < self.speed:
            self.position = list(target)
            self.path.pop(0)
        else:
            # Calculate movement
            move_x = (dx / distance) * self.speed
            move_z = (dz / distance) * self.speed

            # Update position if no collision detected
            if not hasattr(self, "collision_ahead") or not self.collision_ahead:
                self.position[0] += move_x
                self.position[2] += move_z

    def draw(self):
        """Render the vehicle in the OpenGL scene"""
        if self.model is None:
            return

        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(270, 1, 0, 0)
        self.model.render()
        glPopMatrix()
