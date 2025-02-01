# environment.py
# environment.py
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluCylinder  # Agregado para que gluNewQuadric esté definido
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

    def draw(self):
        self.draw_roads()
        self.draw_sidewalks()
        self.draw_park()
        self.draw_buildings()
