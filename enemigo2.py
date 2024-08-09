import pygame
import random
from pygame.sprite import Sprite

class Enemigo2(Sprite):
    def __init__(self, dc_game):
        super().__init__()
        self.screen = dc_game.screen
        self.ajustes = dc_game.ajustes
        self.image = pygame.image.load('imagenes/tanque.png')
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.game = dc_game
        self.rect.x = random.randint(0, self.game.ajustes.anchura - self.rect.width)

        if random.choice([True, False]):
            self.rect.y = random.randint(-100, -40)
            self.direccion = 1
            self.image = pygame.transform.flip(self.original_image, False, True)
        else:
            self.rect.y = random.randint(self.game.ajustes.altura, self.game.ajustes.altura + 40)
            self.direccion = -1

        self.y = float(self.rect.y)
        self.velocidad = random.uniform(0.5, 1)

        # Cargar la imagen de efecto
        self.efecto_image = pygame.image.load('imagenes/laser.png')  # Cambia esta ruta a la de tu imagen de efecto
        self.efecto_rect = self.efecto_image.get_rect()
        self.mostrar_efecto = False
        self.efecto_tiempo = 0
        self.efecto_duracion = 500  # Duración del efecto en milisegundos

    def update(self):
        self.y += self.velocidad * self.direccion
        self.rect.y = self.y

        objeto_central = self.game.objeto_central.rect
        if self.rect.centerx < objeto_central.centerx:
            self.rect.x += 1
        elif self.rect.centerx > objeto_central.centerx:
            self.rect.x -= 1
        if self.rect.centery < objeto_central.centery:
            self.rect.y += 1
        elif self.rect.centery > objeto_central.centery:
            self.rect.y -= 1

        if self.rect.colliderect(objeto_central):
            if not self.mostrar_efecto:
                self.mostrar_efecto = True
                self.efecto_tiempo = pygame.time.get_ticks()
                self.game.objeto_central.recibir_dano(5)

        # Manejar el tiempo del efecto
        if self.mostrar_efecto:
            if pygame.time.get_ticks() - self.efecto_tiempo > self.efecto_duracion:  # Verificar si ha pasado el tiempo
                self.kill()  # Destruir el enemigo después de mostrar el efecto
            else:
                self.draw_efecto()  # Dibujar el efecto

    def draw_efecto(self):
        # Calcular la posición del efecto y dibujarlo en la pantalla
        self.efecto_rect.center = self.rect.center
        self.screen.blit(self.efecto_image, self.efecto_rect)

