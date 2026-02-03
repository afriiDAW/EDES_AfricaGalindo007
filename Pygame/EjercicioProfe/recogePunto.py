import pygame
import random

# ---------------------------
# Configuración
# ---------------------------
ANCHO, ALTO = 800, 600
FPS = 60

TAM_JUGADOR = 40
VEL_JUGADOR = 5

RAD_OBJETO = 10

def nueva_pos_objeto():
    x = random.randint(RAD_OBJETO, ANCHO - RAD_OBJETO)
    y = random.randint(RAD_OBJETO, ALTO - RAD_OBJETO)
    return x, y

def main():
    pygame.init()

    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Recoge el punto (Pygame)")
    icono = pygame.image.load("trump.png")
    pygame.display.set_icon(icono)
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 36)

    # Jugador como rectángulo
    jugador = pygame.Rect(ANCHO // 2, ALTO // 2, TAM_JUGADOR, TAM_JUGADOR)

    # Objeto a recoger (círculo)
    obj_x, obj_y = nueva_pos_objeto()

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
            jugador.x -= VEL_JUGADOR
        if teclas[pygame.K_d]:
            jugador.x += VEL_JUGADOR
        if teclas[pygame.K_w]:
            jugador.y -= VEL_JUGADOR
        if teclas[pygame.K_s]:
            jugador.y += VEL_JUGADOR

        # Evitar salir de pantalla
        jugador.x = max(0, min(ANCHO - jugador.width, jugador.x))
        jugador.y = max(0, min(ALTO - jugador.height, jugador.y))

        # 3) Lógica: colisión jugador - objeto
        # Creamos un rect del objeto para colisión sencilla
        obj_rect = pygame.Rect(obj_x - RAD_OBJETO, obj_y - RAD_OBJETO, RAD_OBJETO * 2, RAD_OBJETO * 2)

        if jugador.colliderect(obj_rect):
            puntuacion += 1
            obj_x, obj_y = nueva_pos_objeto()

        # 4) Dibujado
        pantalla.fill((158, 158, 158))  # fondo oscuro

        # jugador (rectángulo)
        pygame.draw.rect(pantalla, (230, 99, 99), jugador)

        # objeto (círculo)
        pygame.draw.circle(pantalla, (124, 189, 89), (obj_x, obj_y), RAD_OBJETO)
        

        # texto puntuación
        texto = fuente.render(f"Puntuación: {puntuacion}", True, (240, 240, 240))
        pantalla.blit(texto, (10, 10))
        texto = fuente.render("Africa Galindo", True, (89, 189, 177))
        pantalla.blit(texto, (100, 100))
        pygame.display.flip()

        # 5) Control FPS
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
