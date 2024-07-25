import pygame

class Coche:
    def __init__(self, dc_game):
        self.screen = dc_game.screen
        self.screen_rect = dc_game.screen.get_rect()

        self.imagen = pygame.image.load('imagenes/coche.png')
        self.rect = self.imagen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.moviendoIzquierda = False
        self.moviendoDerecha = False
        self.moviendoArriba = False
        self.moviendoAbajo = False

    def blitme(self):
        self.screen.blit(self.imagen, self.rect)

    def actualizar(self):
        if self.moviendoIzquierda and self.rect.left > 0:
            self.rect.x -= 2
        if self.moviendoDerecha and self.rect.right < self.screen_rect.right:
            self.rect.x += 2
        if self.moviendoArriba and self.rect.top > 0:
            self.rect.y -= 2
        if self.moviendoAbajo and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 2
