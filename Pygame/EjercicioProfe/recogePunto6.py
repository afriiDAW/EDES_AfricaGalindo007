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
# HUD simples
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
# Utilidad: crear "sprite" simple con Surface de color
# (si quieres imágenes, sustituyes esto por image.load)
# =========================================================
def make_colored_sprite_surface(w, h, color):
    surface = pygame.Surface((w, h), pygame.SRCALPHA)
    surface.fill(color)
    return surface


# =========================================================
# Player Sprite: flechas + invencibilidad (3s cuando recoge power-up)
# - Composición: Lives dentro del Player
# =========================================================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed, lives_component):
        super().__init__()
        self.image_normal = make_colored_sprite_surface(size, size, (70, 180, 255))
        # Cuando está invencible lo "marcamos" visualmente (más claro para alumnos)
        self.image_invincible = make_colored_sprite_surface(size, size, (140, 255, 180))
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        self.spawn_pos = (x, y)
        self.speed = speed

        # Composición
        self.lives = lives_component

        # Power-up invencibilidad
        self.invincible_until_ms = 0

    def respawn(self):
        self.rect.topleft = self.spawn_pos

    def set_invincible(self, duration_ms):
        now = pygame.time.get_ticks()
        self.invincible_until_ms = now + duration_ms

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until_ms

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed
        return dx, dy

    def keep_inside(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

    def update(self, w, h):
        dx, dy = self.handle_input()
        self.rect.x += dx
        self.rect.y += dy
        self.keep_inside(w, h)

        # Cambia sprite según invencibilidad
        self.image = self.image_invincible if self.is_invincible() else self.image_normal


# =========================================================
# Coin Sprite: moneda (círculo dibujado en surface)
# =========================================================
class Coin(pygame.sprite.Sprite):
    def __init__(self, radius, w, h):
        super().__init__()
        self.radius = radius
        self.w = w
        self.h = h

        size = radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 220, 60), (radius, radius), radius)
        self.rect = self.image.get_rect()

        self.respawn()

    def respawn(self):
        self.rect.centerx = random.randint(self.radius, self.w - self.radius)
        self.rect.centery = random.randint(self.radius, self.h - self.radius)


# =========================================================
# PowerUp: invencibilidad (3 segundos)
# - Aparece de forma ocasional y desaparece al recogerlo o por tiempo
# =========================================================
class InvincibilityPowerUp(pygame.sprite.Sprite):
    def __init__(self, w, h, duration_ms=3000, lifetime_ms=6000):
        super().__init__()
        self.w = w
        self.h = h
        self.duration_ms = duration_ms     # lo que dura la invencibilidad en el jugador
        self.lifetime_ms = lifetime_ms     # lo que dura el power-up en pantalla

        # Sprite visual (estrella simple)
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 120, 255), (13, 13), 12)
        pygame.draw.circle(self.image, (240, 220, 255), (13, 13), 6)
        self.rect = self.image.get_rect()

        self.spawned_at_ms = 0
        self.active = False

    def spawn(self):
        self.rect.centerx = random.randint(20, self.w - 20)
        self.rect.centery = random.randint(20, self.h - 20)
        self.spawned_at_ms = pygame.time.get_ticks()
        self.active = True

    def despawn(self):
        self.active = False

    def update(self):
        # Si está activo y “caduca”, desaparece
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.spawned_at_ms > self.lifetime_ms:
                self.despawn()


# =========================================================
# Enemy base Sprite + HumanEnemy + AutoEnemy
# =========================================================
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed):
        super().__init__()
        self.image = make_colored_sprite_surface(size, size, (255, 90, 90))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_pos = (x, y)
        self.speed = speed

    def respawn(self):
        self.rect.topleft = self.spawn_pos

    def keep_inside(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

    def update(self, w, h, player=None, coin=None):
        pass


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


class AutoEnemy(Enemy):
    def __init__(self, x, y, size, speed, target_mode="PLAYER"):
        super().__init__(x, y, size, speed)
        self.target_mode = target_mode  # "PLAYER" o "COIN"

    def set_target_mode(self, target_mode):
        self.target_mode = target_mode

    def update(self, w, h, player=None, coin=None):
        if self.target_mode == "COIN" and coin is not None:
            target_x, target_y = coin.rect.centerx, coin.rect.centery
        elif player is not None:
            target_x, target_y = player.rect.centerx, player.rect.centery
        else:
            return

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
# Game
# =========================================================
class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.fps = 60

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Recoge el punto - Versión 6 (sprites + power-up)")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        self.state = StateManager()
        self.sounds = SoundManager()

        # Sonidos opcionales (si tienes archivos)
        self.sounds.load_sound("coin", "coin.mp3")
        self.sounds.load_sound("hit", "hit.wav")
        self.sounds.load_sound("power", "hit.wav")

        self.score = Score(self.font)

        # Player con Lives como composición
        lives_component = Lives(self.font, initial_lives=3)
        self.player = Player(x=100, y=self.height // 2, size=40, speed=5, lives_component=lives_component)

        # Enemy elegido en el menú
        self.enemy = None
        self.enemy_mode = None        # "HUMAN" / "AUTO"
        self.auto_target_mode = "PLAYER"  # "PLAYER" / "COIN"

        # Coin
        self.coin = Coin(radius=10, w=self.width, h=self.height)

        # Power-up invencibilidad
        self.powerup = InvincibilityPowerUp(w=self.width, h=self.height, duration_ms=3000, lifetime_ms=6000)

        # Sprites y grupos
        self.all_sprites = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        self.running = True

        # Configuración de spawn del power-up
        self.next_powerup_at_ms = 0
        self.schedule_next_powerup()

    # --------------------------
    # Power-up spawn programado (simple)
    # --------------------------
    def schedule_next_powerup(self):
        # Aparece de forma “aleatoria” entre 4 y 9 segundos
        now = pygame.time.get_ticks()
        delay = random.randint(4000, 9000)
        self.next_powerup_at_ms = now + delay

    def maybe_spawn_powerup(self):
        if self.powerup.active:
            return
        now = pygame.time.get_ticks()
        if now >= self.next_powerup_at_ms:
            self.powerup.spawn()
            self.schedule_next_powerup()

    # --------------------------
    # Elección enemigo / objetivo
    # --------------------------
    def set_enemy_mode(self, mode):
        self.enemy_mode = mode
        ex = self.width - 140
        ey = self.height // 2

        if mode == "HUMAN":
            self.enemy = HumanEnemy(x=ex, y=ey, size=40, speed=5)
        elif mode == "AUTO":
            self.enemy = AutoEnemy(x=ex, y=ey, size=40, speed=4, target_mode=self.auto_target_mode)
        else:
            self.enemy = None

    def set_auto_target_mode(self, target_mode):
        self.auto_target_mode = target_mode
        if isinstance(self.enemy, AutoEnemy):
            self.enemy.set_target_mode(target_mode)

    # --------------------------
    # Preparar grupos de sprites (se llama al iniciar partida)
    # --------------------------
    def rebuild_sprite_groups(self):
        self.all_sprites.empty()
        self.coin_group.empty()
        self.powerup_group.empty()

        self.all_sprites.add(self.player)
        if self.enemy:
            self.all_sprites.add(self.enemy)

        self.coin_group.add(self.coin)
        self.all_sprites.add(self.coin)

        # El power-up solo se dibuja si está activo
        # (lo añadimos al grupo, pero controlamos su visibilidad por active)
        self.powerup_group.add(self.powerup)
        self.all_sprites.add(self.powerup)

    # --------------------------
    # Iniciar partida
    # --------------------------
    def start_game(self):
        self.score.reset()
        self.player.lives.reset()
        self.player.respawn()
        self.coin.respawn()

        if self.enemy is None:
            self.set_enemy_mode("HUMAN")
        self.enemy.respawn()

        # Power-up: reinicio
        self.powerup.despawn()
        self.schedule_next_powerup()

        self.rebuild_sprite_groups()
        self.state.set_state(StateManager.PLAYING)

    # --------------------------
    # Eventos
    # --------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Mute global
                if event.key == pygame.K_m:
                    self.sounds.toggle_mute()

                if self.state.is_menu():
                    if event.key == pygame.K_1:
                        self.set_enemy_mode("HUMAN")
                    if event.key == pygame.K_2:
                        self.set_enemy_mode("AUTO")

                    if event.key == pygame.K_j:
                        self.set_auto_target_mode("PLAYER")
                        if self.enemy_mode == "AUTO":
                            self.set_enemy_mode("AUTO")  # recrea con el nuevo objetivo

                    if event.key == pygame.K_c:
                        self.set_auto_target_mode("COIN")
                        if self.enemy_mode == "AUTO":
                            self.set_enemy_mode("AUTO")

                    if event.key == pygame.K_RETURN:
                        self.start_game()

                elif self.state.is_playing():
                    if event.key == pygame.K_p:
                        self.state.set_state(StateManager.PAUSED)
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)

                elif self.state.is_paused():
                    if event.key == pygame.K_p:
                        self.state.set_state(StateManager.PLAYING)
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)

                elif self.state.is_game_over():
                    if event.key == pygame.K_r:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

    # --------------------------
    # Update (solo PLAYING)
    # --------------------------
    def update(self):
        if not self.state.is_playing():
            return

        # Posible aparición del power-up
        self.maybe_spawn_powerup()

        # Actualizar sprites
        self.player.update(self.width, self.height)
        self.enemy.update(self.width, self.height, player=self.player, coin=self.coin)

        # Actualizar power-up (caducidad)
        self.powerup.update()

        # Colisiones
        self.check_coin_pickup()
        self.check_powerup_pickup()
        self.check_player_hit()

        if self.player.lives.is_dead():
            self.state.set_state(StateManager.GAME_OVER)

    # --------------------------
    # Colisiones
    # --------------------------
    def check_coin_pickup(self):
        # Coin es un sprite; colisión player-coin
        if pygame.sprite.collide_rect(self.player, self.coin):
            self.score.add(1)
            self.coin.respawn()
            self.sounds.play("coin")

    def check_powerup_pickup(self):
        # Solo si el power-up está activo
        if not self.powerup.active:
            return

        if pygame.sprite.collide_rect(self.player, self.powerup):
            # Activar invencibilidad 3 segundos
            self.player.set_invincible(self.powerup.duration_ms)
            self.powerup.despawn()
            self.sounds.play("power")

    def check_player_hit(self):
        # Si el jugador está invencible, no pierde vida
        if self.player.is_invincible():
            return

        if pygame.sprite.collide_rect(self.enemy, self.player):
            self.player.lives.lose_one()
            self.player.respawn()
            self.enemy.respawn()
            self.coin.respawn()

            # Al recibir golpe, también quitamos el power-up (evita situaciones raras)
            self.powerup.despawn()
            self.sounds.play("hit")

    # --------------------------
    # Draw
    # --------------------------
    def draw(self):
        self.screen.fill((20, 20, 30))

        if self.state.is_menu():
            self.draw_menu()

        elif self.state.is_playing():
            # Dibujamos todo, pero el power-up solo si está activo
            self.screen.fill((20, 20, 30))

            # Dibujar sprites manualmente para controlar el power-up activo
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.enemy.image, self.enemy.rect)
            self.screen.blit(self.coin.image, self.coin.rect)

            if self.powerup.active:
                self.screen.blit(self.powerup.image, self.powerup.rect)

            # HUD
            self.score.draw(self.screen)
            self.player.lives.draw(self.screen)
            self.draw_hud_hints()

        elif self.state.is_paused():
            # Mostramos la escena "congelada"
            self.screen.blit(self.player.image, self.player.rect)
            if self.enemy:
                self.screen.blit(self.enemy.image, self.enemy.rect)
            self.screen.blit(self.coin.image, self.coin.rect)
            if self.powerup.active:
                self.screen.blit(self.powerup.image, self.powerup.rect)

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
        inv_state = "SÍ" if self.player.is_invincible() else "NO"

        hint0 = self.font.render(f"Mute: {mute_state} (M) | Invencible: {inv_state}", True, (200, 200, 200))
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
