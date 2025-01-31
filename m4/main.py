import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from objloader import OBJ

WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600

car_obj = None

def init():
    pygame.init()  # para cargar texturas en objloader

    # Fondo verde "pasto"
    glClearColor(0.09, 0.6, 0.149, 1.0)

    # Z-buffer para 3D
    glEnable(GL_DEPTH_TEST)

    # --- Proyección en perspectiva ---
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, WINDOW_WIDTH / float(WINDOW_HEIGHT), 1.0, 1000.0)

    # --- Cámara "como antes" ---
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Por ejemplo, algo como (0,150,130) mirando al origen
    gluLookAt(
        0.0, 150.0, 130.0,  # posición de la cámara
        0.0,   0.0,   0.0,  # a dónde mira
        0.0,   1.0,   0.0   # vector "arriba"
    )

def draw_roads():
    """
    Dibuja la intersección en el plano XZ (y=0):
     - una calle horizontal (x=-100..100, z=-20..20)
     - dos verticales (x=-60..-20 y x=20..60)
     - líneas blancas centrales
    """
    # Carretera gris
    glColor3f(0.3, 0.3, 0.3)

    # -- CALLE HORIZONTAL --
    glBegin(GL_QUADS)
    glVertex3f(-100.0, 0.0,  20.0)
    glVertex3f( 100.0, 0.0,  20.0)
    glVertex3f( 100.0, 0.0, -20.0)
    glVertex3f(-100.0, 0.0, -20.0)
    glEnd()

    # -- VERTICAL IZQUIERDA --
    glBegin(GL_QUADS)
    glVertex3f(-60.0, 0.0,  100.0)
    glVertex3f(-20.0, 0.0,  100.0)
    glVertex3f(-20.0, 0.0, -100.0)
    glVertex3f(-60.0, 0.0, -100.0)
    glEnd()

    # -- VERTICAL DERECHA --
    glBegin(GL_QUADS)
    glVertex3f( 20.0, 0.0,  100.0)
    glVertex3f( 60.0, 0.0,  100.0)
    glVertex3f( 60.0, 0.0, -100.0)
    glVertex3f( 20.0, 0.0, -100.0)
    glEnd()

    # Líneas blancas
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)

    # Línea central horizontal
    glBegin(GL_LINES)
    glVertex3f(-100.0, 0.01, 0.0)
    glVertex3f( 100.0, 0.01, 0.0)
    glEnd()

    # Central vertical izq: x=-40
    glBegin(GL_LINES)
    glVertex3f(-40.0, 0.01,  100.0)
    glVertex3f(-40.0, 0.01, -100.0)
    glEnd()

    # Central vertical der: x=40
    glBegin(GL_LINES)
    glVertex3f(40.0, 0.01,  100.0)
    glVertex3f(40.0, 0.01, -100.0)
    glEnd()

def draw_car():
    """Dibuja el coche con las llantas apuntando hacia "abajo" en la pantalla."""
    if car_obj is None:
        return

    glPushMatrix()

    # Por ejemplo, lo ponemos en z=30, y=0 (sobre la calle horizontal)
    glTranslatef(-65.0, 15.0, 5.0)

    # Ajustamos la rotación para que las llantas queden abajo en la imagen
    # -90° en X "acuesta" el coche sobre el plano XZ
    

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glRotatef(-90.0, 0.0, 0.0, 1.0)

    # Escala
    glScalef(2.0, 2.0, 2.0)

    # Color gris claro
    glColor3f(0.29, 0.341, 0.8)
    car_obj.render()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_roads()
    draw_car()
    glutSwapBuffers()  # Doble buffer

def main():
    global car_obj
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Interseccion 3D")

    init()

    # Cargar tu .obj
    car_obj = OBJ("untitled.obj", swapyz=True)
    car_obj.generate()

    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
