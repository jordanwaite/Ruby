from main import *
import random


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.init()
        pg.sprite.Sprite.__init__(self)
        self.image = img_player
        self.speedx = 0
        self.speedy = 0
        self.play_speed = PLAY_SPEED
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.lives = 3

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.play_speed = PLAY_SPEED
        keystate = pg.key.get_pressed()

        # Player controls input detection.
        if keystate[pg.K_LEFT]:
            self.speedx = -self.play_speed
        if keystate[pg.K_RIGHT]:
            self.speedx = self.play_speed
        if keystate[pg.K_UP]:
            self.speedy = -self.play_speed
        if keystate[pg.K_DOWN]:
            self.speedy = self.play_speed

        # Keeps the player in the game window.
        if self.rect.right > WIDTH - 2:
            self.rect.right = WIDTH - 2
        if self.rect.left < 2:
            self.rect.left = 2
        if self.rect.top < 2:
            self.rect.top = 2
        if self.rect.bottom > HEIGHT - 2:
            self.rect.bottom = HEIGHT - 2

        # Moves the player
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def lives(self, lives):
        if lives == 'down':
            self.lives -= 1
            return self.lives
        elif lives == 'up':
            self.lives += 1
            return self.lives
        return self.lives

    def life_get(self):
        if self.lives == 3:
            return '100%'
        if self.lives == 2:
            return '66%'
        if self.lives == 1:
            return '33%'
        return 'HEALTH ERROR'

    def shoot(self):
        missile = Missile(self.rect.centerx, self.rect.top)
        sound_play('laser.wav')
        return missile


class Missile(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((6, 15))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -MISSILE_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = img_enemy_ship
        self.rect = self.image.get_rect()
        self.speedx = random.randint(-1, 1)
        self.speedy = ENEMY_SPEED
        self.rect.left = x
        self.rect.bottom = y

    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.kill()

        if self.rect.top > 0:
            self.rect.x += self.speedx

    def kill_enemy(self):
        self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explo_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explo_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explo_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
