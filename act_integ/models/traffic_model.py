# traffic_model.py
import random
import time
import agentpy as ap
from models.agents import VehicleAgent
from objects.traffic_light import TrafficLight
from objects.stop_block import StopBlock


class TrafficModel(ap.Model):
    def __init__(self, traffic_lights, **kwargs):
        super().__init__(**kwargs)
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)
        self.traffic_lights = []
        self.stop_blocks = []  # New list for stop blocks
        self.start_time = time.time()
        self._setup_traffic_lights()
        self._setup_stop_blocks()

    def _setup_traffic_lights(self):
        """Create and configure all traffic lights including invisible ones"""
        # Visible traffic lights
        light_configs = [
            # North-South lights
            {"pos": (95.0, 25.0), "dir": "NS", "visible": True},
            {"pos": (-95.0, 30.0), "dir": "NS", "visible": True},
            {"pos": (40.0, -25.0), "dir": "EW", "visible": True},
            {"pos": (-40.0, -20.0), "dir": "EW", "visible": True},
            # Invisible intersection lights
            {"pos": (-70.0, 0.0), "dir": "NS", "visible": False},  # Left intersection
            {"pos": (70.0, 0.0), "dir": "NS", "visible": False},  # Right intersection
            {"pos": (0.0, -20.0), "dir": "EW", "visible": False},  # Bottom intersection
            {"pos": (0.0, 20.0), "dir": "EW", "visible": False},  # Top intersection
        ]

        for config in light_configs:
            light = TrafficLight()
            light.x, light.z = config["pos"]
            light.controls_direction = config["dir"]
            light.visible = config["visible"]

            # Set phase offset for East-West lights
            if config["dir"] == "EW":
                light.phase_offset = (
                    sum(light.timings.values()) / 2
                )  # Offset by half cycle

            self.traffic_lights.append(light)

    def _setup_stop_blocks(self):
        """Create stop blocks for each intersection"""
        # Dimensions for stop blocks
        ns_width = 20  # Width reduced to cover only one lane
        ns_depth = 5  # Depth of NS blocks
        ew_width = 5  # Width of EW blocks
        ew_depth = 20  # Depth reduced to cover only one lane

        # Create stop blocks for each intersection
        stop_block_configs = [
            # Left intersection
            {
                "pos": (-60, -25),  # Northbound - positioned on right lane
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },  # Northbound
            {
                "pos": (-80, 25),  # Southbound - positioned on left lane
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },  # Southbound
            {
                "pos": (
                    -95,
                    10,
                ),  # Westbound - positioned on top lane (changed from bottom)
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },  # Westbound
            {
                "pos": (
                    -45,
                    -10,
                ),  # Eastbound - positioned on bottom lane (changed from top)
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },  # Eastbound
            # Right intersection
            {
                "pos": (80, -25),  # Northbound - positioned on right lane
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },  # Northbound
            {
                "pos": (60, 25),  # Southbound - positioned on left lane
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },  # Southbound
            {
                "pos": (95, -10),  # Eastbound - positioned on bottom lane
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },  # Eastbound
            {
                "pos": (45, 10),  # Westbound - positioned on top lane
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },  # Westbound
        ]

        for config in stop_block_configs:
            block = StopBlock(
                config["pos"][0],
                config["pos"][1],
                config["width"],
                config["depth"],
                config["dir"],
            )
            self.stop_blocks.append(block)

    def setup(self):
        """Configure the model with initial parameters."""
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)

    def step(self):
        """Execute a single step in the simulation."""
        # Update traffic lights based on master time
        master_time = time.time() - self.start_time
        for light in self.traffic_lights:
            light.update(master_time)

        # Update stop blocks based on corresponding traffic lights
        for block in self.stop_blocks:
            for light in self.traffic_lights:
                if light.controls_direction == block.direction:
                    block.update(light)
                    break

        # Spawn new vehicles periodically
        if random.random() < 0.02:
            new_vehicle = VehicleAgent(self)
            self.vehicles.append(new_vehicle)

        # Check for vehicle collisions and update positions
        for vehicle in self.vehicles:
            # Check for collisions with other vehicles
            vehicle.collision_ahead = vehicle.is_collision_ahead(self.vehicles)

            # Check for stop block collisions
            should_stop = False
            for block in self.stop_blocks:
                if block.active and block.is_colliding(vehicle.position):
                    should_stop = True
                    break

            # Stop if there's either a collision ahead or an active stop block
            should_stop = should_stop or vehicle.collision_ahead
            vehicle.move(self.traffic_lights, should_stop)

        # Remove vehicles that have reached their destination
        self.vehicles = ap.AgentList(self, [v for v in self.vehicles if v.path])

    def draw(self):
        """Render all components in the scene."""
        for vehicle in self.vehicles:
            vehicle.draw()

        for light in self.traffic_lights:
            light.draw()

        for block in self.stop_blocks:
            block.draw()
