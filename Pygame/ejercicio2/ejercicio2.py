import pygame
import random

# ---------------------------
# Configuración
# ---------------------------
ANCHO, ALTO = 1300, 800
FPS = 60

TAM_JUGADOR = 40
VEL_JUGADOR = 5

RAD_OBJETO = 10


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1300, 800))
    pygame.display.set_caption("África Galindo")
    
    fondo = pygame.image.load("fondo.jpg").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 36)



    # Jugador como rectángulo
    alonso = pygame.image.load("nano1.png").convert_alpha()
    alonso = pygame.transform.scale(
        alonso, (alonso.get_width()  // 9, alonso.get_height() // 9))
    rect_alonso = alonso.get_rect(center=(600, 200))

    


    podio = pygame.image.load("33.png").convert_alpha()
    podio = pygame.transform.scale(
        podio, (podio.get_width()  // 7, podio.get_height() // 7))
    rect_podio = podio.get_rect(center=(800, 700))


    puntuacion = 0
    corriendo = True

    while corriendo:
        # 1) Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # 2) Input continuo (teclas pulsadas)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            rect_alonso.x -= VEL_JUGADOR
        if teclas[pygame.K_d]:
            rect_alonso.x += VEL_JUGADOR
        if teclas[pygame.K_w]:
            rect_alonso.y -= VEL_JUGADOR
        if teclas[pygame.K_s]:
            rect_alonso.y += VEL_JUGADOR

        if teclas[pygame.K_LEFT]:
            rect_podio.x -= VEL_JUGADOR
        if teclas[pygame.K_RIGHT]:
            rect_podio.x += VEL_JUGADOR
        if teclas[pygame.K_UP]:
            rect_podio.y -= VEL_JUGADOR
        if teclas[pygame.K_DOWN]:
            rect_podio.y += VEL_JUGADOR

        # Evitar salir de pantalla
        rect_alonso.x = max(0, min(ANCHO - rect_alonso.width, rect_alonso.x))
        rect_alonso.y = max(0, min(ALTO - rect_alonso.height, rect_alonso.y))

        rect_podio.x = max(0, min(ANCHO - rect_podio.width, rect_podio.x))
        rect_podio.y = max(0, min(ALTO - rect_podio.height, rect_podio.y))

        # 3) Lógica: colisión jugador - objeto
        # Creamos un rect del objeto para colisión sencilla
        

        if rect_alonso.colliderect(rect_podio):
            puntuacion += 1
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("corresto.mp3")
            sonido.play()
            rect_podio.x = random.randint(0, min(ANCHO - rect_podio.width, rect_podio.x))
            rect_podio.y = random.randint(0, min(ALTO - rect_podio.height, rect_podio.y))

        # 4) Dibujado  
        pantalla.blit(fondo, (0, 0))


        # jugador (rectángulo)
        
        pantalla.blit(alonso, rect_alonso)
        pantalla.blit(podio, rect_podio)
        # objeto (círculo)
        
        
        

        # texto puntuación
        texto = fuente.render(f"Puntuación: {puntuacion}", True, (240, 240, 240))
        

        pantalla.blit(texto, (10, 10))
        pygame.display.flip()

        # 5) Control FPS
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
