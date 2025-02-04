# objects/house.py
from OpenGL.GL import *
from .objloader import OBJ
import os

class House:
    def __init__(self, model_path=None, swapyz=True):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'untitled.obj')
        self.model = OBJ(model_path, swapyz=swapyz)
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
