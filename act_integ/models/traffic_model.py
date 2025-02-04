import random
from typing import List

import agentpy as ap

from models.agents import VehicleAgent


class TrafficModel(ap.Model):
    """A simulation model for traffic dynamics."""

    def __init__(self, **kwargs):
        """Initialize the traffic model."""
        super().__init__(**kwargs)
        self.vehicles: ap.AgentList = None
        self.step_count: int = 0
        self.setup()

    def setup(self):
        """Configure the model with initial parameters."""
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)

    def step(self):
        """Execute a single step in the simulation."""
        self.step_count += 1

        # Spawn new vehicles periodically with randomized interval
        if self.step_count % random.randint(120, 300) == 0:
            new_vehicle = VehicleAgent(self)
            self.vehicles.append(new_vehicle)

        # Update all vehicles
        self.vehicles.step()

    def draw(self):
        """Render all vehicles in the scene."""
        for vehicle in self.vehicles:
            vehicle.draw()
