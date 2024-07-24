import pygame

class Coche:
    def __init__ (self, dc_game):
        self.screen = dc_game.screen
        self.screem_rect = dc_game.screem.get_rect()

        self.imagen = pygame.image.load('')
        self.rect = self.imagen.get_rect()
        self.rect.midbottom = self.screem_rect.midbottom

        self.moviendoIzquierda = False
        self.moviendoDerecha = False
        self.moviendoArriba = False
        self.moviendoAbajo = False



    def blime (self):
        self.screem.blime(self.imagen, self.rect)

    def actualizar (self):
        if self.moviendoIzquierda:
            self.rect.x -= 2
        if self.moviendoDerecha:
            self.rect.x += 2
        if self.moviendoArriba:
            self.rect.y -= 2
        if self.moviendoAbajo:
            self.rect.y += 2