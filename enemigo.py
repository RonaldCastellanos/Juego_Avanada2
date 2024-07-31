import pygame
from pygame.sprite import Sprite
import random
import os

class Enemigo(Sprite):
    def __init__(self, dc_game):
        super().__init__()
        self.screen = dc_game.screen
        self.ajustes = dc_game.ajustes

        # Cargar los fotogramas del GIF
        self.frames = self.load_frames('C:/Users/amaya/OneDrive/Desktop/echos/frames')  # Ruta correcta
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Posicionar al enemigo horizontalmente al azar
        self.rect.x = self.rect.width - 50
        self.rect.y = random.randint(10, dc_game.ajustes.altura - self.rect.height)
        
        self.frame_delay = 100  # Milisegundos entre fotogramas
        self.last_update = pygame.time.get_ticks()

    def load_frames(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                frame = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                frames.append(frame)
        return frames

    def update(self):
        # Actualizar la posición del enemigo para movimiento horizontal
        self.rect.x += self.ajustes.velocidadEnemigo

        # Animar el enemigo
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
