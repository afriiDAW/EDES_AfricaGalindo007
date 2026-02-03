import pygame
import random
import os


# =========================================================
# StateManager: estados del juego
# =========================================================
class StateManager:
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"

    def __init__(self):
        self.state = self.MENU

    def set_state(self, new_state):
        self.state = new_state

    def is_menu(self):
        return self.state == self.MENU

    def is_playing(self):
        return self.state == self.PLAYING

    def is_paused(self):
        return self.state == self.PAUSED

    def is_game_over(self):
        return self.state == self.GAME_OVER


# =========================================================
# SoundManager: sonidos opcionales + mute
# =========================================================
class SoundManager:
    def __init__(self):
        self.enabled = False
        self.muted = False
        self.sounds = {}

        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def toggle_mute(self):
        self.muted = not self.muted

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
        if not self.enabled or self.muted:
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

    def reset(self):
        self.points = 0

    def add(self, amount=1):
        self.points += amount

    def draw(self, screen, x=10, y=10):
        surf = self.font.render(f"Puntuación: {self.points}", True, (240, 240, 240))
        screen.blit(surf, (x, y))


# =========================================================
# Lives: vidas (lo compondrá Player)
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
# Player: jugador (flechas) + composición Lives
# =========================================================
class Player:
    def __init__(self, x, y, size, speed, lives_component):
        self.spawn_x = x
        self.spawn_y = y
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

        # COMPOSICIÓN: las vidas forman parte del jugador
        self.lives = lives_component

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
# Enemy (base)
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

    def keep_inside(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

    def update(self, w, h, player=None, coin=None):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 90, 90), self.rect)


# =========================================================
# HumanEnemy: WASD
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
# AutoEnemy: IA simple con objetivo seleccionable
# - target_mode puede ser "PLAYER" o "COIN"
# =========================================================
class AutoEnemy(Enemy):
    def __init__(self, x, y, size, speed, target_mode="PLAYER"):
        super().__init__(x, y, size, speed)
        self.target_mode = target_mode  # "PLAYER" o "COIN"

    def set_target_mode(self, target_mode):
        self.target_mode = target_mode

    def update(self, w, h, player=None, coin=None):
        # Elegimos el objetivo (centro) según el modo
        if self.target_mode == "COIN" and coin is not None:
            target_x = coin.x
            target_y = coin.y
        elif player is not None:
            target_x = player.rect.centerx
            target_y = player.rect.centery
        else:
            return

        # Movimiento simple hacia el objetivo
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
        pygame.display.set_caption("Recoge el punto - Versión 5 (pausa + IA objetivo + mute)")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        # Managers
        self.state = StateManager()
        self.sounds = SoundManager()

        # Sonidos opcionales (si tienes archivos)
        self.sounds.load_sound("coin", "coin.mp3")
        self.sounds.load_sound("hit", "hit.wav")

        # HUD
        self.score = Score(font=self.font)

        # Entidades
        lives_component = Lives(font=self.font, initial_lives=3)
        self.player = Player(x=100, y=self.height // 2, size=40, speed=5, lives_component=lives_component)
        self.coin = Coin(radius=10, w=self.width, h=self.height)

        # Enemigo (selección)
        self.enemy = None
        self.enemy_mode = None        # "HUMAN" o "AUTO"
        self.auto_target_mode = "PLAYER"  # "PLAYER" o "COIN"

        self.running = True

    # --------------------------
    # Selección de enemigo / objetivo
    # --------------------------
    def set_enemy_mode(self, mode):
        self.enemy_mode = mode

        ex = self.width - 140
        ey = self.height // 2

        if mode == "HUMAN":
            self.enemy = HumanEnemy(x=ex, y=ey, size=40, speed=5)
        elif mode == "AUTO":
            # AutoEnemy con objetivo configurable
            self.enemy = AutoEnemy(x=ex, y=ey, size=40, speed=4, target_mode=self.auto_target_mode)
        else:
            self.enemy = None

    def set_auto_target_mode(self, target_mode):
        self.auto_target_mode = target_mode
        # Si ya existe un autoenemigo, actualizamos su modo en caliente (para el menú y futuras extensiones)
        if isinstance(self.enemy, AutoEnemy):
            self.enemy.set_target_mode(target_mode)

    # --------------------------
    # Reinicio de partida
    # --------------------------
    def start_game(self):
        self.score.reset()
        self.player.lives.reset()

        self.player.respawn()
        self.coin.respawn()

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
                # Mute global (en cualquier estado)
                if event.key == pygame.K_m:
                    self.sounds.toggle_mute()

                # MENU
                if self.state.is_menu():
                    # Elegir tipo de enemigo
                    if event.key == pygame.K_1:
                        self.set_enemy_mode("HUMAN")
                    if event.key == pygame.K_2:
                        self.set_enemy_mode("AUTO")

                    # Elegir objetivo del autoenemigo (solo tiene sentido si eliges AUTO)
                    if event.key == pygame.K_j:
                        self.set_auto_target_mode("PLAYER")
                        # Si el enemigo ya está en AUTO, recrearlo para asegurar coherencia
                        if self.enemy_mode == "AUTO":
                            self.set_enemy_mode("AUTO")

                    if event.key == pygame.K_c:
                        self.set_auto_target_mode("COIN")
                        if self.enemy_mode == "AUTO":
                            self.set_enemy_mode("AUTO")

                    # Empezar
                    if event.key == pygame.K_RETURN:
                        self.start_game()

                # PLAYING
                elif self.state.is_playing():
                    # Pausa
                    if event.key == pygame.K_p:
                        self.state.set_state(StateManager.PAUSED)

                    # ESC vuelve al menú (simple)
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)

                # PAUSED
                elif self.state.is_paused():
                    # Reanudar
                    if event.key == pygame.K_p:
                        self.state.set_state(StateManager.PLAYING)
                    # Salir al menú
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)

                # GAME_OVER
                elif self.state.is_game_over():
                    if event.key == pygame.K_r:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

    # --------------------------
    # Actualización (solo si PLAYING)
    # --------------------------
    def update(self):
        if not self.state.is_playing():
            return

        self.player.update(self.width, self.height)
        self.enemy.update(self.width, self.height, player=self.player, coin=self.coin)

        self.check_coin_pickup()
        self.check_player_hit()

        if self.player.lives.is_dead():
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
            self.player.lives.lose_one()

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
            self.player.lives.draw(self.screen)

            self.draw_hud_hints()

        elif self.state.is_paused():
            # En pausa: dibujamos el último frame "congelado" (opcional).
            # Para simplificar, dibujamos una escena similar y un rótulo de PAUSA.
            self.player.draw(self.screen)
            if self.enemy:
                self.enemy.draw(self.screen)
            self.coin.draw(self.screen)
            self.score.draw(self.screen)
            self.player.lives.draw(self.screen)

            overlay = self.big_font.render("PAUSA", True, (240, 240, 240))
            self.screen.blit(overlay, (self.width // 2 - overlay.get_width() // 2, 220))

            hint = self.font.render("P: reanudar | ESC: menú | M: mute", True, (220, 220, 220))
            self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, 300))

        elif self.state.is_game_over():
            self.draw_game_over()

        pygame.display.flip()

    def draw_hud_hints(self):
        mute_state = "ON" if self.sounds.muted else "OFF"
        hint0 = self.font.render(f"Mute: {mute_state} (M)", True, (200, 200, 200))
        self.screen.blit(hint0, (10, self.height - 90))

        hint1 = self.font.render("Jugador: Flechas | P: Pausa | ESC: Menú", True, (200, 200, 200))
        self.screen.blit(hint1, (10, self.height - 60))

        if self.enemy_mode == "HUMAN":
            hint2 = self.font.render("Enemigo: WASD (humano)", True, (200, 200, 200))
        else:
            target = "Jugador (J)" if self.auto_target_mode == "PLAYER" else "Moneda (C)"
            hint2 = self.font.render(f"Enemigo: automático | Objetivo: {target}", True, (200, 200, 200))
        self.screen.blit(hint2, (10, self.height - 30))

    def draw_menu(self):
        title = self.big_font.render("RECOGE EL PUNTO", True, (240, 240, 240))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 110))

        line = self.font.render("Selecciona el tipo de enemigo:", True, (220, 220, 220))
        self.screen.blit(line, (self.width // 2 - line.get_width() // 2, 210))

        opt1 = self.font.render("1) Humano (WASD)", True, (220, 220, 220))
        opt2 = self.font.render("2) Automático (IA)", True, (220, 220, 220))
        self.screen.blit(opt1, (self.width // 2 - opt1.get_width() // 2, 260))
        self.screen.blit(opt2, (self.width // 2 - opt2.get_width() // 2, 300))

        line2 = self.font.render("Si eliges Automático, selecciona objetivo:", True, (220, 220, 220))
        self.screen.blit(line2, (self.width // 2 - line2.get_width() // 2, 360))

        optj = self.font.render("J) Perseguir al Jugador", True, (220, 220, 220))
        optc = self.font.render("C) Perseguir la Moneda", True, (220, 220, 220))
        self.screen.blit(optj, (self.width // 2 - optj.get_width() // 2, 400))
        self.screen.blit(optc, (self.width // 2 - optc.get_width() // 2, 440))

        selected_enemy = "Ninguno" if self.enemy_mode is None else self.enemy_mode
        selected_target = "Jugador" if self.auto_target_mode == "PLAYER" else "Moneda"

        info1 = self.font.render(f"Enemigo seleccionado: {selected_enemy}", True, (255, 220, 60))
        self.screen.blit(info1, (self.width // 2 - info1.get_width() // 2, 500))

        info2 = self.font.render(f"Objetivo IA: {selected_target}", True, (255, 220, 60))
        self.screen.blit(info2, (self.width // 2 - info2.get_width() // 2, 530))

        start = self.font.render("Enter: empezar | M: mute", True, (200, 200, 200))
        self.screen.blit(start, (self.width // 2 - start.get_width() // 2, 560))

    def draw_game_over(self):
        title = self.big_font.render("GAME OVER", True, (255, 120, 120))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 160))

        final_score = self.font.render(f"Puntuación final: {self.score.points}", True, (240, 240, 240))
        self.screen.blit(final_score, (self.width // 2 - final_score.get_width() // 2, 250))

        enemy_mode = self.enemy_mode if self.enemy_mode else "N/A"
        if enemy_mode == "AUTO":
            target = "Jugador" if self.auto_target_mode == "PLAYER" else "Moneda"
            mode_text = self.font.render(f"Enemigo: AUTO | Objetivo: {target}", True, (240, 240, 240))
        else:
            mode_text = self.font.render("Enemigo: HUMANO", True, (240, 240, 240))
        self.screen.blit(mode_text, (self.width // 2 - mode_text.get_width() // 2, 290))

        line1 = self.font.render("R: reiniciar", True, (220, 220, 220))
        line2 = self.font.render("ESC: salir", True, (220, 220, 220))
        line3 = self.font.render("M: mute", True, (220, 220, 220))
        self.screen.blit(line1, (self.width // 2 - line1.get_width() // 2, 360))
        self.screen.blit(line2, (self.width // 2 - line2.get_width() // 2, 400))
        self.screen.blit(line3, (self.width // 2 - line3.get_width() // 2, 440))

    # --------------------------
    # Loop principal
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
