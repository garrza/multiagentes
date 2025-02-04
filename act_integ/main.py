import os
import time
import random
from typing import List, Optional

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from models.traffic_model import TrafficModel
from environment.city import City
from objects.traffic_light import TrafficLight

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TARGET_FPS = 60


class TrafficSimulation:
    def __init__(self):
        self.city: Optional[City] = None
        self.model: Optional[TrafficModel] = None
        self.traffic_lights: List[TrafficLight] = []

    def _init_opengl(self):
        """Initialize OpenGL settings"""
        glClearColor(0.09, 0.6, 0.149, 1.0)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, WINDOW_WIDTH / float(WINDOW_HEIGHT), 1.0, 2000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            0.0,
            200.0,
            250.0,  # Camera position
            0.0,
            0.0,
            0.0,  # Look at point
            0.0,
            1.0,
            0.0,  # Up vector
        )

        # Lighting setup
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 300.0, 300.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

    def _create_traffic_lights(self):
        positions = [
            ((95.0, 25.0), "NS"),  # Top right corner
            ((-95.0, 30.0), "NS"),  # Top left corner
            ((40.0, -25.0), "EW"),  # Bottom right corner
            ((-40.0, -20.0), "EW"),  # Bottom left corner
        ]

        for pos, direction in positions:
            tl = TrafficLight()
            tl.x, tl.z = pos
            tl.controls_direction = direction
            self.traffic_lights.append(tl)

    def display(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.0, 200.0, 250.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        self.city.draw()
        self.model.draw()

        for tl in self.traffic_lights:
            tl.draw()

        pygame.display.flip()

    def run(self):
        """Main simulation loop"""
        pygame.init()
        pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL
        )
        pygame.display.set_caption("Traffic Simulation - Organized City")

        self._init_opengl()

        # Initialize simulation components
        self.city = City()
        self._create_traffic_lights()
        self.model = TrafficModel(traffic_lights=self.traffic_lights)

        running = True
        last_spawn_time = time.time()

        while running:
            start_time = time.time()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Spawn vehicles periodically
            if time.time() - last_spawn_time >= (2 + random.random() * 3):
                last_spawn_time = time.time()

            # Update simulation
            self.model.step()
            self.display()

            # Control frame rate
            elapsed_time = time.time() - start_time
            time.sleep(max(1 / TARGET_FPS - elapsed_time, 0))

        pygame.quit()


def main():
    simulation = TrafficSimulation()
    simulation.run()


if __name__ == "__main__":
    main()
