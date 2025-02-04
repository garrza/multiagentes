# objects/car.py
from OpenGL.GL import *
from .objloader import OBJ

class Car:
    def __init__(self, model_path, swapyz=True):
        self.model = OBJ(model_path, swapyz=swapyz)
        self.model.generate()
        # Posición y otros parámetros iniciales
        self.x = -60
        # self.y = 15.0
        self.y = 0
        self.z = 140
        self.rotation = 0.0  # Si deseas rotar el coche
        self.scale = 2.0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glRotatef(-90.0, 0.0, 0.0, 1.0)
        glScalef(self.scale, self.scale, self.scale)
        # No forzamos un color fijo para usar el color natural del material
        self.model.render()
        glPopMatrix()
