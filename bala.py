import pygame
from pygame.sprite import Sprite

class bala(Sprite):
    def __init__(self, dc_game):  # Cambiado de _init_ a __init__
        super().__init__()  # Cambiado de _init_ a __init__
        self.screen = dc_game.screen  # Asignar dc_game.screen, no dc_game
        self.ajustes = dc_game.ajustes
        self.color = self.ajustes.colorBala
        self.rect = pygame.Rect(0, 0, self.ajustes.anchuraBala, self.ajustes.alturaBala)
        self.rect.midtop = dc_game.coche.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.ajustes.velocidadBala
        self.rect.y = self.y

    def pintarBala(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
  