# objects/traffic_light.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class TrafficLight:
    def __init__(self):
        # Posición predeterminada; luego se asignará desde main.py
        self.x = 0.0
        self.z = 0.0
        # Altura del poste
        self.pole_height = 20.0
        # Tamaño de la caja del semáforo
        self.box_size = 8.0
        # Radio de las luces
        self.light_radius = 1.5
        # Desplazamiento en z para que las luces queden en la cara frontal de la caja
        self.light_offset_z = self.box_size / 2 + 0.1

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        
        # Dibuja el poste
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.576, 0.671, 0.62)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 1.0, 1.0, self.pole_height, 32, 32)
        glPopMatrix()
        
        # Dibuja la caja en la parte superior
        glPushMatrix()
        glTranslatef(0, self.pole_height, 0)
        glColor3f(0.1, 0.1, 0.1)
        glutSolidCube(self.box_size)
        glPopMatrix()
        
        # Dibuja las luces en la cara frontal de la caja
        # Luz roja (arriba)
        glPushMatrix()
        glTranslatef(0, self.pole_height + self.box_size/4, self.light_offset_z)
        glColor3f(1.0, 0.0, 0.0)
        glutSolidSphere(self.light_radius, 16, 16)
        glPopMatrix()
        
        # Luz amarilla (centro)
        glPushMatrix()
        glTranslatef(0, self.pole_height, self.light_offset_z)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(self.light_radius, 16, 16)
        glPopMatrix()
        
        # Luz verde (abajo)
        glPushMatrix()
        glTranslatef(0, self.pole_height - self.box_size/4, self.light_offset_z)
        glColor3f(0.0, 1.0, 0.0)
        glutSolidSphere(self.light_radius, 16, 16)
        glPopMatrix()
        
        glPopMatrix()
