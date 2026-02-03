import pygame
import random
import os


# =========================================================
# Utilidades de rutas (evita problemas al ejecutar desde otro directorio)
# =========================================================
def asset_path(*parts):
    base = os.path.dirname(__file__)
    return os.path.join(base, "assets", *parts)


# =========================================================
# StateManager
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
# SoundManager: mute global + música
# =========================================================
class SoundManager:
    def __init__(self):
        self.enabled = False
        self.muted = False

        try:
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False

    def toggle_mute(self):
        self.muted = not self.muted
        if not self.enabled:
            return

        # Mute afecta a la música (y a futuros SFX si los añades)
        if self.muted:
            pygame.mixer.music.set_volume(0.0)
        else:
            pygame.mixer.music.set_volume(0.6)

    def start_music_loop(self, filepath, volume=0.6):
        if not self.enabled:
            return
        if not os.path.exists(filepath):
            return

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(0.0 if self.muted else volume)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
        except pygame.error:
            pass

    def stop_music(self):
        if not self.enabled:
            return
        pygame.mixer.music.stop()


# =========================================================
# HUD
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
# AnimatedSprite (base): corta una sprite sheet en frames y anima
# =========================================================
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet_path, frame_w, frame_h, rows, cols, scale=1, frame_time_ms=120, row_index=0):
        super().__init__()

        self.sheet = pygame.image.load(sheet_path).convert_alpha()

        self.frame_w = frame_w
        self.frame_h = frame_h
        self.rows = rows
        self.cols = cols

        self.scale = scale
        self.frame_time_ms = frame_time_ms

        # Guardamos frames por filas (lista de listas)
        self.frames_by_row = []
        for r in range(rows):
            row_frames = []
            for c in range(cols):
                frame = self.sheet.subsurface((c * frame_w, r * frame_h, frame_w, frame_h))
                if scale != 1:
                    frame = pygame.transform.scale(frame, (frame_w * scale, frame_h * scale))
                row_frames.append(frame)
            self.frames_by_row.append(row_frames)

        # Fila que se va a animar (por defecto 0)
        self.set_animation_row(row_index)

        self.last_frame_change_ms = pygame.time.get_ticks()

    def set_animation_row(self, row_index):
        self.row_index = row_index
        self.frames = self.frames_by_row[row_index]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # Si el rect ya existe (sprite en juego), conservamos posición
        if hasattr(self, "rect"):
            old_topleft = self.rect.topleft
            self.rect = self.image.get_rect()
            self.rect.topleft = old_topleft
        else:
            # Primera vez (constructor)
            self.rect = self.image.get_rect()



    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_change_ms >= self.frame_time_ms:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

            # mantener posición actual
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

            self.last_frame_change_ms = now


# =========================================================
# Player: animado + composición Lives + invencibilidad 3s
# =========================================================
class Player(AnimatedSprite):
    def __init__(self, x, y, lives_component):
        # Ajusta a tu sheet real:
        # - frame_w/frame_h: tamaño de cada frame en la sheet
        # - num_frames: nº de frames en una fila (horizontal)
        super().__init__(
            sheet_path=asset_path("player.png"),
            frame_w=41, frame_h=43,
            rows=4, cols=4,
            scale=2,
            frame_time_ms=120,
            row_index=0
        )


        self.rect.topleft = (x, y)
        self.spawn_pos = (x, y)

        self.speed = 5
        self.lives = lives_component

        self.invincible_until_ms = 0

    def respawn(self):
        self.rect.topleft = self.spawn_pos

    def set_invincible(self, duration_ms=3000):
        self.invincible_until_ms = pygame.time.get_ticks() + duration_ms

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until_ms

    def update(self, w, h):
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

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))

        # Animación: solo si se mueve (más “realista”)
        # Elegir fila de animación según dirección dominante
        new_row = self.row_index  # por defecto, mantenemos la actual

        if dx != 0 or dy != 0:
         if abs(dx) > abs(dy):
          new_row = 2 if dx > 0 else 1
         else:
          new_row = 0 if dy > 0 else 3

    # Solo cambiamos si es distinta
        if new_row != self.row_index:
         self.set_animation_row(new_row)

        self.animate()




# =========================================================
# Enemy base
# =========================================================
class Enemy(AnimatedSprite):
    def __init__(self, x, y, target_mode=None):
        super().__init__(
            sheet_path=asset_path("player.png"),
            frame_w=41, frame_h=43,
            rows=4, cols=4,
            scale=2,
            frame_time_ms=120,
            row_index=0
        )
        self.rect.topleft = (x, y)
        self.spawn_pos = (x, y)
        self.speed = 4
        self.target_mode = target_mode

    def respawn(self):
        self.rect.topleft = self.spawn_pos

    def keep_inside(self, w, h):
        self.rect.x = max(0, min(w - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(h - self.rect.height, self.rect.y))


class HumanEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, w, h, player=None, coin=None):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy
        self.keep_inside(w, h)

        if dx != 0 or dy != 0:
            self.animate()


class AutoEnemy(Enemy):
    def __init__(self, x, y, target_mode="PLAYER"):
        super().__init__(x, y, target_mode=target_mode)

    def set_target_mode(self, target_mode):
        self.target_mode = target_mode

    def update(self, w, h, player=None, coin=None):
        if self.target_mode == "COIN" and coin is not None:
            tx, ty = coin.rect.centerx, coin.rect.centery
        elif player is not None:
            tx, ty = player.rect.centerx, player.rect.centery
        else:
            return

        dx = 0
        dy = 0

        if self.rect.centerx < tx:
            dx = self.speed
        elif self.rect.centerx > tx:
            dx = -self.speed

        if self.rect.centery < ty:
            dy = self.speed
        elif self.rect.centery > ty:
            dy = -self.speed

        self.rect.x += dx
        self.rect.y += dy
        self.keep_inside(w, h)

        if dx != 0 or dy != 0:
            self.animate()


# =========================================================
# Coin: sprite con imagen
# =========================================================
class Coin(pygame.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()
        self.image = pygame.image.load(asset_path("coin.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.w = w
        self.h = h
        self.respawn()

    def respawn(self):
        self.rect.centerx = random.randint(20, self.w - 20)
        self.rect.centery = random.randint(20, self.h - 20)


# =========================================================
# PowerUp invencibilidad: imagen + aparece a intervalos
# =========================================================
class InvincibilityPowerUp(pygame.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()
        self.image = pygame.image.load(asset_path("powerup.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (28, 28))
        self.rect = self.image.get_rect()
        self.w = w
        self.h = h

        self.active = False
        self.spawned_at_ms = 0
        self.lifetime_ms = 6000
        self.duration_ms = 3000

    def spawn(self):
        self.rect.centerx = random.randint(20, self.w - 20)
        self.rect.centery = random.randint(20, self.h - 20)
        self.active = True
        self.spawned_at_ms = pygame.time.get_ticks()

    def despawn(self):
        self.active = False

    def update(self):
        if not self.active:
            return
        if pygame.time.get_ticks() - self.spawned_at_ms > self.lifetime_ms:
            self.despawn()


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
        pygame.display.set_caption("Recoge el punto - Versión 7 (animaciones + música)")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        self.state = StateManager()
        self.sounds = SoundManager()

        self.score = Score(self.font)
        lives_component = Lives(self.font, initial_lives=3)
        self.player = Player(x=100, y=self.height // 2, lives_component=lives_component)

        self.coin = Coin(self.width, self.height)
        self.powerup = InvincibilityPowerUp(self.width, self.height)

        self.enemy = None
        self.enemy_mode = None           # "HUMAN" / "AUTO"
        self.auto_target_mode = "PLAYER" # "PLAYER" / "COIN"

        # Gestión de spawn del power-up
        self.next_powerup_at_ms = 0
        self.schedule_next_powerup()

        # Música
        self.music_path = asset_path("music.mp3")
        self.music_playing = False

        self.running = True

    def schedule_next_powerup(self):
        now = pygame.time.get_ticks()
        self.next_powerup_at_ms = now + random.randint(4000, 9000)

    def maybe_spawn_powerup(self):
        if self.powerup.active:
            return
        if pygame.time.get_ticks() >= self.next_powerup_at_ms:
            self.powerup.spawn()
            self.schedule_next_powerup()

    def set_enemy_mode(self, mode):
        self.enemy_mode = mode
        ex = self.width - 140
        ey = self.height // 2

        if mode == "HUMAN":
            self.enemy = HumanEnemy(ex, ey)
        elif mode == "AUTO":
            self.enemy = AutoEnemy(ex, ey, target_mode=self.auto_target_mode)
        else:
            self.enemy = None

    def set_auto_target_mode(self, target_mode):
        self.auto_target_mode = target_mode
        if isinstance(self.enemy, AutoEnemy):
            self.enemy.set_target_mode(target_mode)

    def start_music_if_needed(self):
        # Iniciamos música al entrar en PLAYING
        if not self.music_playing:
            self.sounds.start_music_loop(self.music_path, volume=0.6)
            self.music_playing = True

    def stop_music_if_needed(self):
        if self.music_playing:
            self.sounds.stop_music()
            self.music_playing = False

    def start_game(self):
        self.score.reset()
        self.player.lives.reset()
        self.player.respawn()
        self.coin.respawn()

        if self.enemy is None:
            self.set_enemy_mode("HUMAN")
        self.enemy.respawn()

        self.powerup.despawn()
        self.schedule_next_powerup()

        self.state.set_state(StateManager.PLAYING)
        self.start_music_if_needed()

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
                            self.set_enemy_mode("AUTO")

                    if event.key == pygame.K_c:
                        self.set_auto_target_mode("COIN")
                        if self.enemy_mode == "AUTO":
                            self.set_enemy_mode("AUTO")

                    if event.key == pygame.K_RETURN:
                        self.start_game()

                elif self.state.is_playing():
                    if event.key == pygame.K_p:
                        self.state.set_state(StateManager.PAUSED)
                        # Música sigue sonando en pausa (típico); si prefieres, la paras aquí.
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)
                        self.stop_music_if_needed()

                elif self.state.is_paused():
                    if event.key == pygame.K_p:
                        self.state.set_state(StateManager.PLAYING)
                    if event.key == pygame.K_ESCAPE:
                        self.state.set_state(StateManager.MENU)
                        self.stop_music_if_needed()

                elif self.state.is_game_over():
                    if event.key == pygame.K_r:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.stop_music_if_needed()

    def update(self):
        if not self.state.is_playing():
            return

        self.maybe_spawn_powerup()
        self.powerup.update()

        self.player.update(self.width, self.height)
        self.enemy.update(self.width, self.height, player=self.player, coin=self.coin)

        self.check_coin_pickup()
        self.check_powerup_pickup()
        self.check_player_hit()

        if self.player.lives.is_dead():
            self.state.set_state(StateManager.GAME_OVER)
            self.stop_music_if_needed()

    def check_coin_pickup(self):
        if pygame.sprite.collide_rect(self.player, self.coin):
            self.score.add(1)
            self.coin.respawn()

    def check_powerup_pickup(self):
        if not self.powerup.active:
            return
        if pygame.sprite.collide_rect(self.player, self.powerup):
            self.player.set_invincible(3000)  # 3 segundos
            self.powerup.despawn()

    def check_player_hit(self):
        if self.player.is_invincible():
            return
        if pygame.sprite.collide_rect(self.enemy, self.player):
            self.player.lives.lose_one()
            self.player.respawn()
            self.enemy.respawn()
            self.coin.respawn()
            self.powerup.despawn()

    def draw(self):
        self.screen.fill((0, 0, 0))  # verde claro


        if self.state.is_menu():
            self.draw_menu()
        elif self.state.is_playing():
            self.draw_world()
            self.draw_hud()
        elif self.state.is_paused():
            self.draw_world()
            self.draw_hud()
            self.draw_pause_overlay()
        elif self.state.is_game_over():
            self.draw_game_over()

        pygame.display.flip()

    def draw_world(self):
        self.screen.blit(self.player.image, self.player.rect)
        if self.enemy:
            self.screen.blit(self.enemy.image, self.enemy.rect)
        self.screen.blit(self.coin.image, self.coin.rect)
        if self.powerup.active:
            self.screen.blit(self.powerup.image, self.powerup.rect)

    def draw_hud(self):
        self.score.draw(self.screen)
        self.player.lives.draw(self.screen)

        mute_state = "ON" if self.sounds.muted else "OFF"
        inv = "SÍ" if self.player.is_invincible() else "NO"
        txt = self.font.render(f"Mute: {mute_state} (M) | Invencible: {inv}", True, (200, 200, 200))
        self.screen.blit(txt, (10, self.height - 90))

        if self.enemy_mode == "HUMAN":
            mode = "Enemigo HUMANO (WASD)"
        else:
            target = "Jugador (J)" if self.auto_target_mode == "PLAYER" else "Moneda (C)"
            mode = f"Enemigo AUTO | Objetivo: {target}"
        txt2 = self.font.render(mode, True, (200, 200, 200))
        self.screen.blit(txt2, (10, self.height - 60))

        txt3 = self.font.render("Jugador: Flechas | P: Pausa | ESC: Menú", True, (200, 200, 200))
        self.screen.blit(txt3, (10, self.height - 30))

    def draw_pause_overlay(self):
        overlay = self.big_font.render("PAUSA", True, (240, 240, 240))
        self.screen.blit(overlay, (self.width // 2 - overlay.get_width() // 2, 220))

    def draw_menu(self):
        title = self.big_font.render("RECOGE EL PUNTO", True, (240, 240, 240))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 110))

        opt1 = self.font.render("1) Enemigo humano (WASD)", True, (220, 220, 220))
        opt2 = self.font.render("2) Enemigo automático", True, (220, 220, 220))
        self.screen.blit(opt1, (self.width // 2 - opt1.get_width() // 2, 240))
        self.screen.blit(opt2, (self.width // 2 - opt2.get_width() // 2, 280))

        optj = self.font.render("J) IA persigue al jugador", True, (220, 220, 220))
        optc = self.font.render("C) IA persigue la moneda", True, (220, 220, 220))
        self.screen.blit(optj, (self.width // 2 - optj.get_width() // 2, 340))
        self.screen.blit(optc, (self.width // 2 - optc.get_width() // 2, 380))

        selected_enemy = "Ninguno" if self.enemy_mode is None else self.enemy_mode
        selected_target = "Jugador" if self.auto_target_mode == "PLAYER" else "Moneda"
        info = self.font.render(f"Seleccionado: {selected_enemy} | Objetivo IA: {selected_target}", True, (255, 220, 60))
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 460))

        start = self.font.render("Enter: empezar (música comienza) | M: mute", True, (200, 200, 200))
        self.screen.blit(start, (self.width // 2 - start.get_width() // 2, 520))

    def draw_game_over(self):
        title = self.big_font.render("GAME OVER", True, (255, 120, 120))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 160))

        score = self.font.render(f"Puntuación final: {self.score.points}", True, (240, 240, 240))
        self.screen.blit(score, (self.width // 2 - score.get_width() // 2, 250))

        hint = self.font.render("R: reiniciar | ESC: salir | M: mute", True, (220, 220, 220))
        self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, 340))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        self.stop_music_if_needed()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
