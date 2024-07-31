import pygame
from pygame.sprite import Sprite
import math

class bala(Sprite):
    def __init__(self, dc_game):  # Cambiado de _init_ a __init__
        super().__init__()  # Cambiado de _init_ a __init__
        self.screen = dc_game.screen  
        self.ajustes = dc_game.ajustes
        self.color = self.ajustes.colorBala
        
        # Determinar la posición inicial de la bala según la rotación del coche
        self.rect = pygame.Rect(0, 0, self.ajustes.anchuraBala, self.ajustes.alturaBala)
        self.angle = dc_game.coche.angulo
        
        if self.angle == 0:  # Hacia arriba
            self.rect.midtop = dc_game.coche.rect.midtop
        elif self.angle == 180:  # Hacia abajo
            self.rect.midbottom = dc_game.coche.rect.midbottom
        elif self.angle == -90:  # Hacia la derecha
            self.rect.midright = dc_game.coche.rect.midright
        elif self.angle == 90:  # Hacia la izquierda
            self.rect.midleft = dc_game.coche.rect.midleft

        # Coordenadas flotantes para movimiento preciso
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        # Mover la bala en la dirección según el ángulo del coche
        if self.angle == 0:  # Hacia arriba
            self.y -= self.ajustes.velocidadBala
        elif self.angle == 180:  # Hacia abajo
            self.y += self.ajustes.velocidadBala
        elif self.angle == -90:  # Hacia la derecha
            self.x += self.ajustes.velocidadBala
        elif self.angle == 90:  # Hacia la izquierda
            self.x -= self.ajustes.velocidadBala
        
        self.rect.x = self.x
        self.rect.y = self.y

    def pintarBala(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

  