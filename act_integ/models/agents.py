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
        self.model = None
        self.scale = 4.0
        self.rotation = 0.0

        # Load the model and set initial position
        self.load_vehicle_model()
        self.assign_spawn_point()
        self.calculate_path()

    def load_vehicle_model(self):
        """Load 3D model for the vehicle."""
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "models", "untitled.obj"
        )
        self.model = OBJ(model_path, swapyz=True)
        self.model.generate()

    def assign_spawn_point(self):
        """Assign a random spawn location and initial direction."""
        spawn_points = {
            "N": {"pos": [-57, 0, -135], "rot": 0},
            "S": {"pos": [63, 0, 135], "rot": 180},
            "E": {"pos": [140, 0, -10], "rot": 270},
            "W": {"pos": [-140, 0, 5], "rot": 90},
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
        """Check if vehicle should stop at nearby traffic light"""
        for light in traffic_lights:
            if self.direction in ["N", "S"] and light.controls_direction == "NS":
                if abs(self.position[2] - light.z) < 10 and light.is_red():
                    self.waiting_at_light = True
                    return True
            elif self.direction in ["E", "W"] and light.controls_direction == "EW":
                if abs(self.position[0] - light.x) < 10 and light.is_red():
                    self.waiting_at_light = True
                    return True
        self.waiting_at_light = False
        return False

    def move(self, traffic_lights):
        """Move the vehicle along its path, respecting traffic lights"""
        if self.waiting_at_light:
            if not self.check_traffic_light(traffic_lights):
                self.waiting_at_light = False
            return

        if not self.path:
            return

        target = self.path[0]
        dx = target[0] - self.position[0]
        dz = target[2] - self.position[2]

        distance = (dx**2 + dz**2) ** 0.5

        if distance < self.speed:
            self.position = list(target)
            self.path.pop(0)
        else:
            move_x = (dx / distance) * self.speed
            move_z = (dz / distance) * self.speed
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