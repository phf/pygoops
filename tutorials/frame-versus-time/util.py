import random as R
import pygame.draw as PDR

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def random_color():
    return tuple([R.randint(0, 245) + 10 for _ in range(3)])

def random_place(outer, inner):
    return outer/2 + R.randint(-outer/2+inner, outer/2-inner)

class Circle(object):
    def __init__(self, width, height, radius, speed):
        self.color = random_color()
        self.radius = radius
        self.maxx = width - radius
        self.maxy = height - radius
        self.x = random_place(width, radius)
        self.y = random_place(height, radius)
        self.vx = speed
        if R.randint(0, 1) == 1:
            self.vx = -self.vx
        self.vy = speed
        if R.randint(0, 1) == 1:
            self.vy = -self.vy

    def draw(self, surface):
        PDR.circle(surface, self.color, (int(self.x), int(self.y)), self.radius, 0)

    def update(self, dt=1):
        # this collision code is intentionally flawed: if an
        # objects moves "too far" off the screen, we don't
        # even try to bring it back; this simulates how in-game
        # sprite-sprite collisions would fail more accurately
        if self.x < self.radius and self.x > -self.radius:
            self.x = self.radius
            self.vx = -self.vx
        if self.x > self.maxx and self.x < self.maxx + self.radius:
            self.x = self.maxx
            self.vx = -self.vx
        if self.y < self.radius and self.y > -self.radius:
            self.y = self.radius
            self.vy = -self.vy
        if self.y > self.maxy and self.y < self.maxy + self.radius:
            self.y = self.maxy
            self.vy = -self.vy
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt

    def correct_update(self, dt=1):
        # this one is perfect, it never "goes wrong" as in the
        # objects will never fly totally off the screen; this
        # is, however, unrealistic in terms of actual in-game
        # sprite-sprite collisions, you would not be able to
        # handle them this way
        if self.x < self.radius:
            self.x = self.radius
            self.vx = -self.vx
        if self.x > self.maxx:
            self.x = self.maxx
            self.vx = -self.vx
        if self.y < self.radius:
            self.y = self.radius
            self.vy = -self.vy
        if self.y > self.maxy:
            self.y = self.maxy
            self.vy = -self.vy
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt

    def original_update(self, dt=1):
        # this one was unintentionally flawed because it tries
        # to "move circles back" by a time-dependent amount; if
        # times vary too much between updates, this can lead to
        # "collision jitter" at the boundaries
        if self.x < self.radius or self.x > self.maxx:
            self.vx = -self.vx
            self.x = self.x + self.vx*dt
        if self.y < self.radius or self.y > self.maxy:
            self.vy = -self.vy
            self.y = self.y + self.vy*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
