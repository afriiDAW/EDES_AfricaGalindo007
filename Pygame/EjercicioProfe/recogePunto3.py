import pygame
import random
import os


# =========================================================
# StateManager: controla el estado del juego (MENU/PLAYING/GAME_OVER)
# =========================================================
class StateManager:
    MENU = "MENU"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"

    def __init__(self):
        self.state = self.MENU

    def set_state(self, new_state):
        self.state = new_state

    def is_menu(self):
        return self.state == self.MENU

    def is_playing(self):
        return self.state == self.PLAYING

    def is_game_over(self):
        return self.state == self.GAME_OVER


# =========================================================
# SoundManager: carga y reproduce sonidos (si existen)
# - Es intencionalmente simple y tolerante a errores.
# - Si no hay archivos, no pasa nada (modo silencioso).
# =========================================================
class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        # Intentamos inicializar el mixer; si falla, seguimos sin sonidos.
        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def load_sound(self, name, filepath):
        # Carga un sonido si el mixer está disponible y el archivo existe
        if not self.enabled:
            return
        if not os.path.exists(filepath):
            return
        try:
            self.sounds[name] = pygame.mixer.Sound(filepath)
        except pygame.error:
            # Si hay algún problema con el archivo, no bloqueamos el juego
            pass

    def play(self, name):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()


# =========================================================
# Score: gestiona puntos del jugador
# =========================================================
class Score:
    def __init__(self, font):
        self.points = 0
        self.font = font

    def add(self, amount=1):
        self.points += amount

    def reset(self):
        self.points = 0

    def draw(self, screen, x=10, y=10):
        surface = self.font.render(f"Puntuación: {self.points}", True, (240, 240, 240))
        screen.blit(surface, (x, y))


# =========================================================
# Lives: gestiona vidas del jugador
# =========================================================
class Lives:
    def __init__(self, font, initial_lives=3):
        self.font = font
        self.initial_lives = initial_lives
        self.lives = initial_lives

    def lose_one(self):
        self.lives -= 1
        if self.lives < 0:
            self.lives = 0

    def reset(self):
        self.lives = self.initial_lives

    def is_dead(self):
        return self.lives == 0

    def draw(self, screen, x=10, y=45):
        surface = self.font.render(f"Vidas: {self.lives}", True, (240, 240, 240))
        screen.blit(surface, (x, y))


# =========================================================
# Player: jugador principal (control por flechas)
# =========================================================
class Player:
    def __init__(self, x, y, size, speed):
        self.spawn_x = x
        self.spawn_y = y
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def respawn(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def keep_inside_screen(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

    def update(self, w, h):
        self.handle_input()
        self.keep_inside_screen(w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 180, 255), self.rect)


# =========================================================
# Enemy (base): diseñado para poder tener tipos distintos
# - En esta versión usaremos un enemigo "humano" (WASD).
# - Más adelante podrás crear AutoEnemy heredando de Enemy.
# =========================================================
class Enemy:
    def __init__(self, x, y, size, speed):
        self.spawn_x = x
        self.spawn_y = y
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def respawn(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y

    def update(self, w, h, player=None, coin=None):
        # Se implementa en subclases (humano o automático)
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 90, 90), self.rect)


class HumanEnemy(Enemy):
    # Control por teclado WASD
    def update(self, w, h, player=None, coin=None):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Mantener dentro de pantalla
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))


# =========================================================
# Coin: objeto a recoger
# =========================================================
class Coin:
    def __init__(self, radius, w, h):
        self.radius = radius
        self.w = w
        self.h = h
        self.respawn()

    def respawn(self):
        self.x = random.randint(self.radius, self.w - self.radius)
        self.y = random.randint(self.radius, self.h - self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 220, 60), (self.x, self.y), self.radius)


# =========================================================
# Game: orquesta todo (estados, bucle, colisiones, HUD)
# =========================================================
class Game:
    def __init__(self):
        # Configuración
        self.width = 800
        self.height = 600
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Recoge el punto - Versión 3 (2 jugadores)")
        self.clock = pygame.time.Clock()

        # Recursos
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        # Managers
        self.state = StateManager()
        self.sounds = SoundManager()

        # (Opcional) Cargar sonidos. Si no tienes archivos, no pasa nada.
        self.sounds.load_sound("coin", "coin.mp3")
        self.sounds.load_sound("hit", "hit.wav")

        # Entidades (POO)
        self.player = Player(x=100, y=self.height // 2, size=40, speed=5)
        self.enemy = HumanEnemy(x=self.width - 140, y=self.height // 2, size=40, speed=5)
        self.coin = Coin(radius=10, w=self.width, h=self.height)

        self.score = Score(font=self.font)
        self.lives = Lives(font=self.font, initial_lives=3)

        self.running = True

    # --------------------------
    # Eventos globales
    # --------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Teclas para controlar estados
            if event.type == pygame.KEYDOWN:
                if self.state.is_menu():
                    # En menú: Enter para empezar
                    if event.key == pygame.K_RETURN:
                        self.start_game()

                elif self.state.is_game_over():
                    # En game over: R para reiniciar, ESC para salir
                    if event.key == pygame.K_r:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state.is_playing():
                    # En juego: ESC vuelve al menú (simple)
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)

    def start_game(self):
        # Reinicia todo lo necesario para una nueva partida
        self.score.reset()
        self.lives.reset()
        self.player.respawn()
        self.enemy.respawn()
        self.coin.respawn()
        self.state.set_state(StateManager.PLAYING)

    # --------------------------
    # Actualización por estado
    # --------------------------
    def update(self):
        if self.state.is_playing():
            self.player.update(self.width, self.height)
            self.enemy.update(self.width, self.height, player=self.player, coin=self.coin)

            self.check_coin_pickup()
            self.check_player_hit()

            if self.lives.is_dead():
                self.state.set_state(StateManager.GAME_OVER)

    # --------------------------
    # Colisiones
    # --------------------------
    def check_coin_pickup(self):
        if self.player.rect.colliderect(self.coin.get_rect()):
            self.score.add(1)
            self.coin.respawn()
            self.sounds.play("coin")  # si existe

    def check_player_hit(self):
        # Si enemigo toca al jugador, el jugador pierde una vida y se reposicionan
        if self.enemy.rect.colliderect(self.player.rect):
            self.lives.lose_one()
            self.player.respawn()
            self.enemy.respawn()
            self.coin.respawn()
            self.sounds.play("hit")  # si existe

    # --------------------------
    # Dibujado por estado
    # --------------------------
    def draw(self):
        self.screen.fill((20, 20, 30))

        if self.state.is_menu():
            self.draw_menu()

        elif self.state.is_playing():
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            self.coin.draw(self.screen)
            self.score.draw(self.screen)
            self.lives.draw(self.screen)

            # Indicaciones de control en pantalla
            hint1 = self.font.render("Jugador: Flechas | Enemigo: WASD | ESC: Menú", True, (200, 200, 200))
            self.screen.blit(hint1, (10, self.height - 30))

        elif self.state.is_game_over():
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        title = self.big_font.render("REC OGE EL PUNTO", True, (240, 240, 240))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 140))

        line1 = self.font.render("Enter: empezar", True, (220, 220, 220))
        line2 = self.font.render("Jugador: Flechas", True, (220, 220, 220))
        line3 = self.font.render("Enemigo: WASD (2ª persona)", True, (220, 220, 220))
        self.screen.blit(line1, (self.width // 2 - line1.get_width() // 2, 260))
        self.screen.blit(line2, (self.width // 2 - line2.get_width() // 2, 310))
        self.screen.blit(line3, (self.width // 2 - line3.get_width() // 2, 350))

    def draw_game_over(self):
        title = self.big_font.render("GAME OVER", True, (255, 120, 120))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 170))

        final_score = self.font.render(f"Puntuación final: {self.score.points}", True, (240, 240, 240))
        self.screen.blit(final_score, (self.width // 2 - final_score.get_width() // 2, 260))

        line1 = self.font.render("R: reiniciar", True, (220, 220, 220))
        line2 = self.font.render("ESC: salir", True, (220, 220, 220))
        self.screen.blit(line1, (self.width // 2 - line1.get_width() // 2, 320))
        self.screen.blit(line2, (self.width // 2 - line2.get_width() // 2, 360))

    # --------------------------
    # Bucle principal
    # --------------------------
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()


# =========================================================
# Entrada
# =========================================================
if __name__ == "__main__":
    Game().run()
