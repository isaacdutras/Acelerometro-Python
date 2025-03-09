# import pygame
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
# import math

# # Variáveis de controle do avião (as mesmas para todos os aviões)
# pitch = 0.0  # rotação em torno do eixo X
# roll = 0.0   # rotação em torno do eixo Z

# # Parâmetros da câmera (coordenadas esféricas)
# cam_angle_x = 45.0  # ângulo horizontal (yaw)
# cam_angle_y = 20.0  # ângulo vertical (pitch)
# cam_distance = 20.0

# # Sensibilidade do mouse para movimentação da câmera
# mouse_sensitivity = 0.2

# def init_gl():
#     glClearColor(0.5, 0.7, 1.0, 1.0)  # cor de fundo (sem chão)
#     glEnable(GL_DEPTH_TEST)

# def draw_airplane():
#     """
#     Desenha um avião utilizando um cubo escalado para ter aspecto alongado.
#     """
#     glBegin(GL_QUADS)
#     # Frente
#     glColor3f(0.0, 0.0, 1.0)
#     glVertex3f( 0.5,  0.1, -1.0)
#     glVertex3f(-0.5,  0.1, -1.0)
#     glVertex3f(-0.5, -0.1, -1.0)
#     glVertex3f( 0.5, -0.1, -1.0)
#     # Traseira
#     glColor3f(0.0, 1.0, 0.0)
#     glVertex3f( 0.5,  0.1, 1.0)
#     glVertex3f(-0.5,  0.1, 1.0)
#     glVertex3f(-0.5, -0.1, 1.0)
#     glVertex3f( 0.5, -0.1, 1.0)
#     # Esquerda
#     glColor3f(1.0, 0.0, 0.0)
#     glVertex3f(-0.5,  0.1, -1.0)
#     glVertex3f(-0.5,  0.1, 1.0)
#     glVertex3f(-0.5, -0.1, 1.0)
#     glVertex3f(-0.5, -0.1, -1.0)
#     # Direita
#     glColor3f(1.0, 1.0, 0.0)
#     glVertex3f(0.5,  0.1, -1.0)
#     glVertex3f(0.5,  0.1, 1.0)
#     glVertex3f(0.5, -0.1, 1.0)
#     glVertex3f(0.5, -0.1, -1.0)
#     # Topo
#     glColor3f(1.0, 0.0, 1.0)
#     glVertex3f( 0.5,  0.1, -1.0)
#     glVertex3f(-0.5,  0.1, -1.0)
#     glVertex3f(-0.5,  0.1, 1.0)
#     glVertex3f( 0.5,  0.1, 1.0)
#     # Base
#     glColor3f(0.0, 1.0, 1.0)
#     glVertex3f( 0.5, -0.1, -1.0)
#     glVertex3f(-0.5, -0.1, -1.0)
#     glVertex3f(-0.5, -0.1, 1.0)
#     glVertex3f( 0.5, -0.1, 1.0)
#     glEnd()

# def draw_airplane_instance(x, y, z):
#     """
#     Desenha uma instância do avião traduzida para a posição (x, y, z)
#     e aplicando as rotações globais de pitch e roll.
#     """
#     glPushMatrix()
#     glTranslatef(x, y, z)
#     glRotatef(pitch, 1, 0, 0)  # aplica o pitch
#     glRotatef(roll, 0, 0, 1)   # aplica o roll
#     draw_airplane()
#     glPopMatrix()

# def update_camera():
#     """
#     Atualiza a posição da câmera com base em coordenadas esféricas.
#     A câmera está sempre olhando para a origem.
#     """
#     global cam_angle_x, cam_angle_y, cam_distance
#     rad_x = math.radians(cam_angle_x)
#     rad_y = math.radians(cam_angle_y)
#     cam_x = cam_distance * math.cos(rad_y) * math.sin(rad_x)
#     cam_y = cam_distance * math.sin(rad_y)
#     cam_z = cam_distance * math.cos(rad_y) * math.cos(rad_x)
#     glLoadIdentity()
#     gluLookAt(cam_x, cam_y, cam_z,  0, 0, 0,  0, 1, 0)

# def main():
#     global pitch, roll, cam_angle_x, cam_angle_y
#     pygame.init()
#     display = (800, 600)
#     pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
#     pygame.display.set_caption("8 Aviões em 3D com Controle de Câmera")
    
#     init_gl()
    
#     # Configura a projeção em perspectiva
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
#     glMatrixMode(GL_MODELVIEW)
    
#     clock = pygame.time.Clock()
#     running = True
#     left_button_down = False  # para controlar o movimento da câmera com o botão esquerdo
    
#     # Define as posições dos 8 aviões (dispostos em uma grade 2x4)
#     # Por exemplo, distribuídos em duas linhas (y) e quatro colunas (x)
#     airplane_positions = []
#     x_positions = [-6, -2, 2, 6]
#     y_positions = [2, -2]
#     for y in y_positions:
#         for x in x_positions:
#             airplane_positions.append((x, y, 0))
    
#     while running:
#         dt = clock.tick(60) / 1000.0  # tempo decorrido em segundos
        
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 running = False
#             # Clica o botão esquerdo para mover a câmera
#             elif event.type == MOUSEBUTTONDOWN:
#                 if event.button == 1:  # botão esquerdo
#                     left_button_down = True
#             elif event.type == MOUSEBUTTONUP:
#                 if event.button == 1:
#                     left_button_down = False
#             elif event.type == MOUSEMOTION and left_button_down:
#                 dx, dy = event.rel
#                 cam_angle_x += dx * mouse_sensitivity
#                 cam_angle_y += dy * mouse_sensitivity
#                 # Limita o ângulo vertical para evitar inversão total da câmera
#                 cam_angle_y = max(-89, min(89, cam_angle_y))
        
#         # Controle dos aviões pelas setas do teclado
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_UP]:
#             pitch += 90 * dt   # aumenta o pitch (rotaciona para baixo)
#         if keys[pygame.K_DOWN]:
#             pitch -= 90 * dt   # diminui o pitch (rotaciona para cima)
#         if keys[pygame.K_LEFT]:
#             roll += 90 * dt    # aumenta o roll (rotação para a esquerda)
#         if keys[pygame.K_RIGHT]:
#             roll -= 90 * dt    # diminui o roll (rotação para a direita)
        
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         update_camera()
        
#         # Desenha cada avião na posição definida
#         for pos in airplane_positions:
#             draw_airplane_instance(*pos)
        
#         pygame.display.flip()
    
#     pygame.quit()

# if __name__ == '__main__':
#     main()
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import serial
import threading

yaw, pitch, roll = 0.0, 0.0, 0.0
mouse_x, mouse_y = 0, 0
camera_yaw, camera_pitch = 0.0, 0.0
serial_port = "/dev/ttyACM0"  # Altere para a porta correta
baud_rate = 115200

def read_serial():
    global yaw, pitch, roll
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        while True:
            data = ser.readline().decode("utf-8").strip()
            if data:
                try:
                    y, p, r = map(float, data.split("/"))
                    yaw, pitch, roll = y, p, r
                except ValueError:
                    pass
    except serial.SerialException:
        print("Erro ao acessar a porta serial")

def draw_airplane():
    glPushMatrix()
    glRotatef(yaw, 0, 1, 0)  # Yaw (eixo Y)
    glRotatef(pitch, 1, 0, 0)  # Pitch (eixo X)
    glRotatef(roll, 0, 0, 1)  # Roll (eixo Z)
    
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)
    glVertex3f(-1, 0, -2)
    glVertex3f(1, 0, -2)
    glVertex3f(1, 0, 2)
    glVertex3f(-1, 0, 2)
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    glVertex3f(-1, 0, -2)
    glVertex3f(1, 0, -2)
    glVertex3f(0, 1, -3)
    glEnd()
    
    glPopMatrix()

def main():
    global mouse_x, mouse_y, camera_yaw, camera_pitch
    
    threading.Thread(target=read_serial, daemon=True).start()
    
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                dx, dy = event.rel
                camera_yaw += dx * 0.2
                camera_pitch += dy * 0.2
        
        glLoadIdentity()
        glRotatef(camera_pitch, 1, 0, 0)
        glRotatef(camera_yaw, 0, 1, 0)
        glTranslatef(0, 0, -10)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_airplane()
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
