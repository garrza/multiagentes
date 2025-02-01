# environment.py
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluDisk
from OpenGL.GLUT import *

class City:
    def __init__(self):
        # Aquí podrías inicializar parámetros (dimensiones, colores, etc.)
        pass

    def draw_roads(self):
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
        glVertex3f(50.0,  0.0, 150.0)
        glVertex3f(90.0,  0.0, 150.0)
        glVertex3f(90.0,  0.0, -150.0)
        glVertex3f(50.0,  0.0, -150.0)
        glEnd()
        
        # Líneas centrales en blanco
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex3f(-150.0, 0.01, 0.0)
        glVertex3f(150.0,  0.01, 0.0)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(-70.0, 0.01, 150.0)
        glVertex3f(-70.0, 0.01, -150.0)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(70.0, 0.01, 150.0)
        glVertex3f(70.0, 0.01, -150.0)
        glEnd()

    def draw_sidewalks(self):
        glColor3f(0.8, 0.8, 0.8)
        # Aceras de la calle horizontal
        glBegin(GL_QUADS)
        glVertex3f(-150.0, 0.001, 22.0)
        glVertex3f(150.0, 0.001, 22.0)
        glVertex3f(150.0, 0.001, 20.0)
        glVertex3f(-150.0, 0.001, 20.0)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(-150.0, 0.001, -20.0)
        glVertex3f(150.0, 0.001, -20.0)
        glVertex3f(150.0, 0.001, -22.0)
        glVertex3f(-150.0, 0.001, -22.0)
        glEnd()
        
        # Aceras para la vertical izquierda
        glBegin(GL_QUADS)
        glVertex3f(-92.0, 0.001, 150.0)
        glVertex3f(-90.0, 0.001, 150.0)
        glVertex3f(-90.0, 0.001, -150.0)
        glVertex3f(-92.0, 0.001, -150.0)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(-50.0, 0.001, 150.0)
        glVertex3f(-48.0, 0.001, 150.0)
        glVertex3f(-48.0, 0.001, -150.0)
        glVertex3f(-50.0, 0.001, -150.0)
        glEnd()
        
        # Aceras para la vertical derecha
        glBegin(GL_QUADS)
        glVertex3f(50.0, 0.001, 150.0)
        glVertex3f(52.0, 0.001, 150.0)
        glVertex3f(52.0, 0.001, -150.0)
        glVertex3f(50.0, 0.001, -150.0)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(90.0, 0.001, 150.0)
        glVertex3f(92.0, 0.001, 150.0)
        glVertex3f(92.0, 0.001, -150.0)
        glVertex3f(90.0, 0.001, -150.0)
        glEnd()

    def draw_buildings(self):
        glColor3f(0.5, 0.5, 0.5)
        # Por ejemplo, tres edificios con posiciones separadas
        building_positions = [
            (-28, -38),
            (5, -38),
            (-28, -100)
        ]
        for pos in building_positions:
            x, z = pos
            glPushMatrix()
            glTranslatef(x, 15, z)
            glScalef(31, 31, 31)
            glutSolidCube(1)
            glPopMatrix()

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
            (20, 0, 110)
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
        bush_radius = 2.0      # Radio del arbusto (se mantiene el tamaño)
        spacing = 15.0         # Espaciado entre arbustos
        margin = 5.0           # Margen interno para reducir el perímetro

        # Límites internos para la colocación de arbustos:
        x_min = -50.0 + margin   # -65.0
        x_max = 50.0 - margin    # 65.0
        z_bottom = 30.0 + margin # 35.0
        z_top = 130.0 - margin   # 125.0

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

    def draw(self):
        self.draw_roads()
        self.draw_sidewalks()
        self.draw_park()
        self.draw_buildings()
        self.draw_park_bushes()  # Ahora los arbustos se colocan en el perímetro reducido
        self.draw_pool()



