"""
                                           ___       ________   ___
                                          / / |     / /   \  \ /  /
                                     __  / /| | /| / / /| |\    /
                                    / /_/ / | |/ |/ / ___ |/  /
 ___________________________________\____/  |__/|__/_/  |_/__/___________________________________
/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/_____/____/


Ruby
    Created by: Jordan Waite
    September, 2018

Things to try and to add:
                    - Add new enemies.
                    - Implement power ups or different weapons.
                    - Enemies shoot back
"""
from media import *
import sprites
import sys
import levels

# Once instance of the game is created in the main function. The game class controls the game loop, events,
# updates all sprites, draws to the window, handles the moving background, start/game over/ pause screen,
# Changes to some settings can be made in the game init or in the settings module.


class Game:
    def __init__(self):
        pg.init()
        self.running = False
        self.start = True
        self.game_over = True
        self.pause = False
        self.music = ''

        self.ALL_SPRITES = pg.sprite.Group()
        self.ALL_SHOTS = pg.sprite.Group()
        self.ALL_ENEMY = pg.sprite.Group()

        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.player = sprites.Player()
        self.ALL_SPRITES.add(self.player)
        self.bg_x = 0
        self.bg_y1 = -2200  # Pixel positions that allows the background to be seamless.
        self.bg_y2 = -5200
        self.score = 0
        self.level = 0
        self.last_shot = pg.time.get_ticks()
        self.shot_delay = 150
        self.lives = 3

    def run(self):
        self.start_screen()

        while self.running:
            self.events()
            self.update()
            self.draw()
            CLOCK.tick(FPS)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.display.quit()
                pg.quit()
                sys.exit(0)
            if event.type == pg.KEYDOWN:
                if self.running and not self.game_over:
                    if event.key == pg.K_ESCAPE:
                        self.pause = True
                        self.pause_screen()

                if event.key == pg.K_q:
                    self.level += 1
                    arr = levels.level(self.level)
                    for i in range(len(arr)):
                        for j in range(len(arr[0])):
                            if arr[i][j] == 1:
                                x = j
                                y = i
                                enemy = sprites.Enemy(x * (WIDTH // len(arr[0])), y * len(arr) - 11 * HEIGHT)
                                self.ALL_ENEMY.add(enemy)
                                self.ALL_SPRITES.add(enemy)

        keystate = pg.key.get_pressed()
        if keystate[pg.K_SPACE] and not self.pause:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.shot_delay:
                self.last_shot = now
                shot = self.player.shoot()
                self.ALL_SPRITES.add(shot)
                self.ALL_SHOTS.add(shot)
        return True

    def update(self):
        self.ALL_SPRITES.update()

        hit_player = pg.sprite.spritecollide(self.player, self.ALL_ENEMY, True)
        for hit in hit_player:
            expl = sprites.Explosion(hit.rect.center, 'sm')
            self.ALL_SPRITES.add(expl)
            self.lives = sprites.Player.lives(self.player, 'down')
            if self.lives <= 0:
                self.ALL_SPRITES = pg.sprite.Group()
                self.ALL_SHOTS = pg.sprite.Group()
                self.ALL_ENEMY = pg.sprite.Group()
                self.game_over = True
                self.game_over_screen()

        hit_enemy = pg.sprite.groupcollide(self.ALL_SHOTS, self.ALL_ENEMY, True, True)
        for hit in hit_enemy:
            expl = sprites.Explosion(hit.rect.center, 'lg')
            self.ALL_SPRITES.add(expl)
            sprites.Enemy.kill_enemy(hit)
            self.score += 100

    def draw(self):
        self.background()
        self.ALL_SPRITES.draw(self.window)
        draw_text(self.score, 50, WIDTH // 2 - 30, 20)

        self.life = pg.Surface((self.lives * (WIDTH // 3), 15))
        life_perc = sprites.Player.life_get(self.player)
        if self.lives == 1:
            self.life.fill(RED_DARK)
            self.window.blit(self.life, (0, 0))
            draw_text('|', 25, WIDTH // 3 - 2, -2)
            draw_text(life_perc, 25, 90, 0)
            draw_text('HEALTH:', 25, 10, 0)
        elif self.lives == 2:
            self.life.fill(ORANGE)
            self.window.blit(self.life, (0, 0))
            draw_text('|', 25, 2 * (WIDTH // 3) - 2, -2)
            draw_text(life_perc, 25, 90, 0)
            draw_text('HEALTH:', 25, 10, 0)
        elif self.lives == 3:
            self.life.fill(GREEN_DARK)
            self.window.blit(self.life, (0, 0))
            draw_text('HEALTH:', 25, 10, 0)
            draw_text(life_perc, 25, 90, 0)

        pg.display.flip()

    def background(self):
        window.blit(img_bg_game, (self.bg_x, self.bg_y1))
        window.blit(img_bg_game, (self.bg_x, self.bg_y2))

        if self.bg_y1 > HEIGHT:
            self.bg_y1 = -5200
        if self.bg_y2 > HEIGHT:
            self.bg_y2 = -5200

        # Controls the speed of the scrolling.
        self.bg_y1 += BG_SCROLL
        self.bg_y2 += BG_SCROLL

    def start_screen(self):
        self.window.blit(img_bg_start, (0, 0))
        self.window.blit(img_title, (WIDTH // 2 - 102, 100))
        self.window.blit(img_jordan, (10, HEIGHT - 50))

        if self.music == 'main.wav':
            print('pass')
        else:
            self.music = music_play('main.wav')

        while self.start:
            self.start = self.events()
            self.button(img_play, img_play2, WIDTH // 2 - 50, 220, 'play')
            self.button(img_exit, img_exit2, WIDTH // 2 - 50, 280, 'exit')
            pg.display.flip()

    def game_over_screen(self):
        self.window.blit(img_bg_over, (0, 0))
        self.window.blit(img_title, (0, 0))
        self.window.blit(img_over, (WIDTH // 2 - 245, HEIGHT // 2 - 100))
        draw_text(self.score, 50, WIDTH // 2 - 30, 20)
        pg.sprite.Group.empty(self.ALL_ENEMY)

        while self.game_over:
            self.game_over = self.events()
            self.button(img_playagain, img_playagain2, WIDTH // 2 - 121, 480, 'play')
            self.button(img_exit, img_exit2, WIDTH // 2 - 50, 540, 'exit')
            pg.display.flip()

        self.game_over = False
        self.score = 0
        self.level = 0

        if self.running:
            main()

    def pause_screen(self):
        self.window.blit(img_title, (0, 0))
        self.window.blit(img_pause, (WIDTH // 2 - 113, HEIGHT // 2 - 100))
        while self.pause:
            self.game_over = self.events()
            self.button(img_play, img_play2, WIDTH // 2 - 50, 480, 'play')
            self.button(img_exit, img_exit2, WIDTH // 2 - 50, 540, 'exit')
            pg.display.flip()

    def button(self, img_1, img_2, but1_x, but1_y, action):
        but = self.window.blit(img_1, (but1_x, but1_y))
        click = pg.mouse.get_pressed()
        if but.collidepoint(pg.mouse.get_pos()):
            self.window.blit(img_2, (but1_x, but1_y))
            if click[0] == 1:
                if action == 'play':
                    self.start = False
                    self.game_over = False
                    self.pause = False
                    self.running = True
                if action == 'exit':
                    pg.display.quit()
                    pg.quit()
                    sys.exit(0)


def main():
    g = Game()
    g.run()


if __name__ == '__main__':
    main()
