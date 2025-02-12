# environment.py
import random
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluDisk
from OpenGL.GLUT import *


class City:
    def __init__(self):
        # Building dimensions and spacing
        self.building_width = 20  # X-axis footprint
        self.building_depth = 20  # Z-axis footprint
        self.min_gap = 5

        # Define building zones (x_start, x_end, z_start, z_end)
        self.building_zones = [
            (-150, -90, -110, -30),  # Left bottom quadrant
            (-150, -90, 30, 110),  # Left top quadrant
            (90, 150, -110, -30),  # Right bottom quadrant
            (90, 150, 30, 110),  # Right top quadrant
            (-50, 50, -110, -30),  # Bottom center (original zone)
        ]

        # Generate building positions for all zones
        self.building_positions = []

        for zone in self.building_zones:
            x_start, x_end, z_start, z_end = zone

            # Calculate available space for this zone
            x_span = x_end - x_start
            z_span = z_end - z_start

            # Calculate maximum buildings per axis for this zone
            max_x = int((x_span - self.min_gap) / (self.building_width + self.min_gap))
            max_z = int((z_span - self.min_gap) / (self.building_depth + self.min_gap))

            # Calculate actual spacing with even margins
            x_spacing = (x_span - (max_x * self.building_width)) / (max_x + 1)
            z_spacing = (z_span - (max_z * self.building_depth)) / (max_z + 1)

            # Generate grid positions for this zone
            for i in range(max_x):
                for j in range(max_z):
                    x = x_start + x_spacing * (i + 1) + self.building_width * (i + 0.5)
                    z = z_start + z_spacing * (j + 1) + self.building_depth * (j + 0.5)
                    self.building_positions.append((x, z))

        # Window parameters
        self.window_height = 0.15
        self.mullion = 0.05
        self.row_height = self.window_height + self.mullion

        # Generate random number of rows and calculate heights
        self.window_rows = [random.randint(5, 15) for _ in self.building_positions]
        self.building_heights = [
            rows * self.row_height * 30 for rows in self.window_rows
        ]

    def draw_roads(self):
        # Draw base road surfaces
        glColor3f(0.3, 0.3, 0.3)

        # Calle horizontal: x de -150 a 150, z entre -20 y 20
        glBegin(GL_QUADS)
        glVertex3f(-150.0, 0.0, 20.0)
        glVertex3f(150.0, 0.0, 20.0)
        glVertex3f(150.0, 0.0, -20.0)
        glVertex3f(-150.0, 0.0, -20.0)
        glEnd()

        # Calle vertical izquierda: x de -90 a -50, z de -150 a 150
        glBegin(GL_QUADS)
        glVertex3f(-90.0, 0.0, 150.0)
        glVertex3f(-50.0, 0.0, 150.0)
        glVertex3f(-50.0, 0.0, -150.0)
        glVertex3f(-90.0, 0.0, -150.0)
        glEnd()

        # Calle vertical derecha: x de 50 a 90, z de -150 a 150
        glBegin(GL_QUADS)
        glVertex3f(50.0, 0.0, 150.0)
        glVertex3f(90.0, 0.0, 150.0)
        glVertex3f(90.0, 0.0, -150.0)
        glVertex3f(50.0, 0.0, -150.0)
        glEnd()

        # Draw road markings
        glColor3f(1.0, 1.0, 1.0)  # White color for lines
        glLineWidth(2.0)

        # Center lines for roads
        glBegin(GL_LINES)
        # Horizontal road center line
        glVertex3f(-150.0, 0.01, 0.0)
        glVertex3f(150.0, 0.01, 0.0)
        # Left vertical road center line
        glVertex3f(-70.0, 0.01, 150.0)
        glVertex3f(-70.0, 0.01, -150.0)
        # Right vertical road center line
        glVertex3f(70.0, 0.01, 150.0)
        glVertex3f(70.0, 0.01, -150.0)
        glEnd()

        # Draw intersection markings
        def draw_intersection_lines(x_start, x_end, z_start, z_end, segments=6):
            segment_length = (x_end - x_start) / segments
            for i in range(segments + 1):
                x = x_start + segment_length * i
                glBegin(GL_LINES)
                glVertex3f(x, 0.15, z_start)  # Raised above sidewalk
                glVertex3f(x, 0.15, z_end)  # Raised above sidewalk
                glEnd()

        def draw_vertical_intersection_lines(
            x_start, x_end, z_start, z_end, segments=6
        ):
            segment_length = (z_end - z_start) / segments
            for i in range(segments + 1):
                z = z_start + segment_length * i
                glBegin(GL_LINES)
                glVertex3f(x_start, 0.15, z)  # Raised above sidewalk
                glVertex3f(x_end, 0.15, z)  # Raised above sidewalk
                glEnd()

        # Draw crosswalk background rectangles in light gray
        glColor3f(0.85, 0.85, 0.85)  # Light gray for crosswalk background

        def draw_crosswalk_background(x1, x2, z1, z2):
            glBegin(GL_QUADS)
            glVertex3f(x1, 0.12, z1)
            glVertex3f(x2, 0.12, z1)
            glVertex3f(x2, 0.12, z2)
            glVertex3f(x1, 0.12, z2)
            glEnd()

        # Draw crosswalk backgrounds
        # Left intersection
        draw_crosswalk_background(-90, -50, 20, 25)  # North
        draw_crosswalk_background(-90, -50, -25, -20)  # South
        draw_crosswalk_background(-90, -85, -20, 20)  # West
        draw_crosswalk_background(-55, -50, -20, 20)  # East

        # Right intersection
        draw_crosswalk_background(50, 90, 20, 25)  # North
        draw_crosswalk_background(50, 90, -25, -20)  # South
        draw_crosswalk_background(50, 55, -20, 20)  # West
        draw_crosswalk_background(85, 90, -20, 20)  # East

        # Draw crosswalk lines in white
        glColor3f(1.0, 1.0, 1.0)  # White for crosswalk lines

        # Left intersection horizontal lines
        draw_intersection_lines(-90, -50, 20, 25)  # North side
        draw_intersection_lines(-90, -50, -25, -20)  # South side

        # Right intersection horizontal lines
        draw_intersection_lines(50, 90, 20, 25)  # North side
        draw_intersection_lines(50, 90, -25, -20)  # South side

        # Left intersection vertical lines
        draw_vertical_intersection_lines(-90, -85, -20, 20)  # West side
        draw_vertical_intersection_lines(-55, -50, -20, 20)  # East side

        # Right intersection vertical lines
        draw_vertical_intersection_lines(50, 55, -20, 20)  # West side
        draw_vertical_intersection_lines(85, 90, -20, 20)  # East side

        # Draw stop lines at intersections
        glLineWidth(4.0)  # Thicker lines for stop lines
        glBegin(GL_LINES)
        # Left intersection stop lines
        glVertex3f(-90, 0.15, 20)
        glVertex3f(-50, 0.15, 20)
        glVertex3f(-90, 0.15, -20)
        glVertex3f(-50, 0.15, -20)
        glVertex3f(-90, 0.15, 20)
        glVertex3f(-90, 0.15, -20)
        glVertex3f(-50, 0.15, 20)
        glVertex3f(-50, 0.15, -20)

        # Right intersection stop lines
        glVertex3f(50, 0.15, 20)
        glVertex3f(90, 0.15, 20)
        glVertex3f(50, 0.15, -20)
        glVertex3f(90, 0.15, -20)
        glVertex3f(50, 0.15, 20)
        glVertex3f(50, 0.15, -20)
        glVertex3f(90, 0.15, 20)
        glVertex3f(90, 0.15, -20)
        glEnd()

        glLineWidth(2.0)  # Reset line width

    def draw_sidewalks(self):
        """Draw sidewalks along all roads"""
        glColor3f(0.8, 0.8, 0.8)  # Light gray color
        sidewalk_width = 5.0
        sidewalk_height = 0.1

        # Helper function to draw a sidewalk segment
        def draw_sidewalk_segment(x1, z1, x2, z2):
            glBegin(GL_QUADS)
            glVertex3f(x1, sidewalk_height, z1)
            glVertex3f(x2, sidewalk_height, z1)
            glVertex3f(x2, sidewalk_height, z2)
            glVertex3f(x1, sidewalk_height, z2)
            glEnd()

        # Horizontal road sidewalks
        # North side
        draw_sidewalk_segment(-150, 20, 150, 20 + sidewalk_width)
        # South side
        draw_sidewalk_segment(-150, -20 - sidewalk_width, 150, -20)

        # Left vertical road sidewalks
        # West side
        draw_sidewalk_segment(-90 - sidewalk_width, -150, -90, 150)
        # East side
        draw_sidewalk_segment(-50, -150, -50 + sidewalk_width, 150)

        # Right vertical road sidewalks
        # West side
        draw_sidewalk_segment(50 - sidewalk_width, -150, 50, 150)
        # East side
        draw_sidewalk_segment(90, -150, 90 + sidewalk_width, 150)

    def draw_window_grid(
        self, face_width, face_height, ideal_window_width, ideal_window_height, mullion
    ):
        """Dynamically draws window grid on a building face"""
        # Calculate maximum possible columns/rows
        cols = int((face_width + mullion) // (ideal_window_width + mullion))
        rows = int((face_height + mullion) // (ideal_window_height + mullion))

        # Calculate actual window dimensions to fit perfectly
        window_w = (face_width - (cols + 1) * mullion) / cols
        window_h = (face_height - (rows + 1) * mullion) / rows

        # Calculate starting positions (lower-left corner)
        start_x = -face_width / 2 + mullion + window_w / 2
        start_y = -face_height / 2 + mullion + window_h / 2

        # Draw each window
        for col in range(cols):
            for row in range(rows):
                x = start_x + col * (window_w + mullion)
                y = start_y + row * (window_h + mullion)
                glPushMatrix()
                glTranslatef(x, y, 0)
                glScalef(window_w, window_h, 0.01)
                glutSolidCube(1)
                glPopMatrix()

    def draw_buildings(self):
        glPushAttrib(GL_LIGHTING_BIT)  # Save current lighting/material state

        # Base material (light gray concrete)
        building_material = {
            "ambient": (0.85, 0.85, 0.85, 1.0),
            "diffuse": (0.95, 0.95, 0.95, 1.0),
            "specular": (0.3, 0.3, 0.3, 1.0),
            "shininess": 30.0,
        }

        glDisable(GL_COLOR_MATERIAL)  # Temporarily disable color tracking
        glMaterialfv(GL_FRONT, GL_AMBIENT, building_material["ambient"])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, building_material["diffuse"])
        glMaterialfv(GL_FRONT, GL_SPECULAR, building_material["specular"])
        glMaterialf(GL_FRONT, GL_SHININESS, building_material["shininess"])

        # Draw buildings with windows on multiple faces
        for pos, height, rows in zip(
            self.building_positions, self.building_heights, self.window_rows
        ):
            x, z = pos
            glPushMatrix()
            # Position the building
            glTranslatef(x, height / 2, z)
            glScalef(self.building_width, height, self.building_depth)

            # Draw base cube representing the building
            glutSolidCube(1)

            # Draw window details on multiple faces
            glDisable(GL_LIGHTING)
            glColor3f(0.2, 0.4, 0.8)  # Medium blue for windows

            # Front face (Z+)
            glPushMatrix()
            glTranslatef(0, 0, 0.501)
            self.draw_window_grid(
                1.0, 1.0, self.row_height, self.window_height, self.mullion
            )
            glPopMatrix()

            # Back face (Z-)
            glPushMatrix()
            glTranslatef(0, 0, -0.501)
            glRotatef(180, 0, 1, 0)
            self.draw_window_grid(
                1.0, 1.0, self.row_height, self.window_height, self.mullion
            )
            glPopMatrix()

            # Right face (X+)
            glPushMatrix()
            glTranslatef(0.501, 0, 0)
            glRotatef(90, 0, 1, 0)
            self.draw_window_grid(
                1.0, 1.0, self.row_height, self.window_height, self.mullion
            )
            glPopMatrix()

            # Left face (X-)
            glPushMatrix()
            glTranslatef(-0.501, 0, 0)
            glRotatef(-90, 0, 1, 0)
            self.draw_window_grid(
                1.0, 1.0, self.row_height, self.window_height, self.mullion
            )
            glPopMatrix()

            glEnable(GL_LIGHTING)
            glPopMatrix()

        glPopAttrib()  # Restore previous lighting/material state

    def draw_tree(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.55, 0.27, 0.07)
        quad = gluNewQuadric()
        gluCylinder(quad, 1.0, 1.0, 10.0, 12, 3)
        glTranslatef(0, 0, 10.0)
        glColor3f(0.0, 0.8, 0.0)
        glutSolidSphere(3.0, 12, 12)
        glPopMatrix()

    def draw_park(self):
        # Área del parque
        glColor3f(0.4, 0.8, 0.4)
        glBegin(GL_QUADS)
        glVertex3f(-70, 0.0, 30)
        glVertex3f(70, 0.0, 30)
        glVertex3f(70, 0.0, 130)
        glVertex3f(-70, 0.0, 130)
        glEnd()
        # Árboles en el parque
        tree_positions = [
            (-40, 0, 50),
            (0, 0, 70),
            (40, 0, 50),
            (-20, 0, 110),
            (20, 0, 110),
        ]
        for pos in tree_positions:
            self.draw_tree(*pos)

    def draw_park_bushes(self):
        """
        Dibuja arbustos a lo largo del perímetro del parque usando un margen interno.
        El parque se define en el área de:
        (-70, 0, 30) a (70, 0, 130).
        Con un margen de 5 unidades, los arbustos se colocarán en:
        x de -65 a 65 y z de 35 a 125.
        """
        glColor3f(0.0, 0.6, 0.0)  # Color verde para los arbustos
        bush_radius = 2.0  # Radio del arbusto (se mantiene el tamaño)
        spacing = 15.0  # Espaciado entre arbustos
        margin = 5.0  # Margen interno para reducir el perímetro

        # Límites internos para la colocación de arbustos:
        x_min = -50.0 + margin  # -65.0
        x_max = 50.0 - margin  # 65.0
        z_bottom = 30.0 + margin  # 35.0
        z_top = 130.0 - margin  # 125.0

        # Borde inferior: z = z_bottom, x de x_min a x_max
        x = x_min
        while x <= x_max:
            glPushMatrix()
            glTranslatef(x, 1.0, z_bottom)
            glutSolidSphere(bush_radius, 16, 16)
            glPopMatrix()
            x += spacing

        # Borde superior: z = z_top, x de x_min a x_max
        x = x_min
        while x <= x_max:
            glPushMatrix()
            glTranslatef(x, 1.0, z_top)
            glutSolidSphere(bush_radius, 16, 16)
            glPopMatrix()
            x += spacing

        # Borde izquierdo: x = x_min, z de z_bottom a z_top (omitiendo esquinas duplicadas)
        z = z_bottom + spacing
        while z <= z_top - spacing:
            glPushMatrix()
            glTranslatef(x_min, 1.0, z)
            glutSolidSphere(bush_radius, 16, 16)
            glPopMatrix()
            z += spacing

        # Borde derecho: x = x_max, z de z_bottom a z_top
        z = z_bottom + spacing
        while z <= z_top - spacing:
            glPushMatrix()
            glTranslatef(x_max, 1.0, z)
            glutSolidSphere(bush_radius, 16, 16)
            glPopMatrix()
            z += spacing

    def draw_pool(self):
        # Dibujar una alberca (piscina) usando un disco azul
        glPushMatrix()
        # Colocar la alberca en una posición adecuada, por ejemplo, en el centro del parque
        glTranslatef(0, 0.001, 100)
        glColor3f(0.0, 0.5, 1.0)  # Azul para el agua
        quadric = gluNewQuadric()
        gluDisk(quadric, 0.0, 15.0, 32, 1)
        glPopMatrix()

    def draw_crosswalks(self):
        """Draw zebra crossings at intersections"""
        # First draw white base for crosswalk
        glColor3f(0.8, 0.8, 0.8)  # Light gray like sidewalks

        def draw_crosswalk_base(x, z, horizontal=True):
            if horizontal:
                width = 8.0  # Length of crossing
                depth = 5.0  # Width of crossing
                glBegin(GL_QUADS)
                glVertex3f(x, 0.02, z - depth / 2)
                glVertex3f(x + width, 0.02, z - depth / 2)
                glVertex3f(x + width, 0.02, z + depth / 2)
                glVertex3f(x, 0.02, z + depth / 2)
                glEnd()
            else:
                width = 5.0  # Width of crossing
                depth = 8.0  # Length of crossing
                glBegin(GL_QUADS)
                glVertex3f(x - width / 2, 0.02, z)
                glVertex3f(x + width / 2, 0.02, z)
                glVertex3f(x + width / 2, 0.02, z + depth)
                glVertex3f(x - width / 2, 0.02, z + depth)
                glEnd()

        # Draw yellow stripes
        def draw_crosswalk_stripes(x, z, horizontal=True):
            glColor3f(1.0, 0.8, 0.0)  # Yellow color for stripes
            stripe_width = 0.5
            stripe_spacing = 0.5
            if horizontal:
                width = 8.0  # Length of crossing
                depth = 5.0  # Width of crossing
                num_stripes = int(depth / (stripe_width + stripe_spacing))
                for i in range(num_stripes):
                    offset = i * (stripe_width + stripe_spacing) - depth / 2
                    glBegin(GL_QUADS)
                    glVertex3f(x, 0.03, z + offset)
                    glVertex3f(x + width, 0.03, z + offset)
                    glVertex3f(x + width, 0.03, z + offset + stripe_width)
                    glVertex3f(x, 0.03, z + offset + stripe_width)
                    glEnd()
            else:
                width = 5.0  # Width of crossing
                depth = 8.0  # Length of crossing
                num_stripes = int(width / (stripe_width + stripe_spacing))
                for i in range(num_stripes):
                    offset = i * (stripe_width + stripe_spacing) - width / 2
                    glBegin(GL_QUADS)
                    glVertex3f(x + offset, 0.03, z)
                    glVertex3f(x + offset + stripe_width, 0.03, z)
                    glVertex3f(x + offset + stripe_width, 0.03, z + depth)
                    glVertex3f(x + offset, 0.03, z + depth)
                    glEnd()

        # Draw crosswalks at each intersection
        crosswalk_positions = [
            # Left intersection
            {"x": -75, "z": -25, "horizontal": True},  # South
            {"x": -75, "z": 20, "horizontal": True},  # North
            {"x": -90, "z": -2.5, "horizontal": False},  # West
            {"x": -55, "z": -2.5, "horizontal": False},  # East
            # Right intersection
            {"x": 65, "z": -25, "horizontal": True},  # South
            {"x": 65, "z": 20, "horizontal": True},  # North
            {"x": 85, "z": -2.5, "horizontal": False},  # West
            {"x": 50, "z": -2.5, "horizontal": False},  # East
        ]

        # Draw all crosswalks
        for pos in crosswalk_positions:
            # First draw the base (light gray)
            draw_crosswalk_base(pos["x"], pos["z"], pos["horizontal"])
            # Then draw the yellow stripes on top
            draw_crosswalk_stripes(pos["x"], pos["z"], pos["horizontal"])

    def draw(self):
        self.draw_roads()
        self.draw_sidewalks()
        self.draw_crosswalks()  # Add crosswalks
        self.draw_park()
        self.draw_buildings()
        self.draw_park_bushes()  # Ahora los arbustos se colocan en el perímetro reducido
        self.draw_pool()
