import pygame
import random
import os


# =========================================================
# StateManager: estados del juego
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
# SoundManager: sonidos opcionales
# =========================================================
class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds = {}

        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def load_sound(self, name, filepath):
        if not self.enabled:
            return
        if not os.path.exists(filepath):
            return
        try:
            self.sounds[name] = pygame.mixer.Sound(filepath)
        except pygame.error:
            pass

    def play(self, name):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()


# =========================================================
# Score: puntos
# =========================================================
class Score:
    def __init__(self, font):
        self.font = font
        self.points = 0

    def add(self, amount=1):
        self.points += amount

    def reset(self):
        self.points = 0

    def draw(self, screen, x=10, y=10):
        surf = self.font.render(f"Puntuación: {self.points}", True, (240, 240, 240))
        screen.blit(surf, (x, y))


# =========================================================
# Lives: vidas
# =========================================================
class Lives:
    def __init__(self, font, initial_lives=3):
        self.font = font
        self.initial_lives = initial_lives
        self.lives = initial_lives

    def reset(self):
        self.lives = self.initial_lives

    def lose_one(self):
        self.lives -= 1
        if self.lives < 0:
            self.lives = 0

    def is_dead(self):
        return self.lives == 0

    def draw(self, screen, x=10, y=45):
        surf = self.font.render(f"Vidas: {self.lives}", True, (240, 240, 240))
        screen.blit(surf, (x, y))


# =========================================================
# Player: jugador (flechas)
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

    def keep_inside(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

    def update(self, w, h):
        self.handle_input()
        self.keep_inside(w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 180, 255), self.rect)


# =========================================================
# Coin: moneda
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
# Enemy (base): permite elegir tipo
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
        # Se implementa en subclases
        pass

    def keep_inside(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 90, 90), self.rect)


# =========================================================
# HumanEnemy: enemigo controlado por WASD
# =========================================================
class HumanEnemy(Enemy):
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

        self.keep_inside(w, h)


# =========================================================
# AutoEnemy: enemigo automático (IA simple)
# - En esta versión: persigue al jugador.
# - Puedes cambiar el objetivo a coin fácilmente.
# =========================================================
class AutoEnemy(Enemy):
    def update(self, w, h, player=None, coin=None):
        # Elegimos objetivo:
        # - Por defecto: perseguir al jugador
        if player is None:
            return

        target_x = player.rect.centerx
        target_y = player.rect.centery

        # Movimiento simple: si estoy a la izquierda del objetivo, avanzo; etc.
        if self.rect.centerx < target_x:
            self.rect.x += self.speed
        elif self.rect.centerx > target_x:
            self.rect.x -= self.speed

        if self.rect.centery < target_y:
            self.rect.y += self.speed
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed

        self.keep_inside(w, h)


# =========================================================
# Game: controlador principal
# =========================================================
class Game:
    def __init__(self):
        # Configuración
        self.width = 800
        self.height = 600
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Recoge el punto - Versión 4 (enemigo elegible)")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        # Managers
        self.state = StateManager()
        self.sounds = SoundManager()

        # Sonidos opcionales (si tienes archivos)
        self.sounds.load_sound("coin", "coin.mp3")
        self.sounds.load_sound("hit", "hit.wav")

        # Entidades base (se crean aquí)
        self.player = Player(x=100, y=self.height // 2, size=40, speed=5)
        self.coin = Coin(radius=10, w=self.width, h=self.height)

        # El enemigo depende de la elección en el menú
        self.enemy = None
        self.enemy_mode = None  # "HUMAN" o "AUTO"

        # HUD
        self.score = Score(font=self.font)
        self.lives = Lives(font=self.font, initial_lives=3)

        self.running = True

    # --------------------------
    # Creación del enemigo según elección
    # --------------------------
    def set_enemy_mode(self, mode):
        self.enemy_mode = mode

        # Posición inicial del enemigo a la derecha
        ex = self.width - 140
        ey = self.height // 2

        if mode == "HUMAN":
            self.enemy = HumanEnemy(x=ex, y=ey, size=40, speed=5)
        elif mode == "AUTO":
            self.enemy = AutoEnemy(x=ex, y=ey, size=40, speed=4)  # un poco más lento para ser justo
        else:
            self.enemy = None

    # --------------------------
    # Reinicio de partida
    # --------------------------
    def start_game(self):
        self.score.reset()
        self.lives.reset()
        self.player.respawn()
        self.coin.respawn()

        # Si no se eligió modo, por defecto humano (para evitar None)
        if self.enemy is None:
            self.set_enemy_mode("HUMAN")

        self.enemy.respawn()
        self.state.set_state(StateManager.PLAYING)

    # --------------------------
    # Eventos
    # --------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # MENU
                if self.state.is_menu():
                    # Elegir modo de enemigo
                    if event.key == pygame.K_1:
                        self.set_enemy_mode("HUMAN")
                    if event.key == pygame.K_2:
                        self.set_enemy_mode("AUTO")

                    # Empezar
                    if event.key == pygame.K_RETURN:
                        self.start_game()

                # PLAYING
                elif self.state.is_playing():
                    # ESC vuelve al menú (simple)
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)

                # GAME_OVER
                elif self.state.is_game_over():
                    if event.key == pygame.K_r:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

    # --------------------------
    # Actualización
    # --------------------------
    def update(self):
        if not self.state.is_playing():
            return

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
            self.sounds.play("coin")

    def check_player_hit(self):
        if self.enemy.rect.colliderect(self.player.rect):
            self.lives.lose_one()

            # Respawn "limpio" para que se note el impacto y reinicio del duelo
            self.player.respawn()
            self.enemy.respawn()
            self.coin.respawn()

            self.sounds.play("hit")

    # --------------------------
    # Dibujado
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

            hint = self.font.render("ESC: Menú | Jugador: Flechas", True, (200, 200, 200))
            self.screen.blit(hint, (10, self.height - 30))

            if self.enemy_mode == "HUMAN":
                hint2 = self.font.render("Enemigo: WASD (humano)", True, (200, 200, 200))
            else:
                hint2 = self.font.render("Enemigo: automático (IA simple)", True, (200, 200, 200))
            self.screen.blit(hint2, (10, self.height - 60))

        elif self.state.is_game_over():
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        title = self.big_font.render("RECOGE EL PUNTO", True, (240, 240, 240))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 120))

        subtitle = self.font.render("Elige tipo de enemigo:", True, (220, 220, 220))
        self.screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 220))

        opt1 = self.font.render("1) Humano (WASD)", True, (220, 220, 220))
        opt2 = self.font.render("2) Automático (IA simple)", True, (220, 220, 220))
        self.screen.blit(opt1, (self.width // 2 - opt1.get_width() // 2, 270))
        self.screen.blit(opt2, (self.width // 2 - opt2.get_width() // 2, 310))

        # Mostrar selección actual
        selected = "Ninguno (elige 1 o 2)" if self.enemy_mode is None else self.enemy_mode
        sel_text = self.font.render(f"Seleccionado: {selected}", True, (255, 220, 60))
        self.screen.blit(sel_text, (self.width // 2 - sel_text.get_width() // 2, 360))

        start = self.font.render("Enter: empezar | Flechas: jugador | Esc: salir en game over", True, (200, 200, 200))
        self.screen.blit(start, (self.width // 2 - start.get_width() // 2, 430))

    def draw_game_over(self):
        title = self.big_font.render("GAME OVER", True, (255, 120, 120))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 160))

        final_score = self.font.render(f"Puntuación final: {self.score.points}", True, (240, 240, 240))
        self.screen.blit(final_score, (self.width // 2 - final_score.get_width() // 2, 250))

        mode = self.enemy_mode if self.enemy_mode else "N/A"
        mode_text = self.font.render(f"Modo enemigo: {mode}", True, (240, 240, 240))
        self.screen.blit(mode_text, (self.width // 2 - mode_text.get_width() // 2, 290))

        line1 = self.font.render("R: reiniciar", True, (220, 220, 220))
        line2 = self.font.render("ESC: salir", True, (220, 220, 220))
        self.screen.blit(line1, (self.width // 2 - line1.get_width() // 2, 360))
        self.screen.blit(line2, (self.width // 2 - line2.get_width() // 2, 400))

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


if __name__ == "__main__":
    Game().run()
