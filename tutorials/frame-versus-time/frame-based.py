# Example of frame-based animation.
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
# Other constants, not really for playing with.
WIDTH = 800
HEIGHT = 600
RADIUS = 100
SPEED = 4 # pixels/frame

PG.init()
screen = PD.set_mode((WIDTH, HEIGHT), PG.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

circles = []
for _ in range(NUM_CIRCLES):
    circle = U.Circle(WIDTH, HEIGHT, RADIUS, SPEED)
    circles.append(circle)

clock = PT.Clock()
font = PF.Font(None, 24)

while True:
    clock.tick()

    screen.fill(U.BLACK)

    for c in circles:
        c.draw(screen)

    surf = font.render("frames/second: %3.2f" % (clock.get_fps()), True, U.WHITE)
    screen.blit(surf, (24, 24))

    PD.flip()

    for c in circles:
        c.update()

    for event in PE.get():
        if event.type == PG.QUIT:
            exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            exit()
