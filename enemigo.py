import pygame
from pygame.sprite import Sprite
import random
import os

class Enemigo(Sprite):
    def __init__(self, dc_game):
        super().__init__()
        self.screen = dc_game.screen
        self.ajustes = dc_game.ajustes
        self.game = dc_game  # Guardar la referencia al juego principal

        # Cargar los fotogramas del GIF
        self.frames = self.load_frames('../echos/frames')  
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Determinar si el enemigo aparece desde la izquierda o la derecha
        if random.choice([True, False]):
            self.rect.x = -self.rect.width  # Aparece desde la izquierda
            self.direccion = 1  # Mueve hacia la derecha
        else:
            self.rect.x = self.ajustes.anchura  # Aparece desde la derecha
            self.direccion = -1  # Mueve hacia la izquierda

        self.rect.y = random.randint(10, dc_game.ajustes.altura - self.rect.height)
        
        self.frame_delay = 100  # Milisegundos entre fotogramas
        self.last_update = pygame.time.get_ticks()
        
        # Velocidad aleatoria ajustable
        self.velocidad = random.uniform(0.5, 1)  # Cambia el rango de valores según tus necesidades

    def load_frames(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                frames.append(frame)
        return frames

    def update(self):
        # Actualizar la posición del enemigo para movimiento horizontal
        self.rect.x += self.velocidad * self.direccion

        # Animar el enemigo
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Mover hacia el objeto central
        objeto_central = self.game.objeto_central.rect
        if self.rect.centerx < objeto_central.centerx:
            self.rect.x += self.velocidad
        elif self.rect.centerx > objeto_central.centerx:
            self.rect.x -= self.velocidad
        if self.rect.centery < objeto_central.centery:
            self.rect.y += self.velocidad
        elif self.rect.centery > objeto_central.centery:
            self.rect.y -= self.velocidad

        # Comprueba si el enemigo ha llegado al objeto central
        if self.rect.colliderect(objeto_central):
            self.game.objeto_central.recibir_dano(1)  # Aplica 2 puntos de daño
            self.kill()  # Elimina el enemigo si colisiona con el objeto central