# main.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from environment import City
from objects.car import Car
from objects.traffic_light import TrafficLight  # Asegúrate de que TrafficLight esté implementado

WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600

# Variables globales para los elementos de la escena
city = None
car = None
traffic_lights = []  # Lista para los semáforos

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    city.draw()       # Dibuja el entorno
    car.draw()        # Dibuja el coche 
    for tl in traffic_lights:
        tl.draw()     # Dibuja cada semáforo
    glutSwapBuffers()

def main():
    global city, car, house, traffic_lights
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Simulacion de Trafico - Ciudad Organizada")
    
    init()
    
    # Inicializa el entorno y los objetos
    city = City()
    car = Car("models/untitled.obj", swapyz=True)
    
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
    
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
