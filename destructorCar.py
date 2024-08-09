import pygame
import sys
import random
from ajustes import Ajustes
from coche import Coche
from bala import bala
from enemigo import Enemigo
from enemigo2 import Enemigo2
from objeto_central import ObjetoCentral

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
                        self.dc_game.tiempo_inicio = pygame.time.get_ticks()  # Iniciar el temporizador
                    elif self.opciones[self.opcion_seleccionada] == "Salir":
                        sys.exit()

class PausaMenu:
    def __init__(self, dc_game):
        self.dc_game = dc_game
        self.screen = dc_game.screen
        self.ajustes = dc_game.ajustes
        self.font = pygame.font.SysFont(None, 48)
        self.opciones = ["Continuar", "Salir"]
        self.opcion_seleccionada = 0

    def mostrar_menu_pausa(self):
        self.screen.fill((0, 0, 0))
        for i, opcion in enumerate(self.opciones):
            color = (255, 0, 0) if i == self.opcion_seleccionada else (255, 255, 255)
            opcion_texto = self.font.render(opcion, True, color)
            self.screen.blit(opcion_texto, (self.ajustes.anchura / 2 - opcion_texto.get_width() / 2, 200 + i * 50))
        pygame.display.flip()
    
    def comprobar_eventos_pausa(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                elif event.key == pygame.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                elif event.key == pygame.K_RETURN:
                    if self.opciones[self.opcion_seleccionada] == "Continuar":
                        self.dc_game.en_pausa = False
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
        self.enemigos2 = pygame.sprite.Group()
        self.nivel = 1
        self.ajustes.puntuacion = 0  # Inicializar la puntuación
        self.tiempo_inicio = pygame.time.get_ticks()

        self.enviarEnemigos()

        # Inicializar el mezclador de sonido
        pygame.mixer.init()

        # Cargar sonidos
        self.sonido_motor = pygame.mixer.Sound('sonidos/stranger.mp3') 
        self.sonido_disparo = pygame.mixer.Sound('sonidos/Murillo.wav')

        # Reproducir sonido de motor en bucle
        self.sonido_motor.play(-1)  # -1 para bucle infinito

        self.en_juego = False
        self.en_pausa = False  # Estado de pausa
        self.menu = Menu(self)
        self.menu_pausa = PausaMenu(self)

        self.font = pygame.font.SysFont(None, 48)  # Fuente para el tiempo
        self.font_puntuacion = pygame.font.SysFont(None, 36)  # Fuente para la puntuación

        # Cargar y centrar la imagen
        self.centro_imagen = pygame.image.load('imagenes/castillo.png')  # Cambia esta ruta a la de tu imagen
        self.centro_rect = self.centro_imagen.get_rect()
        self.centro_rect.center = (self.ajustes.anchura // 2, self.ajustes.altura // 2)
        self.objeto_central = ObjetoCentral(self)
        self.objeto_central_group = pygame.sprite.Group()
        self.objeto_central_group.add(self.objeto_central)

        # Cargar las imágenes de transición
        self.imagen_transicion_nivel2 = pygame.image.load('imagenes/nivel 2.png')  # Cambia esta ruta a la de tu imagen
        self.rect_transicion_nivel2 = self.imagen_transicion_nivel2.get_rect()
        self.rect_transicion_nivel2.center = (self.ajustes.anchura // 2, self.ajustes.altura // 2)

        self.imagen_transicion_vida0 = pygame.image.load('imagenes/Game.png')  # Cambia esta ruta a la de tu imagen
        self.rect_transicion_vida0 = self.imagen_transicion_vida0.get_rect()
        self.rect_transicion_vida0.center = (self.ajustes.anchura // 2, self.ajustes.altura // 2)

        self.imagen_explosion = pygame.image.load('imagenes/laser.png').convert_alpha()
        self.rect_explosion = self.imagen_explosion.get_rect()
        self.explosiones = []  # Para guardar las explosiones activas

    def enviarEnemigos(self):
     cantidad_enemigos = random.randint(1, 4)  # Número aleatorio entre 1 y 4
     while len(self.enemigos) < cantidad_enemigos:
        cocheMalvado = Enemigo(self)
        self.enemigos.add(cocheMalvado)

    def enviarEnemigos2(self):
        while len(self.enemigos2) < 1:  # Asegurarse de tener al menos 2 enemigos2 en pantalla
            enemigo2 = Enemigo2(self)
            self.enemigos2.add(enemigo2)

    def eliminarEnemigosViejos(self):
        for enemigo in self.enemigos.copy():
            if enemigo.rect.right >= self.ajustes.anchura:
                self.enemigos.remove(enemigo)
        self.enviarEnemigos()  # Asegurarse de mantener la cantidad mínima

    def eliminarEnemigos2Viejos(self):
        for enemigo in self.enemigos2.copy():
            if enemigo.rect.top > self.ajustes.altura or enemigo.rect.bottom < 0:
                self.enemigos2.remove(enemigo)
        self.enviarEnemigos2()  # Asegurarse de mantener la cantidad mínima

    def actualizarEnemigos(self):
        self.enemigos.update()
        if self.nivel >= 2:
            self.enemigos2.update()

    def mostrar_transicion(self, imagen, rect):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000:  # 2 segundos
            self.screen.blit(imagen, rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
    
    def mostrar_imagen_transicion_y_cerrar(self):
        self.mostrar_transicion(self.imagen_transicion_vida0, self.rect_transicion_vida0)
        pygame.time.wait(1000)  # Esperar 2 segundos antes de salir
        pygame.quit()
        sys.exit()

    def mostrar_puntuacion(self):
        puntuacion_texto = self.font_puntuacion.render(f"Puntuación: {self.ajustes.puntuacion}", True, (255, 255, 255))
        self.screen.blit(puntuacion_texto, (10, 50))

    def actualizarPantalla(self):
       self.screen.blit(self.fondo, (0, 0))
       self.coche.blitme()
       for bala in self.balas.sprites():
         bala.pintarBala()
   
       self.enemigos.draw(self.screen)
       if self.nivel >= 2:
         self.enemigos2.draw(self.screen)

    # Mostrar explosiones
       for explosion in self.explosiones:
        self.screen.blit(self.imagen_explosion, explosion.topleft)  # Dibujar explosiones en la pantalla

    # Eliminar explosiones que han estado en pantalla por un tiempo
       self.explosiones = [explosion for explosion in self.explosiones if explosion.y > 0]

    # Mostrar la barra de vida del ObjetoCentral
       if self.objeto_central.vida > 0:
        self.objeto_central_group.draw(self.screen)
        self.objeto_central.blitme()  # Esto incluye la barra de vida
       else:
        self.mostrar_imagen_transicion_y_cerrar()

       self.mostrar_tiempo()  # Mostrar el tiempo en la pantalla
       self.mostrar_puntuacion()  # Mostrar la puntuación en la pantalla
       self.screen.blit(self.centro_imagen, self.centro_rect)  # Dibujar la imagen centrada
       pygame.display.flip()


    def dispararBala(self):
        nuevaBala = bala(self)
        self.balas.add(nuevaBala)

        # Reproducir sonido de disparo
        self.sonido_disparo.play()

    def eliminar_objeto_central(self):
        self.objeto_central_group.remove(self.objeto_central)
        self.objeto_central.kill()  # También elimina el sprite del grupo

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
                elif event.key == pygame.K_SPACE and self.nivel >= 2:  # Permitir disparar solo a partir del nivel 2
                 self.dispararBala()
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.en_pausa = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.coche.moviendoDerecha = False
                elif event.key == pygame.K_LEFT:
                    self.coche.moviendoIzquierda = False
                elif event.key == pygame.K_UP:
                    self.coche.moviendoArriba = False
                elif event.key == pygame.K_DOWN:
                    self.coche.moviendoAbajo = False

    def actualizar_puntuacion(self, puntos):
     self.ajustes.puntuacion += puntos
     if self.ajustes.puntuacion >= 100:
        self.recuperar_salud()
        self.ajustes.puntuacion = 0  # Reiniciar puntuación después de recuperación

    def recuperar_salud(self):
     recuperacion = 0.1 * self.objeto_central.vida_maxima  # 10% de la vida máxima
     self.objeto_central.vida = min(self.objeto_central.vida + recuperacion, self.objeto_central.vida_maxima)

    def comprobar_colisiones(self):
    # Colisiones entre balas y enemigos
     for bala in self.balas.copy():
        if bala.rect.bottom <= 0:
            self.balas.remove(bala)

     colisiones = pygame.sprite.groupcollide(self.balas, self.enemigos, True, True)
     if colisiones:
        for enemigos in colisiones.values():
            self.actualizar_puntuacion(len(enemigos) * 10)  # Añadir puntos por cada enemigo destruido
        self.enviarEnemigos()
     if colisiones:
        self.enviarEnemigos()  # Asegurarse de mantener la cantidad mínima

    # Colisiones entre el coche y los enemigos
     enemigos_colisionados = pygame.sprite.spritecollide(self.coche, self.enemigos, False)
     if enemigos_colisionados:
        primer_enemigo = enemigos_colisionados[0]  # Tomar solo el primer enemigo
        primer_enemigo.kill()  # Eliminar solo ese enemigo
        self.coche.destruir()  # Destruir el coche
        self.enemigos.remove(primer_enemigo)  # Asegurarse de eliminarlo del grupo de enemigos
        self.enviarEnemigos()  # Enviar nuevos enemigos si es necesario

    def comprobar_colisiones2(self):
        for bala in self.balas.copy():
            if bala.rect.bottom <= 0:
                self.balas.remove(bala)

        colisiones = pygame.sprite.groupcollide(self.balas, self.enemigos2, True, True)
        if colisiones:
            for enemigos2 in colisiones.values():
                self.actualizar_puntuacion(len(enemigos2) * 20)  # Añadir puntos por cada enemigo2 destruido
            self.enviarEnemigos2()
        if colisiones:
            self.enviarEnemigos2()  # Asegurarse de mantener la cantidad mínima

        if pygame.sprite.spritecollideany(self.coche, self.enemigos2):
            self.coche.destruir()

    def mostrar_tiempo(self):
        tiempo_actual = pygame.time.get_ticks() - self.tiempo_inicio
        tiempo_mostrado = max(0, tiempo_actual // 1000)  # Convertir a segundos
        tiempo_texto = self.font.render(f"Tiempo: {tiempo_mostrado}", True, (255, 255, 255))
        self.screen.blit(tiempo_texto, (10, 10))

    def fin_del_juego(self):
      self.screen.fill((0, 0, 0))  # Limpiar pantalla
      mensaje_victoria = self.font.render("¡Has ganado el juego!", True, (0, 255, 0))
      self.screen.blit(mensaje_victoria, (self.ajustes.anchura / 2 - mensaje_victoria.get_width() / 2, self.ajustes.altura / 2 - mensaje_victoria.get_height() / 2))
      pygame.display.flip()
      pygame.time.wait(2000)  # Esperar 3 segundos para mostrar el mensaje
      pygame.quit()
      sys.exit()

    def comprobar_nivel(self):
        tiempo_actual = pygame.time.get_ticks() - self.tiempo_inicio
        if tiempo_actual >= 100000:  # 100 segundos
         self.fin_del_juego()  # Finalizar el juego si se ha alcanzado el tiempo límite
        if tiempo_actual >= 50000 and self.nivel == 1:  # 10 segundos y en nivel 1
            self.nivel = 2
            self.enemigos.empty()  # Vaciar enemigos antiguos
            self.enemigos2.empty()  # Vaciar enemigos2 antiguos
            
            self.coche.rect.center = (self.ajustes.anchura // 2, self.ajustes.altura - self.coche.rect.height // 2)
            self.coche.x = float(self.coche.rect.x)
            self.coche.y = float(self.coche.rect.y)
            self.coche.moviendoDerecha = False
            self.coche.moviendoIzquierda = False
            self.coche.moviendoArriba = False
            self.coche.moviendoAbajo = False
            self.coche.tiempo_movimiento = {key: 0 for key in self.coche.tiempo_movimiento}
            self.coche.rect.center = (self.ajustes.anchura // 2, self.ajustes.altura - self.coche.rect.height // 2)  # Reiniciar posición del coche
            
            if tiempo_actual >= 55000 and self.nivel == 2:  # 75 segundos y en nivel 2
               self.objeto_central.vida = min(self.objeto_central.vida + self.objeto_central.vida_maxima * 0.5, self.objeto_central.vida_maxima)
            self.mostrar_transicion(self.imagen_transicion_nivel2, self.rect_transicion_nivel2)
            pygame.time.wait(2000)  # Esperar 2 segundos antes de continuar
            self.enviarEnemigos()  # Asegurarse de enviar enemigos del nivel 1
            self.enviarEnemigos2()  # Asegurarse de enviar enemigos del nivel 2
            

    def run(self):
        while True:
            if self.en_juego:
                if self.en_pausa:
                    self.menu_pausa.mostrar_menu_pausa()
                    self.menu_pausa.comprobar_eventos_pausa()
                else:
                    self.comprobarEventos()
                    self.coche.actualizar()
                    self.balas.update()
                    self.eliminarEnemigosViejos()
                    self.eliminarEnemigos2Viejos()
                    self.actualizarEnemigos()
                    self.actualizarPantalla()
                    self.comprobar_colisiones()
                    self.comprobar_colisiones2()
                    self.comprobar_nivel()
            else:
                self.menu.mostrar_menu()
                self.menu.comprobar_eventos()

if __name__ == "__main__":
    juego = DestructorCar()
    juego.run()

