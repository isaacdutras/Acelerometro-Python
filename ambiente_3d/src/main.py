import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import serial
import collections
import numpy as np

# Configuração da porta serial
try:
    ser = serial.Serial('COM4', 115200, timeout=1)
except Exception as e:
    print(f"Erro ao abrir a porta serial: {e}")
    ser = None

# Configuração do Filtro de Kalman
class KalmanFilter:
    def __init__(self, process_variance=1e-5, measurement_variance=0.1):
        self.estimate = 0.0
        self.error_estimate = 1.0
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
    
    def update(self, measurement):
        self.error_estimate += self.process_variance
        kalman_gain = self.error_estimate / (self.error_estimate + self.measurement_variance)
        self.estimate += kalman_gain * (measurement - self.estimate)
        self.error_estimate *= (1 - kalman_gain)
        return self.estimate

# Criando filtros para cada eixo de cada MPU
num_mpus = 4
filters = [[KalmanFilter() for _ in range(3)] for _ in range(num_mpus)]

def read_serial():
    try:
        if ser and ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            values = data.split('/')
            if len(values) == num_mpus * 3:
                return [float(v) for v in values]
    except Exception as e:
        print(f"Erro na leitura da porta serial: {e}")
    return [0.0] * (num_mpus * 3)

def init_gl():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def draw_paper_plane():
    glBegin(GL_QUADS)
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
    gluLookAt(6, 4, 10, 0, 0, 0, 0, 1, 0)

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
    positions = [(-3, 0, 0), (-1, 0, 0), (1, 0, 0), (3, 0, 0)]
    
    while running:
        dt = clock.tick(60) / 1000.0
        raw_values = read_serial()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        filtered_values = []
        for i in range(num_mpus):
            yaw = filters[i][0].update(raw_values[i * 3])
            pitch = filters[i][1].update(raw_values[i * 3 + 1])
            roll = filters[i][2].update(raw_values[i * 3 + 2])
            filtered_values.append((yaw, pitch, roll))
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        update_camera()
        
        for i in range(num_mpus):
            draw_airplane_instance(*positions[i], *filtered_values[i])
        
        pygame.display.flip()
    
    pygame.quit()
    if ser:
        ser.close()

if __name__ == '__main__':
    main()
