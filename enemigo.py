import pygame
from pygame.sprite import Sprite
import random

class Enemigo(Sprite):

    def __init__(self,dc_game) :
        super().__init__()
        self.screem = dc_game.screen

        self.imagen = pygame.image.load('')
        self.rect = self.imagen.get_rect()

        self.rect.y =self.rect.height-50
        self.rect.x= random.randint(10,self.rect.width)*10
        self.ajustes = dc_game.ajustes

    def update (self):
        self.rect.y += self.ajustes.velocidadEnemigo