# traffic_model.py
import random
import time
import agentpy as ap
from models.agents import VehicleAgent
from objects.traffic_light import TrafficLight
from objects.stop_block import StopBlock
from models.pedestrian import PedestrianAgent


class TrafficModel(ap.Model):
    def __init__(self, traffic_lights, **kwargs):
        super().__init__(**kwargs)
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)
        self.pedestrians = ap.AgentList(self, 0, PedestrianAgent)
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

        # Create stop blocks for each intersection - positions adjusted to be before crosswalks
        stop_block_configs = [
            # Left intersection
            {
                "pos": (-60, -30),  # Northbound - moved back 5 units
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },
            {
                "pos": (-80, 30),  # Southbound - moved back 5 units
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },
            {
                "pos": (-100, 10),  # Westbound - moved back 5 units
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },
            {
                "pos": (-40, -10),  # Eastbound - moved back 5 units
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },
            # Right intersection
            {
                "pos": (80, -30),  # Northbound - moved back 5 units
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },
            {
                "pos": (60, 30),  # Southbound - moved back 5 units
                "width": ns_width,
                "depth": ns_depth,
                "dir": "NS",
            },
            {
                "pos": (100, -10),  # Eastbound - moved back 5 units
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },
            {
                "pos": (40, 10),  # Westbound - moved back 5 units
                "width": ew_width,
                "depth": ew_depth,
                "dir": "EW",
            },
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

        # Spawn new pedestrians periodically
        if random.random() < 0.01:  # Lower spawn rate than vehicles
            new_pedestrian = PedestrianAgent(self)
            self.pedestrians.append(new_pedestrian)

        # Update pedestrians first
        for pedestrian in self.pedestrians:
            pedestrian.move(self.traffic_lights, self.vehicles)

        # Then update vehicles with pedestrian awareness
        for vehicle in self.vehicles:
            # Check for nearby pedestrians
            should_stop = False
            for pedestrian in self.pedestrians:
                if self._is_pedestrian_in_vehicle_path(vehicle, pedestrian):
                    should_stop = True
                    break

            # Regular vehicle updates
            vehicle.collision_ahead = vehicle.is_collision_ahead(self.vehicles)
            should_stop = should_stop or vehicle.collision_ahead

            for block in self.stop_blocks:
                if block.active and block.is_colliding(vehicle.position):
                    should_stop = True
                    break

            vehicle.move(self.traffic_lights, should_stop)

        # Remove vehicles that have reached their destination
        self.vehicles = ap.AgentList(self, [v for v in self.vehicles if v.path])
        # Remove pedestrians that reached destination
        self.pedestrians = ap.AgentList(self, [p for p in self.pedestrians if p.path])

    def draw(self):
        """Render all components in the scene."""
        for vehicle in self.vehicles:
            vehicle.draw()

        for light in self.traffic_lights:
            light.draw()

        for block in self.stop_blocks:
            block.draw()

        for pedestrian in self.pedestrians:
            pedestrian.draw()

    def _is_pedestrian_in_vehicle_path(self, vehicle, pedestrian, safe_distance=20.0):
        """Check if pedestrian is in vehicle's path and needs to be avoided"""
        # Get vehicle's projected path
        if not vehicle.path:
            return False

        next_point = vehicle.path[0]

        # Calculate if pedestrian is between vehicle and its next point
        v_pos = vehicle.position
        p_pos = pedestrian.position

        # Simple rectangular check based on vehicle direction
        if vehicle.direction in ["N", "S"]:
            # Check if pedestrian is in same vertical lane
            if abs(p_pos[0] - v_pos[0]) > 5.0:
                return False

            # Check if pedestrian is between vehicle and its target
            if vehicle.direction == "N":
                return v_pos[2] < p_pos[2] < v_pos[2] + safe_distance
            else:
                return v_pos[2] - safe_distance < p_pos[2] < v_pos[2]
        else:
            # Similar check for east-west movement
            if abs(p_pos[2] - v_pos[2]) > 5.0:
                return False

            if vehicle.direction == "E":
                return v_pos[0] < p_pos[0] < v_pos[0] + safe_distance
            else:
                return v_pos[0] - safe_distance < p_pos[0] < v_pos[0]
