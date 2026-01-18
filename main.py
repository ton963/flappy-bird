from pygame import *
from random import randint

init()
window_size = 1200, 640
window = display.set_mode(window_size)
clock = time.Clock()

player_rect = Rect(150, window_size[1]//2-100, 100, 100)

img_back = transform.scale(image.load("images/fon.png"), window_size)
img_player = transform.scale(image.load("images/flappy.png"), (player_rect.width, player_rect.height))
img_pipe_top = image.load("images/pipet.png")
img_pipe_bottom = image.load("images/pipeb.png")

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distanse=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_height = max(1, window_size[1] - (height + gap))
        bottom_pipe = Rect(start_x, height + gap, pipe_width, bottom_height)
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distanse
    return pipes

pipes = generate_pipes(150)
main_font = font.Font(None, 100)
score = 0
lose = False
y_vel = 2

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.blit(img_back, (0, 0))
    window.blit(img_player, (player_rect.x, player_rect.y))

    for i, pie in enumerate(pipes[:]):
        if not lose:
            pie.x -= 10

        if i % 2 == 0:
            scaled_pipe_top = transform.scale(img_pipe_top, (pie.width, pie.height))
            window.blit(scaled_pipe_top, (pie.x, pie.y))
        else:
            scaled_pipe_bottom = transform.scale(img_pipe_bottom, (pie.width, pie.height))
            window.blit(scaled_pipe_bottom, (pie.x, pie.y))

        if pie.x <= 200:
            pipes.remove(pie)
            score += 0.5

        if player_rect.colliderect(pie):
            lose = True

    if len(pipes) < 8:
        pipes += generate_pipes(150)

    score_text = main_font.render(f'{int(score)}', 1, 'black')
    center_text = window_size[0] // 2 - score_text.get_rect().w
    window.blit(score_text, (center_text, 40))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w] and not lose:
        player_rect.y -= 15
    if keys[K_s] and not lose:
        player_rect.y += 15
    if keys[K_r] and lose:
        lose = False
        score = 0
        pipes = generate_pipes(150)
        player_rect.y = window_size[1]//2-100
    if player_rect.y >= window_size[1] - player_rect.h:
        lose = True
        if lose:
            player_rect.y += y_vel
            y_vel *= 1.1
