import pygame

class ObjetoCentral(pygame.sprite.Sprite):
    def __init__(self, dc_game):
        super().__init__()
        self.screen = dc_game.screen
        self.settings = dc_game.ajustes
        self.image = pygame.image.load('imagenes/castillo.png')
        self.rect = self.image.get_rect()
        self.rect.center = (self.settings.anchura // 2, self.settings.altura // 2)
        self.vida = 100
        self.vida_maxima = 100
        self.game = dc_game  # Referencia al juego principal

    def update(self):
        pass

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        self.dibujar_barra_vida()

    def dibujar_barra_vida(self):
        ancho_barra = 200
        alto_barra = 20
        verde = (0, 255, 0)
        rojo = (255, 0, 0)

        barra_vida = pygame.Surface((ancho_barra, alto_barra))
        barra_vida.fill(rojo)

        vida_restante = max(0, self.vida)
        ancho_vida = int(ancho_barra * vida_restante / self.vida_maxima)

        barra_vida_restante = pygame.Surface((ancho_vida, alto_barra))
        barra_vida_restante.fill(verde)
        
        self.screen.blit(barra_vida, (self.rect.left, self.rect.top - 30))
        self.screen.blit(barra_vida_restante, (self.rect.left, self.rect.top - 30))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.rect.left, self.rect.top - 30, ancho_barra, alto_barra), 2)

    def recibir_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.destruir()

    def destruir(self):
        self.game.mostrar_imagen_transicion_y_cerrar()  # Llama a la función en el juego principal
        self.kill()  # Elimina el sprite del grupo
