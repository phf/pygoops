# Example of time-based animation with minimum intervals.
#
# Peter H. Froehlich <phf@acm.org>
# Johns Hopkins Gaming Lab <http://gaming.jhu.edu/>
#
# Released into the public domain.

import util as U
import sys as S

import pygame as PG
import pygame.display as PD
import pygame.event as PE
import pygame.font as PF
import pygame.time as PT

# See the README file for the following parameters.
NUM_CIRCLES = int(S.argv[1])
TARGET_FPS = int(S.argv[2])
INTERVAL = float(S.argv[3])
# Other constants, not really for playing with.
WIDTH = 800
HEIGHT = 600
RADIUS = 100
SPEED = 4*TARGET_FPS # pixels/second

PG.init()
screen = PD.set_mode((WIDTH, HEIGHT), PG.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

circles = []
for _ in range(NUM_CIRCLES):
    circle = U.Circle(WIDTH, HEIGHT, RADIUS, SPEED)
    circles.append(circle)

clock = PT.Clock()
font = PF.Font(None, 24)

current_time = PT.get_ticks()
updates = 0

while True:
    new_time = PT.get_ticks()
    frame_time = (new_time - current_time) / 1000.0
    current_time = new_time

    clock.tick()

    screen.fill(U.BLACK)

    for c in circles:
        c.draw(screen)

    surf = font.render("frames/second: %3.4f" % (clock.get_fps()), True, U.WHITE)
    screen.blit(surf, (24, 24))
    surf = font.render("seconds/frame: %3.4f" % (frame_time), True, U.WHITE)
    screen.blit(surf, (24, 48))
    surf = font.render("updates/frame: %3.4f" % (updates), True, U.WHITE)
    screen.blit(surf, (24, 72))

    PD.flip()

    updates = 0
    while frame_time > 0.0:
        delta = min(frame_time, INTERVAL)
        for c in circles:
            c.update(delta)
        frame_time -= delta
        updates += 1

    for event in PE.get():
        if event.type == PG.QUIT:
            exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            exit()
