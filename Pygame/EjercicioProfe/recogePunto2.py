import pygame
import random


# =========================================================
# CLASE Player
# - Responsabilidad: representar y mover al jugador
# - Atributos clave:
#   - rect: posición y tamaño del jugador
#   - speed: velocidad de movimiento
# - Métodos:
#   - handle_input(): lee teclas y modifica el rect
#   - update(): controla límites de pantalla
#   - draw(): dibuja el jugador
# =========================================================
class Player:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def handle_input(self):
        # Lee las teclas pulsadas y actualiza posición
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def keep_inside_screen(self, width, height):
        # Evita que el jugador salga de la pantalla
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(height - self.rect.height, self.rect.y))

    def update(self, screen_width, screen_height):
        # Separar input y límites ayuda a enseñar responsabilidades
        self.handle_input()
        self.keep_inside_screen(screen_width, screen_height)

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 180, 255), self.rect)


# =========================================================
# CLASE Coin
# - Responsabilidad: representar el objeto a recoger
# - Atributos clave:
#   - x, y: posición del centro de la moneda
#   - radius: radio del círculo
# - Métodos:
#   - respawn(): cambia la posición
#   - get_rect(): devuelve un Rect para detectar colisión fácil
#   - draw(): dibuja la moneda
# =========================================================
class Coin:
    def __init__(self, radius, screen_width, screen_height):
        self.radius = radius
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.respawn()

    def respawn(self):
        # Aparece en una posición aleatoria dentro de los límites
        self.x = random.randint(self.radius, self.screen_width - self.radius)
        self.y = random.randint(self.radius, self.screen_height - self.radius)

    def get_rect(self):
        # Rect de colisión (cuadrado que envuelve al círculo)
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 220, 60), (self.x, self.y), self.radius)


# =========================================================
# CLASE Score
# - Responsabilidad: gestionar la puntuación
# - Atributos clave:
#   - points: puntos actuales
#   - font: fuente para dibujar texto
# - Métodos:
#   - add(): suma puntos
#   - draw(): renderiza y dibuja el texto
# =========================================================
class Score:
    def __init__(self, font):
        self.points = 0
        self.font = font

    def add(self, amount=1):
        self.points += amount

    def draw(self, screen):
        text_surface = self.font.render(f"Puntuación: {self.points}", True, (240, 240, 240))
        screen.blit(text_surface, (10, 10))


# =========================================================
# CLASE Game
# - Responsabilidad: coordinar todo:
#   - Inicialización Pygame
#   - Bucle principal
#   - Eventos
#   - Actualización
#   - Colisiones
#   - Dibujado
# - Esta clase es la que el alumno suele "mapear" directamente
#   a su diagrama de clases como el controlador principal.
# =========================================================
class Game:
    def __init__(self):
        # Configuración general
        self.width = 800
        self.height = 600
        self.fps = 60

        # Inicialización Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Recoge el punto Version 2 (POO)")
        self.clock = pygame.time.Clock()

        # Recursos
        self.font = pygame.font.SysFont(None, 36)

        # Objetos del juego (según el diagrama de clases)
        self.player = Player(x=self.width // 2, y=self.height // 2, size=40, speed=5)
        self.coin = Coin(radius=10, screen_width=self.width, screen_height=self.height)
        self.score = Score(font=self.font)

        # Estado del bucle
        self.running = True

    def handle_events(self):
        # Maneja eventos del sistema (cerrar ventana, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_collisions(self):
        # Colisión jugador-moneda: si ocurre, suma puntos y respawnea la moneda
        if self.player.rect.colliderect(self.coin.get_rect()):
            self.score.add(1)
            self.coin.respawn()

    def update(self):
        # Actualiza el estado del juego (movimiento + colisiones)
        self.player.update(self.width, self.height)
        self.check_collisions()

    def draw(self):
        # Dibuja todo en pantalla
        self.screen.fill((20, 20, 30))  # fondo
        self.player.draw(self.screen)
        self.coin.draw(self.screen)
        self.score.draw(self.screen)

        pygame.display.flip()

    def run(self):
        # Bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()


# =========================================================
# PUNTO DE ENTRADA
# =========================================================
if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Pulsa ENTER para salir...")