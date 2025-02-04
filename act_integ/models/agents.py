import os
import random
from typing import List, Tuple

import agentpy as ap
from OpenGL.GL import *

from models.vehicles import Vehicle
from objects.objloader import OBJ


class VehicleAgent(ap.Agent):
    """An agent representing a vehicle in the traffic simulation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vehicle: Vehicle = Vehicle.AUTO  # Use the class-level AUTO attribute
        self.speed: float = 0.5
        self.position: List[float] = [0.0, 0.0, 0.0]
        self.path_id: int = 1
        self.model: OBJ = None
        self.scale: float = 4.0
        
        # Load model immediately during initialization
        self._load_vehicle_model()
        self._assign_spawn_point()

    def _load_vehicle_model(self):
        """Load 3D model for the vehicle."""
        model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'untitled.obj')
        self.model = OBJ(model_path, swapyz=True)
        self.model.generate()

    def _assign_spawn_point(self):
        """Assign a random spawn location and path for the vehicle."""
        spawn_options: List[str] = ["left", "right", "top", "bottom"]
        spawn_side: str = random.choice(spawn_options)

        spawn_configs: dict = {
            "left": ([-140, 0, 5], [2, 3]),
            "right": ([140, 0, -10], [2, 3]),
            "bottom": ([-57, 0, 135], [1]),
            "top": ([63, 0, -135], [1])
        }

        self.position, path_choices = spawn_configs[spawn_side]
        self.path_id = random.choice(path_choices)

    def move_along_path(self):
        """Define vehicle trajectory based on assigned path."""
        self.speed = min(
            self.speed + self.vehicle.acceleration,
            self.vehicle.max_speed
        )

        path_movements: dict = {
            1: self._move_straight,
            2: self._move_right,
            3: self._move_left
        }

        path_movements[self.path_id]()

    def _move_straight(self):
        """Move vehicle straight forward."""
        self.position[2] += self.speed

    def _move_right(self):
        """Move vehicle straight, then turn right."""
        if self.position[2] < 100:
            self.position[2] += self.speed
        else:
            self.position[0] += self.speed

    def _move_left(self):
        """Move vehicle straight, then turn left."""
        if self.position[2] < 100:
            self.position[2] += self.speed
        else:
            self.position[0] -= self.speed

    def step(self):
        """Update vehicle state in each simulation step."""
        self.move_along_path()

    def draw(self):
        """Render vehicle in OpenGL scene."""
        if self.model is None:
            return  # Skip drawing if no model is loaded

        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(270, 1, 0, 0)  # Rotate vehicle
        self.model.render()
        glPopMatrix()
