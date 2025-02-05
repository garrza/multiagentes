import random
from typing import List, Tuple, Optional
import agentpy as ap
from OpenGL.GL import *
from OpenGL.GLUT import *
from objects.traffic_light import TrafficLight


class PedestrianAgent(ap.Agent):
    def setup(self):
        """Initialize pedestrian attributes"""
        self.position = [0.0, 0.0, 0.0]
        self.speed = 0.3
        self.direction = "N"  # N, S, E, W
        self.path = []
        self.waiting_to_cross = False
        self.personality = random.choice(["patient", "aggressive", "impulsive"])
        self.size = 2.0
        self.color = self._get_personality_color()

        self.assign_spawn_point()
        self.calculate_path()

    def _get_personality_color(self) -> Tuple[float, float, float]:
        """Return color based on personality"""
        colors = {
            "patient": (0.0, 0.8, 0.0),  # Green
            "aggressive": (0.8, 0.0, 0.0),  # Red
            "impulsive": (0.8, 0.8, 0.0),  # Yellow
        }
        return colors[self.personality]

    def assign_spawn_point(self):
        """Assign random spawn location on sidewalk"""
        # Define spawn zones on sidewalks
        spawn_zones = {
            "N": [
                # Left vertical road
                {"x_range": (-90, -50), "z": -140, "direction": "N"},
                # Right vertical road
                {"x_range": (50, 90), "z": -140, "direction": "N"},
            ],
            "S": [
                # Left vertical road
                {"x_range": (-90, -50), "z": 140, "direction": "S"},
                # Right vertical road
                {"x_range": (50, 90), "z": 140, "direction": "S"},
            ],
            "E": [
                # Top horizontal road
                {"x": -140, "z_range": (-20, 20), "direction": "E"}
            ],
            "W": [
                # Top horizontal road
                {"x": 140, "z_range": (-20, 20), "direction": "W"}
            ],
        }

        # Select random spawn direction and zone
        self.direction = random.choice(list(spawn_zones.keys()))
        zone = random.choice(spawn_zones[self.direction])

        # Set position based on zone
        if self.direction in ["N", "S"]:
            self.position = [
                random.uniform(zone["x_range"][0], zone["x_range"][1]),
                0,
                zone["z"],
            ]
        else:
            self.position = [
                zone["x"],
                0,
                random.uniform(zone["z_range"][0], zone["z_range"][1]),
            ]

    def calculate_path(self):
        """Calculate path including sidewalk movement and crossings"""
        if self.direction in ["N", "S"]:
            self.calculate_vertical_path()
        else:
            self.calculate_horizontal_path()

    def calculate_vertical_path(self):
        """Calculate path for north-south movement including sidewalk navigation"""
        current_x, _, current_z = self.position

        # Determine which vertical road we're on
        if -90 <= current_x <= -50:  # Left vertical road
            if self.direction == "N":
                # Use west sidewalk (-90 - sidewalk_width)
                target_x = -95
            else:
                # Use east sidewalk (-50 + sidewalk_width)
                target_x = -45
        else:  # Right vertical road (50 <= current_x <= 90)
            if self.direction == "N":
                # Use west sidewalk (50 - sidewalk_width)
                target_x = 45
            else:
                # Use east sidewalk (90 + sidewalk_width)
                target_x = 95

        target_z = -current_z  # Opposite end of road

        # Add waypoints including sidewalk approach and crosswalk points
        self.path = []

        # First move to correct sidewalk if not already there
        if abs(current_x - target_x) > 0.5:
            self.path.append((target_x, 0, current_z))

        if self.direction == "N":
            # Add crosswalk approach points
            if current_z < -25:
                # Approach crosswalk on sidewalk
                self.path.append((target_x, 0, -25))
                # Move to crosswalk
                self.path.append((target_x, 0, -22))
                # Cross the road
                self.path.append((target_x, 0, 22))
                # Return to sidewalk
                self.path.append((target_x, 0, 25))
            # Continue to destination on sidewalk
            self.path.append((target_x, 0, target_z))
        else:  # Direction is "S"
            if current_z > 25:
                # Approach crosswalk on sidewalk
                self.path.append((target_x, 0, 25))
                # Move to crosswalk
                self.path.append((target_x, 0, 22))
                # Cross the road
                self.path.append((target_x, 0, -22))
                # Return to sidewalk
                self.path.append((target_x, 0, -25))
            # Continue to destination on sidewalk
            self.path.append((target_x, 0, target_z))

    def calculate_horizontal_path(self):
        """Calculate path for east-west movement including sidewalk navigation"""
        current_x, _, current_z = self.position
        target_x = -current_x

        # Determine which sidewalk to use (north or south)
        if self.direction == "E":
            # Use north sidewalk
            target_z = 25
        else:
            # Use south sidewalk
            target_z = -25

        # Add waypoints including sidewalk approach and crosswalk points
        self.path = []

        # First move to correct sidewalk if not already there
        if abs(current_z - target_z) > 0.5:
            self.path.append((current_x, 0, target_z))

        if self.direction == "E":
            if current_x < -50:
                # Approach left intersection
                self.path.append((-90, 0, target_z))
                # Move to crosswalk
                self.path.append((-87, 0, target_z))
                # Cross the road
                self.path.append((-53, 0, target_z))
                # Return to sidewalk
                self.path.append((-50, 0, target_z))
            elif current_x < 50:
                # Approach right intersection
                self.path.append((50, 0, target_z))
                # Move to crosswalk
                self.path.append((53, 0, target_z))
                # Cross the road
                self.path.append((87, 0, target_z))
                # Return to sidewalk
                self.path.append((90, 0, target_z))
        else:  # Direction is "W"
            if current_x > 50:
                # Approach right intersection
                self.path.append((90, 0, target_z))
                # Move to crosswalk
                self.path.append((87, 0, target_z))
                # Cross the road
                self.path.append((53, 0, target_z))
                # Return to sidewalk
                self.path.append((50, 0, target_z))
            elif current_x > -50:
                # Approach left intersection
                self.path.append((-50, 0, target_z))
                # Move to crosswalk
                self.path.append((-53, 0, target_z))
                # Cross the road
                self.path.append((-87, 0, target_z))
                # Return to sidewalk
                self.path.append((-90, 0, target_z))

        # Continue to final destination on sidewalk
        self.path.append((target_x, 0, target_z))

    def should_wait(self, traffic_lights) -> bool:
        """Determine if pedestrian should wait based on personality and traffic"""
        if self.personality == "aggressive":
            return False
        elif self.personality == "impulsive":
            return random.random() < 0.3
        else:  # patient
            return True

    def move(self, traffic_lights, vehicles):
        """Enhanced movement with better traffic awareness"""
        if not self.path:
            return

        target = self.path[0]
        dx = target[0] - self.position[0]
        dz = target[2] - self.position[2]
        distance = (dx**2 + dz**2) ** 0.5

        # Check if at crosswalk
        at_crosswalk = self._is_at_crosswalk()

        if at_crosswalk:
            # Get relevant traffic light
            traffic_light = self._get_relevant_traffic_light(traffic_lights)
            if traffic_light:
                should_wait = self._should_wait_at_crossing(traffic_light)
                if should_wait:
                    self.waiting_to_cross = True
                    return

        # Check for nearby vehicles if crossing
        if self._is_crossing_road():
            if self._is_vehicle_too_close(vehicles):
                self.waiting_to_cross = True
                return

        # Move towards target
        if distance < self.speed:
            self.position = list(target)
            self.path.pop(0)
        else:
            move_x = (dx / distance) * self.speed
            move_z = (dz / distance) * self.speed
            self.position[0] += move_x
            self.position[2] += move_z

    def _is_at_crosswalk(self) -> bool:
        """Check if pedestrian is at a crosswalk"""
        x, _, z = self.position

        # Check horizontal crosswalks (near vertical roads)
        if abs(z) >= 20 and abs(z) <= 25:
            # Left intersection
            if -90 <= x <= -50:
                return True
            # Right intersection
            if 50 <= x <= 90:
                return True

        # Check vertical crosswalks (near horizontal road)
        if -25 <= z <= 25:
            # Left intersection
            if -90 <= x <= -85 or -55 <= x <= -50:
                return True
            # Right intersection
            if 50 <= x <= 55 or 85 <= x <= 90:
                return True

        return False

    def _is_crossing_road(self) -> bool:
        """Check if pedestrian is currently crossing a road"""
        x, _, z = self.position

        # Check if crossing horizontal road
        if -20 <= z <= 20:
            # At left intersection
            if -87 <= x <= -53:
                return True
            # At right intersection
            if 53 <= x <= 87:
                return True

        # Check if crossing vertical roads
        if (-90 <= x <= -50) or (50 <= x <= 90):
            # At crosswalk zones
            if -22 <= z <= 22:
                return True

        return False

    def _is_vehicle_too_close(self, vehicles, safe_distance=30.0) -> bool:
        """Check if any vehicle is too close for safe crossing"""
        for vehicle in vehicles:
            dx = vehicle.position[0] - self.position[0]
            dz = vehicle.position[2] - self.position[2]
            distance = (dx**2 + dz**2) ** 0.5
            if distance < safe_distance:
                return True
        return False

    def draw(self):
        """Render pedestrian as colored sphere"""
        glPushMatrix()
        glTranslatef(*self.position)
        glColor3f(*self.color)
        glutSolidSphere(self.size, 8, 8)
        glPopMatrix()

    def _get_relevant_traffic_light(self, traffic_lights) -> Optional[TrafficLight]:
        """Get the relevant traffic light for the current crossing"""
        x, _, z = self.position

        # For vertical roads (NS direction)
        if (-90 <= x <= -50) or (50 <= x <= 90):
            for light in traffic_lights:
                if light.controls_direction == "NS":
                    # Check if we're near this light's position
                    if abs(x - light.x) < 20 and abs(z - light.z) < 30:
                        return light

        # For horizontal road (EW direction)
        if -25 <= z <= 25:
            for light in traffic_lights:
                if light.controls_direction == "EW":
                    # Check if we're near this light's position
                    if abs(x - light.x) < 30 and abs(z - light.z) < 20:
                        return light

        return None

    def _should_wait_at_crossing(self, traffic_light) -> bool:
        """Determine if pedestrian should wait based on traffic light and personality"""
        if not traffic_light:
            return self.personality == "patient"

        # Check if it's safe to cross (when vehicles have red light)
        safe_to_cross = (
            traffic_light.is_red()
        )  # Vehicles have red light = pedestrians can cross

        # Aggressive pedestrians might cross regardless of light
        if self.personality == "aggressive":
            return False

        # Impulsive pedestrians sometimes ignore unsafe conditions
        if self.personality == "impulsive":
            if not safe_to_cross:  # If it's not safe to cross
                return random.random() > 0.3  # 30% chance to cross anyway
            return False  # Cross if safe

        # Patient pedestrians only cross when safe
        return not safe_to_cross  # Wait if not safe to cross
