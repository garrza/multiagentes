import agentpy as ap
import random
from vehicles import AUTO
from OpenGL.GL import *
from objects.objloader import OBJ

class VehicleAgent(ap.Agent):
    def setup(self):
        """ Selecciona aleatoriamente un tipo de vehículo y su posición inicial """
        self.vehiculo = random.choice([AUTO])  # Random vehicle type
        self.speed = 0.5  # Initial speed
        self.assign_spawn_point()  # Assign a random spawn location and path
        
        # Modelo del coche
        self.model_path = "untitled.obj"
        self.model = OBJ(self.model_path, swapyz=True)
        self.model.generate()
        
        self.scale = 4.0  # Escala para el coche

    def assign_spawn_point(self):
        """ Asigna una posición de aparición aleatoria y su ruta correspondiente """
        spawn_options = ["left", "right", "top", "bottom"]
        spawn_side = random.choice(spawn_options)  # Choose a random side

        if spawn_side == "left":
            self.position = [-140, 0, 5]  # Spawn on left
            self.path_id = random.choice([2, 3])  # Turn left or right

        elif spawn_side == "right":
            self.position = [140, 0, -10]  # Spawn on right
            self.path_id = random.choice([2, 3])  # Turn left or right

        elif spawn_side == "bottom":
            self.position = [-57, 0, 135]  # Spawn at top
            self.path_id = 1  # Moves straight

        elif spawn_side == "top":
            self.position = [63, 0, -135]  # Spawn at bottom
            self.path_id = 1  # Moves straight

    def move_along_path(self):
        
        """ Define la trayectoria del vehículo según su camino asignado """
        self.speed = min(self.speed + self.vehiculo.acceleration, self.vehiculo.max_speed)

        if self.path_id == 1:
            # Path 1: Moves straight forward (Z direction)
            self.position[2] += self.speed  

        elif self.path_id == 2:
            # Path 2: Moves straight, then turns right at Z = 100
            if self.position[2] < 100:
                self.position[2] += self.speed  
            else:
                self.position[0] += self.speed  # Turn right

        elif self.path_id == 3:
            # Path 3: Moves straight, then turns left at Z = 100
            if self.position[2] < 100:
                self.position[2] += self.speed  
            else:
                self.position[0] -= self.speed  # Turn left

    def step(self):
        self.move_along_path()

    def draw(self):
        """ Dibuja el coche en OpenGL """
        glPushMatrix()
        glTranslatef(*self.position) # Establecer la posición del coche
        glScalef(self.scale, self.scale, self.scale)  # Aplicar la escala
        
        # Rotate the vehicle (example: rotating around the Y-axis)
        rotation_angle = 270  # Angle of rotation in degrees (you can change this)
        glRotatef(rotation_angle, 1, 0, 0)  # Rotate around the Y-axis
        
        # Se dibuja
        self.model.render()  # Renderiza el modelo cargado
        glPopMatrix()
