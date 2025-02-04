# main.py
import pygame
import time
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from model import TrafficModel
from environment import City
from objects.car import Car
from objects.traffic_light import TrafficLight  # Asegúrate de que TrafficLight esté implementado

WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600

# Variables globales para los elementos de la escena
city = None
car = None
model = None
traffic_lights = []  # Lista para los semáforos

spawner_left = 0
spawner_right = 0
spawner_up = (0, 0, 0)
spawner_down = (-60, 0, 140)

def init():
    pygame.init()
    glClearColor(0.09, 0.6, 0.149, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, WINDOW_WIDTH / float(WINDOW_HEIGHT), 1.0, 2000.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        0.0, 200.0, 250.0,  # Posición de la cámara
        0.0, 0.0, 0.0,      # A dónde mira
        0.0, 1.0, 0.0       # Vector "arriba"
    )

def display():
    """ Renderiza la escena """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    city.draw()       # Dibuja el entorno
    #car.draw()        # Dibuja el coche
    model.draw()
    
    for tl in traffic_lights:
        tl.draw()     # Dibuja cada semáforo
        
    glutSwapBuffers()

def main():
    global city, model, car, traffic_lights
    count = 0
    
    # Inicializar de pygame y OpenGL
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Simulacion de Trafico - Ciudad Organizada")
    
    # Inicializar pygame
    pygame.init()
    
    # Inicializar el entorno de OpenGL
    init()
    
    # Inicializa el entorno y los objetos
    city = City()
    model = TrafficModel()
    #car = Car("models/untitled.obj", swapyz=True)
    
    # Crear 4 semáforos y asignarles posiciones (por ejemplo, en cada esquina de la intersección)
    # Ajusta los valores según la escala y la posición de tu ciudad.
    positions = [
        (95.0, 25.0),    # Semáforo en la esquina superior derecha
        (-95.0, 30.0),   # Semáforo en la esquina superior izquierda
        (40.0, -25.0),   # Semáforo en la esquina inferior derecha
        (-40.0, -20.0)   # Semáforo en la esquina inferior izquierda
    ]

    for pos in positions:
        tl = TrafficLight()
        tl.x, tl.z = pos  # Asigna la posición deseada
        traffic_lights.append(tl)
        
    running = True
    last_spawn_time = time.time()
    
    while running:
        start_time = time.time()

        # Cerrar la ventana si el usuario presiona la tecla ESC o cierra la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawnear un carro cada 2-5 segundos
        if time.time() - last_spawn_time >= (2 + random.random() * 3):
            last_spawn_time = time.time()

        # Actualizar simulación
        model.step()
        display()
        
        # Control de FPS (60 FPS)
        elapsed_time = time.time() - start_time
        time.sleep(max(1 / 60 - elapsed_time, 0))

    pygame.quit()

if __name__ == "__main__":
    main()
