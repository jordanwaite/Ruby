import os
from settings import *


# Loading all graphics.
pg.init()
pg.mixer.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
font_name = pg.font.match_font('arial')
pg.mixer.set_num_channels(3)


def music_play(music):
    project_folder = os.path.dirname(__file__)
    sound_folder = os.path.join(project_folder, 'sound')
    pg.mixer.music.load(os.path.join(sound_folder, music))
    pg.mixer.music.play(-1)
    return music


def sound_play(sound):
    project_folder = os.path.dirname(__file__)
    sound_folder = os.path.join(project_folder, 'sound')
    y = pg.mixer.Sound(os.path.join(sound_folder, sound))
    y.play()


def draw_text(text, size, x, y):
    font = pg.font.SysFont(font_name, size)
    text_surface = font.render(str(text), True, WHITE)
    window.blit(text_surface, (x, y))


def load_img(img_name, color_key):
    project_folder = os.path.dirname(__file__)
    img_folder = os.path.join(project_folder, 'img')
    img1 = pg.image.load(os.path.join(img_folder, img_name,)).convert()
    img1.set_colorkey(color_key)
    return img1


img_bg_start = load_img('bg_start.png', BLACK)
img_bg_game = load_img('bg_game.png', BLACK)
img_bg_over = load_img('bg_over.png', BLACK)
img_title = load_img('game_logo.png', BLACK)
img_jordan = load_img('jordan.png', BLACK)
img_over = load_img('game_over.png', BLACK)
img_pause = load_img('pause.png', BLACK)
img_player = load_img('player.png', BLACK)
img_enemy_ship = load_img('enemy.png', WHITE)
img_play = load_img('play_but.png', BLACK)
img_exit = load_img('exit_but.png', BLACK)
img_play2 = load_img('play_but2.png', BLACK)
img_exit2 = load_img('exit_but2.png', BLACK)
img_playagain = load_img('play_again.png', BLACK)
img_playagain2 = load_img('play_again2.png', BLACK)

img_bg_start = pg.transform.scale(img_bg_start, (WIDTH, HEIGHT))
img_bg_over = pg.transform.scale(img_bg_over, (WIDTH, HEIGHT))
img_player = pg.transform.scale(img_player, (40, 30))

explo_anim = {}
explo_anim['lg'] = []
explo_anim['sm'] = []
for i in range(8):
    filename = 'explo{}.png'.format(i)
    img = load_img(filename, BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    explo_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explo_anim['sm'].append(img_sm)
