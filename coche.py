import pygame
import time

class Coche:
    def __init__(self, dc_game):
        self.screen = dc_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ajustes = dc_game.ajustes

        self.image = pygame.image.load('imagenes/cocheR2.png')
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.angulo = 0

        self.moviendoDerecha = False
        self.moviendoIzquierda = False
        self.moviendoArriba = False
        self.moviendoAbajo = False

        # Tiempo de presionamiento para cada tecla de dirección
        self.tiempo_movimiento = {
            "derecha": 0,
            "izquierda": 0,
            "arriba": 0,
            "abajo": 0
        }

        self.velocidad_inicial = 0.05  # Velocidad inicial muy baja
        self.velocidad_maxima = 3   # Velocidad máxima alta
        self.aceleracion = (self.velocidad_maxima - self.velocidad_inicial) / 0.4  # Aceleración rápida

        # Atributos para el control de balas
        self.max_balas = 10
        self.balas_disponibles = self.max_balas
        self.tiempo_recarga = 1.5  # Tiempo de recarga en segundos
        self.ultimo_lanzamiento = time.time()

    def actualizar(self):
        ahora = time.time()

        if self.moviendoDerecha:
            self.tiempo_movimiento["derecha"] += 0.01  # Incrementar más lentamente
            velocidad = self.velocidad_inicial + min(self.tiempo_movimiento["derecha"] * self.aceleracion, self.velocidad_maxima)
            self.x += velocidad
            self.angulo = -90
        else:
            self.tiempo_movimiento["derecha"] = 0

        if self.moviendoIzquierda:
            self.tiempo_movimiento["izquierda"] += 0.01  # Incrementar más lentamente
            velocidad = self.velocidad_inicial + min(self.tiempo_movimiento["izquierda"] * self.aceleracion, self.velocidad_maxima)
            self.x -= velocidad
            self.angulo = 90
        else:
            self.tiempo_movimiento["izquierda"] = 0

        if self.moviendoArriba:
            self.tiempo_movimiento["arriba"] += 0.01  # Incrementar más lentamente
            velocidad = self.velocidad_inicial + min(self.tiempo_movimiento["arriba"] * self.aceleracion, self.velocidad_maxima)
            self.y -= velocidad
            self.angulo = 0
        else:
            self.tiempo_movimiento["arriba"] = 0

        if self.moviendoAbajo:
            self.tiempo_movimiento["abajo"] += 0.01  # Incrementar más lentamente
            velocidad = self.velocidad_inicial + min(self.tiempo_movimiento["abajo"] * self.aceleracion, self.velocidad_maxima)
            self.y += velocidad
            self.angulo = 180
        else:
            self.tiempo_movimiento["abajo"] = 0

        self.rect.x = self.x
        self.rect.y = self.y

        # Rotar la imagen del coche según el ángulo
        self.image = pygame.transform.rotate(self.original_image, self.angulo)

        # Gestionar el recarga de balas
        if self.balas_disponibles < self.max_balas and (ahora - self.ultimo_lanzamiento) >= self.tiempo_recarga:
            self.balas_disponibles = self.max_balas
            self.ultimo_lanzamiento = ahora

    def rotar(self, direccion):
        if direccion == 'derecha':
            self.angulo = -90
        elif direccion == 'izquierda':
            self.angulo = 90
        elif direccion == 'arriba':
            self.angulo = 0
        elif direccion == 'abajo':
            self.angulo = 180
        self.image = pygame.transform.rotate(self.original_image, self.angulo)

    def reiniciar_posicion(self):
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.angulo = 0  # Opcional: restablecer el ángulo
        self.image = pygame.transform.rotate(self.original_image, self.angulo)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def destruir(self):
        # Eliminar el coche, no se muestra mensaje
        self.rect.x = -self.rect.width

    def lanzar_bala(self):
        ahora = time.time()
        if self.balas_disponibles > 0:
            # Lógica para lanzar la bala
            self.balas_disponibles -= 1
            # Aquí iría la creación y envío de la bala

        if self.balas_disponibles == 0:
            self.ultimo_lanzamiento = ahora

