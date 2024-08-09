import pygame
from pygame.sprite import Sprite

class BalaEnemigo(Sprite):
    def __init__(self, dc_game, x, y):
        super().__init__()
        self.screen = dc_game.screen
        self.image = pygame.image.load('imagenes/laser.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.y = float(self.rect.y)
        self.velocidad = 5

    def update(self):
        self.y += self.velocidad
        self.rect.y = self.y
        # Eliminar la bala si sale de la pantalla
        if self.rect.top >= self.screen.get_height():
            self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)