import pygame
import random
from traffic_light import TrafficLight
from vehicle import RegularVehicle, FastVehicle, SlowVehicle, CompactVehicle


class TrafficSimulation:
    def __init__(self):
        pygame.init()

        # Display settings
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Traffic Intersection Simulation")

        # Colors
        self.ROAD_COLOR = (40, 40, 40)
        self.GRASS_COLOR = (34, 139, 34)
        self.MARKING_COLOR = (255, 255, 255)

        self.ROAD_WIDTH = 80
        self.INTERSECTION_X = self.WIDTH // 2
        self.INTERSECTION_Y = self.HEIGHT // 2

        self.clock = pygame.time.Clock()
        self.running = True
        self.vehicles = []
        self.spawn_timer = 0
        self.SPAWN_RATE = 120

        # Initialize traffic lights
        self.setup_traffic_lights()

    def setup_traffic_lights(self):
        # Position traffic lights at the corners of the intersection
        self.lights = {
            "horizontal": TrafficLight(
                self.INTERSECTION_X
                + self.ROAD_WIDTH // 2
                + 10,  # Right of intersection
                self.INTERSECTION_Y
                - self.ROAD_WIDTH // 2
                - 10,  # Top edge of horizontal road
                0,
            ),
            "vertical": TrafficLight(
                self.INTERSECTION_X
                + self.ROAD_WIDTH // 2
                + 10,  # Right of intersection
                self.INTERSECTION_Y - self.ROAD_WIDTH // 2 - 10,  # Above intersection
                90,
            ),
        }

        # Link traffic lights
        self.lights["horizontal"].set_other_light(self.lights["vertical"])
        self.lights["vertical"].set_other_light(self.lights["horizontal"])

        # Set initial states
        self.lights["horizontal"].state = "GREEN"
        self.lights["vertical"].state = "RED"

    def spawn_vehicle(self):
        if self.spawn_timer <= 0:

            spawn_points = {
                "horizontal": {"x": 0, "y": self.INTERSECTION_Y - self.ROAD_WIDTH // 4},
                "vertical": {
                    "x": self.INTERSECTION_X - self.ROAD_WIDTH // 4,
                    "y": self.HEIGHT,
                },
            }

            # Choose direction and vehicle type
            direction = random.choice(["horizontal", "vertical"])
            vehicle_class = random.choice(
                [RegularVehicle, FastVehicle, SlowVehicle, CompactVehicle]
            )

            # Create vehicle
            new_vehicle = vehicle_class(
                spawn_points[direction]["x"],
                spawn_points[direction]["y"],
                direction,
                self.vehicles,
                self.ROAD_WIDTH,
            )

            # Add vehicle if no collision
            if not any(self.check_collision(new_vehicle, v) for v in self.vehicles):
                self.vehicles.append(new_vehicle)

            self.spawn_timer = self.SPAWN_RATE + random.randint(-20, 20)
        else:
            self.spawn_timer -= 1

    def check_collision(self, v1, v2):
        return (
            abs(v1.x - v2.x) < max(v1.width, v2.width) + 10
            and abs(v1.y - v2.y) < max(v1.height, v2.height) + 10
        )

    def draw_roads(self):
        # Fill background with grass
        self.screen.fill(self.GRASS_COLOR)

        # Draw horizontal road
        pygame.draw.rect(
            self.screen,
            self.ROAD_COLOR,
            (
                0,
                self.INTERSECTION_Y - self.ROAD_WIDTH // 2,
                self.WIDTH,
                self.ROAD_WIDTH,
            ),
        )

        # Draw vertical road
        pygame.draw.rect(
            self.screen,
            self.ROAD_COLOR,
            (
                self.INTERSECTION_X - self.ROAD_WIDTH // 2,
                0,
                self.ROAD_WIDTH,
                self.HEIGHT,
            ),
        )

        # Draw road markings
        self.draw_road_markings()

    def draw_road_markings(self):
        # Parameters for dashed lines
        dash_length = 30
        gap_length = 20
        line_width = 2

        # Horizontal road center line
        y = self.INTERSECTION_Y
        for x in range(0, self.WIDTH, dash_length + gap_length):
            if (
                x > self.INTERSECTION_X + self.ROAD_WIDTH // 2
                or x < self.INTERSECTION_X - self.ROAD_WIDTH // 2
            ):
                pygame.draw.rect(
                    self.screen,
                    self.MARKING_COLOR,
                    (x, y - line_width // 2, dash_length, line_width),
                )

        # Vertical road center line
        x = self.INTERSECTION_X
        for y in range(0, self.HEIGHT, dash_length + gap_length):
            if (
                y > self.INTERSECTION_Y + self.ROAD_WIDTH // 2
                or y < self.INTERSECTION_Y - self.ROAD_WIDTH // 2
            ):
                pygame.draw.rect(
                    self.screen,
                    self.MARKING_COLOR,
                    (x - line_width // 2, y, line_width, dash_length),
                )

    def update(self):
        # Update traffic lights
        for light in self.lights.values():
            light.update()

        # Update vehicles
        for vehicle in self.vehicles[:]:
            if vehicle.direction == "horizontal":
                vehicle.update(self.lights["horizontal"], self.INTERSECTION_X)
                if vehicle.x > self.WIDTH:
                    self.vehicles.remove(vehicle)
            else:
                vehicle.update(self.lights["vertical"], self.INTERSECTION_Y)
                if vehicle.y < 0:
                    self.vehicles.remove(vehicle)

        self.spawn_vehicle()

    def draw(self):
        self.draw_roads()

        # Draw vehicles
        for vehicle in self.vehicles:
            vehicle.draw(self.screen)

        # Draw traffic lights
        for light in self.lights.values():
            light.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    sim = TrafficSimulation()
    sim.run()
    pygame.quit()
