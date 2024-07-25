import pygame
import sys
from ajustes import Ajustes
from coche import Coche
from bala import bala
from enemigo import Enemigo

class DestructorCar:
    def __init__(self):
        pygame.init()
        self.ajustes = Ajustes()
        self.screen = pygame.display.set_mode((self.ajustes.anchura, self.ajustes.altura))
        self.fondo = pygame.image.load(self.ajustes.fondo)
        pygame.display.set_caption("Coche Destructor")
        self.coche = Coche(self)
        self.balas = pygame.sprite.Group() 
        self.enemigos = pygame.sprite.Group()
        self.enviarEnemigos()
    
    def enviarEnemigos(self):
        cocheMalvado=Enemigo(self)
        self.enemigos.add(cocheMalvado)  
    
    def eliminarEnemigosViejos(self):
        for enemigo in self.enemigos.copy():
            if enemigo.rect.bottom >= self.ajustes.altura:
                self.enemigos.remove(enemigo)
                self.enviarEnemigos ()

    def actualizarEnemigos(self):
        self.enemigos.update()
       
    def actualizarPantalla(self):
        self.screen.blit(self.fondo, (0, 0))
        self.coche.blitme()
        for bala in self.balas.sprites():
            bala.pintarBala() 
        self.enemigos.drawn(self.screem)
        pygame.display.flip()

    def dispararBala(self):
        nuevaBala = bala(self)
        self.balas.add(nuevaBala)  # Corregido: debería ser 'self.balas', no 'self.bala'   

    def comprobarEventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.coche.moviendoDerecha = True
                elif event.key == pygame.K_LEFT:
                    self.coche.moviendoIzquierda = True
                elif event.key == pygame.K_UP:
                    self.coche.moviendoArriba = True
                elif event.key == pygame.K_DOWN:
                    self.coche.moviendoAbajo = True
                elif event.key == pygame.K_SPACE:
                    self.dispararBala()    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.coche.moviendoDerecha = False
                elif event.key == pygame.K_LEFT:
                    self.coche.moviendoIzquierda = False
                elif event.key == pygame.K_UP:
                    self.coche.moviendoArriba = False
                elif event.key == pygame.K_DOWN:
                    self.coche.moviendoAbajo = False

    def run_game(self):
        while True:
            self.comprobarEventos()
            self.coche.actualizar()
            self.balas.update() 
            self.actualizarEnemigos()  
            self.eliminarEnemigosViejos()
            self.actualizarPantalla()

if __name__ == "__main__":
    dc = DestructorCar()
    dc.run_game()
