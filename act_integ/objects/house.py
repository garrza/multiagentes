# objects/house.py
from OpenGL.GL import *
from .objloader import OBJ

class House:
    def __init__(self, model_path, swapyz=True):
        self.model = OBJ(model_path, swapyz=swapyz)
        self.model.generate()
        # Posición y otros parámetros iniciales para la casa
        self.x = 100.0
        self.y = 0.0
        self.z = -50.0
        self.rotation = 0.0  # Rotación alrededor del eje Y
        self.scale = 1.5

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rotation, 0.0, 1.0, 0.0)
        glScalef(self.scale, self.scale, self.scale)
        self.model.render()
        glPopMatrix()
