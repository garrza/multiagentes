# main.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

    # Lighting setup
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 300.0, 300.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(
        0.0, 200.0, 250.0,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )
    
    # Dibujar elementos
    city.draw()
    car.draw()
    for tl in traffic_lights:
        tl.draw()
    
    pygame.display.flip()

def main():
    global city, car, traffic_lights
    
    # Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), 
        pygame.DOUBLEBUF | pygame.OPENGL
    )
    
    # OpenGL initialization
    glClearColor(0.09, 0.6, 0.149, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, WINDOW_WIDTH/float(WINDOW_HEIGHT), 1.0, 2000.0)
    glMatrixMode(GL_MODELVIEW)

    # Lighting setup
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 300.0, 300.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

    # Game initialization
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
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update game state
        # (Add your game logic here)
        
        # Render frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.0, 200.0, 250.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        
        # Draw game objects
        city.draw()
        car.draw()
        for tl in traffic_lights:
            tl.draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
