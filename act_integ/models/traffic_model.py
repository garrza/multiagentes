# traffic_model.py
import random
import agentpy as ap
from models.agents import VehicleAgent


class TrafficModel(ap.Model):
    def __init__(self, traffic_lights, **kwargs):
        super().__init__(**kwargs)
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)
        self.traffic_lights = traffic_lights
        self.step_count = 0

    def setup(self):
        """Configure the model with initial parameters."""
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)

    def step(self):
        """Execute a single step in the simulation."""
        self.step_count += 1

        # Update traffic lights
        for light in self.traffic_lights:
            light.update()

        # Spawn new vehicles periodically
        if self.step_count % random.randint(120, 300) == 0:
            new_vehicle = VehicleAgent(self)
            self.vehicles.append(new_vehicle)

        # Update all vehicles
        for vehicle in self.vehicles:
            vehicle.move(self.traffic_lights)

        # Remove vehicles that have reached their destination
        self.vehicles = ap.AgentList(
            self, [v for v in self.vehicles if v.path]
        )  # Only keep vehicles with remaining path

    def draw(self):
        """Render all vehicles in the scene."""
        for vehicle in self.vehicles:
            vehicle.draw()
