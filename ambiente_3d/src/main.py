import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import serial
import collections

# Configuração da porta serial
try:
    ser = serial.Serial('COM4', 115200, timeout=1)
except Exception as e:
    print(f"Erro ao abrir a porta serial: {e}")
    ser = None

# Fila para o filtro de média móvel
window_size = 5
yaw_buffer = collections.deque([0.0] * window_size, maxlen=window_size)
pitch_buffer = collections.deque([0.0] * window_size, maxlen=window_size)
roll_buffer = collections.deque([0.0] * window_size, maxlen=window_size)
yaw2_buffer = collections.deque([0.0] * window_size, maxlen=window_size)
pitch2_buffer = collections.deque([0.0] * window_size, maxlen=window_size)
roll2_buffer = collections.deque([0.0] * window_size, maxlen=window_size)

def read_serial():
    try:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            values = data.split('/')
            if len(values) == 6:
                yaw_buffer.append(float(values[0]))
                pitch_buffer.append(float(values[1]))
                roll_buffer.append(float(values[2]))
                yaw2_buffer.append(float(values[3]))
                pitch2_buffer.append(float(values[4]))
                roll2_buffer.append(float(values[5]))
    except Exception as e:
        print(f"Erro na leitura da porta serial: {e}")

def get_filtered_value(buffer):
    return sum(buffer) / len(buffer)

def init_gl():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def draw_paper_plane():
    glBegin(GL_QUADS)
      # Frente
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f( 0.5,  0.1, -1.0)
    glVertex3f(-0.5,  0.1, -1.0)
    glVertex3f(-0.5, -0.1, -1.0)
    glVertex3f( 0.5, -0.1, -1.0)
    # Traseira
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f( 0.5,  0.1, 1.0)
    glVertex3f(-0.5,  0.1, 1.0)
    glVertex3f(-0.5, -0.1, 1.0)
    glVertex3f( 0.5, -0.1, 1.0)
    # Esquerda
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.5,  0.1, -1.0)
    glVertex3f(-0.5,  0.1, 1.0)
    glVertex3f(-0.5, -0.1, 1.0)
    glVertex3f(-0.5, -0.1, -1.0)
    # Direita
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(0.5,  0.1, -1.0)
    glVertex3f(0.5,  0.1, 1.0)
    glVertex3f(0.5, -0.1, 1.0)
    glVertex3f(0.5, -0.1, -1.0)
    # Topo
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f( 0.5,  0.1, -1.0)
    glVertex3f(-0.5,  0.1, -1.0)
    glVertex3f(-0.5,  0.1, 1.0)
    glVertex3f( 0.5,  0.1, 1.0)
    # Base
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f( 0.5, -0.1, -1.0)
    glVertex3f(-0.5, -0.1, -1.0)
    glVertex3f(-0.5, -0.1, 1.0)
    glVertex3f( 0.5, -0.1, 1.0)
    glEnd()

def draw_airplane_instance(x, y, z, yaw, pitch, roll):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(yaw, 0, 1, 0)
    glRotatef(pitch, 1, 0, 0)
    glRotatef(roll, 0, 0, 1)
    draw_paper_plane()
    glPopMatrix()

def update_camera():
    glLoadIdentity()
    gluLookAt(6, 4, 10,  0, 0, 0,  0, 1, 0)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulação de Aviões de Papel com MPU6050")
    
    init_gl()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        read_serial()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        yaw1 = get_filtered_value(yaw_buffer)
        pitch1 = get_filtered_value(pitch_buffer)
        roll1 = get_filtered_value(roll_buffer)
        yaw2 = get_filtered_value(yaw2_buffer)
        pitch2 = get_filtered_value(pitch2_buffer)
        roll2 = get_filtered_value(roll2_buffer)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        update_camera()
        
        draw_airplane_instance(-2, 0, 0, yaw1, pitch1, roll1)
        draw_airplane_instance(2, 0, 0, yaw2, pitch2, roll2)
        
        pygame.display.flip()
    
    pygame.quit()
    if ser:
        ser.close()

if __name__ == '__main__':
    main()
