from enum import Enum
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class LightState(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3


class TrafficLight:
    def __init__(self):
        self.x = 0.0
        self.z = 0.0
        self.pole_height = 20.0
        self.box_size = 8.0
        self.light_radius = 1.5
        self.light_offset_z = self.box_size / 2 + 0.1
        self.visible = True  # New attribute to control visibility

        # Traffic light state
        self.current_state = LightState.RED
        self.state_start_time = time.time()
        self.timings = {
            LightState.RED: 10.0,    # 10 seconds
            LightState.YELLOW: 3.0,  # 3 seconds
            LightState.GREEN: 8.0,   # 8 seconds
        }

        # Direction this light controls (set during initialization)
        self.controls_direction = "NS"  # "NS" for North-South, "EW" for East-West
        self.phase_offset = 0.0  # Time offset for synchronization

    def update(self, master_time):
        """Update light state based on master time"""
        cycle_time = sum(self.timings.values())
        adjusted_time = (master_time + self.phase_offset) % cycle_time

        # Determine state based on time in cycle
        if adjusted_time < self.timings[LightState.GREEN]:
            self.current_state = LightState.GREEN
        elif adjusted_time < self.timings[LightState.GREEN] + self.timings[LightState.YELLOW]:
            self.current_state = LightState.YELLOW
        else:
            self.current_state = LightState.RED

    def is_red(self):
        return self.current_state == LightState.RED or self.current_state == LightState.YELLOW

    def draw(self):
        if not self.visible:
            return

        glPushMatrix()
        glTranslatef(self.x, 0, self.z)

        # Draw pole
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.576, 0.671, 0.62)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 1.0, 1.0, self.pole_height, 32, 32)
        glPopMatrix()

        # Draw box
        glPushMatrix()
        glTranslatef(0, self.pole_height, 0)
        glColor3f(0.1, 0.1, 0.1)
        glutSolidCube(self.box_size)
        glPopMatrix()

        # Draw lights with current state
        self._draw_lights()

        glPopMatrix()

    def _draw_lights(self):
        # Red light
        glPushMatrix()
        glTranslatef(0, self.pole_height + self.box_size / 4, self.light_offset_z)
        if self.current_state == LightState.RED:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(0.3, 0.0, 0.0)
        glutSolidSphere(self.light_radius, 16, 16)
        glPopMatrix()

        # Yellow light
        glPushMatrix()
        glTranslatef(0, self.pole_height, self.light_offset_z)
        if self.current_state == LightState.YELLOW:
            glColor3f(1.0, 1.0, 0.0)
        else:
            glColor3f(0.3, 0.3, 0.0)
        glutSolidSphere(self.light_radius, 16, 16)
        glPopMatrix()

        # Green light
        glPushMatrix()
        glTranslatef(0, self.pole_height - self.box_size / 4, self.light_offset_z)
        if self.current_state == LightState.GREEN:
            glColor3f(0.0, 1.0, 0.0)
        else:
            glColor3f(0.0, 0.3, 0.0)
        glutSolidSphere(self.light_radius, 16, 16)
        glPopMatrix()
