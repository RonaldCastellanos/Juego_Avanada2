import pygame
import sys
from ajustes import Ajustes
from coche import Coche
from bala import bala
from enemigo import Enemigo

class Menu:
    def __init__(self, dc_game):
        self.dc_game = dc_game
        self.screen = dc_game.screen
        self.ajustes = dc_game.ajustes
        self.font = pygame.font.SysFont(None, 48)
        self.opciones = ["Iniciar Juego", "Salir"]
        self.opcion_seleccionada = 0

    def mostrar_menu(self):
        self.screen.fill((0, 0, 0))
        for i, opcion in enumerate(self.opciones):
            color = (255, 0, 0) if i == self.opcion_seleccionada else (255, 255, 255)
            opcion_texto = self.font.render(opcion, True, color)
            self.screen.blit(opcion_texto, (self.ajustes.anchura / 2 - opcion_texto.get_width() / 2, 200 + i * 50))
        pygame.display.flip()

    def comprobar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                elif event.key == pygame.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                elif event.key == pygame.K_RETURN:
                    if self.opciones[self.opcion_seleccionada] == "Iniciar Juego":
                        self.dc_game.en_juego = True
                    elif self.opciones[self.opcion_seleccionada] == "Salir":
                        sys.exit()

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
        self.puntuacionJugador = 0
        self.salud = self.ajustes.vidasJugador
        self.enemigosHuir = self.ajustes.enemigoQuePuedehuir


        # Inicializar el mezclador de sonido
        pygame.mixer.init()

        # Cargar sonidos
        self.sonido_motor = pygame.mixer.Sound('sonidos/stranger.mp3') 
        self.sonido_disparo = pygame.mixer.Sound('sonidos/Murillo.wav')

        # Reproducir sonido de motor en bucle
        self.sonido_motor.play(-1)  # -1 para bucle infinito

        self.en_juego = False
        self.menu = Menu(self)

    def enviarEnemigos(self):
        cocheMalvado = Enemigo(self)
        self.enemigos.add(cocheMalvado)

    def eliminarEnemigosViejos(self):
        for enemigo in self.enemigos.copy():
            if enemigo.rect.right >= self.ajustes.anchura:
                self.enemigos.remove(enemigo)
                self.enviarEnemigos()

    def actualizarEnemigos(self):
        self.enemigos.update()
       
    def actualizarPantalla(self):
        self.screen.blit(self.fondo, (0, 0))
        self.coche.blitme()
        for bala in self.balas.sprites():
            bala.pintarBala()
        self.enemigos.draw(self.screen)
        pygame.display.flip()

    def dispararBala(self):
        nuevaBala = bala(self)
        self.balas.add(nuevaBala)

        # Reproducir sonido de disparo
        self.sonido_disparo.play()

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
            if self.en_juego:
                self.comprobarEventos()
                self.coche.actualizar()
                self.balas.update()
                self.actualizarEnemigos()
                self.eliminarEnemigosViejos()
                self.actualizarPantalla()
            else:
                self.menu.mostrar_menu()
                self.menu.comprobar_eventos()

if __name__ == "__main__":
    dc = DestructorCar()
    dc.run_game()
