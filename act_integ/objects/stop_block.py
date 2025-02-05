from OpenGL.GL import *


class StopBlock:
    def __init__(self, x, z, width, depth, direction):
        self.x = x
        self.z = z
        self.width = width
        self.depth = depth
        self.direction = direction  # "NS" or "EW"
        self.active = True  # Synced with traffic light
        self.visible = False  # For debugging, set to True to see the blocks

    def update(self, light_state):
        """Sync with traffic light state"""
        self.active = light_state.is_red()

    def is_colliding(self, vehicle_pos) -> bool:
        """Check if vehicle is colliding with this stop block"""
        # Calculate block boundaries
        x_min = self.x - self.width / 2
        x_max = self.x + self.width / 2
        z_min = self.z - self.depth / 2
        z_max = self.z + self.depth / 2

        # Check if vehicle position is within block boundaries
        return x_min <= vehicle_pos[0] <= x_max and z_min <= vehicle_pos[2] <= z_max

    def draw(self):
        """Draw the stop block (for debugging)"""
        if not self.visible:
            return

        glPushMatrix()
        glTranslatef(self.x, 0.1, self.z)  # Slightly above ground

        # Red when active, transparent green when inactive
        if self.active:
            glColor4f(1.0, 0.0, 0.0, 0.5)  # Semi-transparent red
        else:
            glColor4f(0.0, 1.0, 0.0, 0.3)  # Semi-transparent green

        glBegin(GL_QUADS)
        glVertex3f(-self.width / 2, 0, -self.depth / 2)
        glVertex3f(self.width / 2, 0, -self.depth / 2)
        glVertex3f(self.width / 2, 0, self.depth / 2)
        glVertex3f(-self.width / 2, 0, self.depth / 2)
        glEnd()

        glPopMatrix()
