import pygame 
import sys
from ajustes import Ajustes
from coche import Coche

class destructorCar :
    def __init__(self):
        pygame.init()
        self.Ajustes()
        self.screen = pygame.display.set_mode((self.ajustes.anchura, self.ajustes.altura))
        self.fondo = pygame.image.load(self.ajustes.fondo)
        pygame.display.set_caption("Coche Destructor")
        self.coche = Coche(self)


        def actualizarPantalla(self):
            self.screen.blit(self.fondo, (0, 0))
            self.coche.blime()
            pygame.display.flip()



        def comprobarEventos(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                   
                   if event.key == pygame.K_RIGHT:
                        self.coche.moviendoDerecha = True
                        self.coche.rect.x  += 2 

                elif event.key == pygame.K_LEFT:
                        self.coche.moviendoIzquierda = True
                        self.coche.rect.x  -= 2

                elif event.key == pygame.K_UP:
                        self.coche.moviendoArriba = True
                        self.coche.rect.y  -= 2

                elif event.key == pygame.K_DOWN:
                        self.coche.moviendoAbajo = True
                        self.coche.rect.y  += 2
        
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
              self.comprobarEventos(self)
              self.coche.actualizar()
              self.actualizarPantalla()
                

    if __name__ == "__main__":
        dc = destructorCar()
        dc.run_game()
        