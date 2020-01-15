from Physics import Point, Vector
from math import pi, sin
import pygame


class NewGround:

    def __init__(self):
        self.y = 0

    def getHeight(self, x):
        return self.y + 100*sin(x*0.005) + 40*sin(x*0.006+2)
        # return 0

    def getGroundSurface(self, x):
        s = Point(x - 1, self.getHeight(x - 1))
        p = Point(x + 1, self.getHeight(x + 1))
        return s.getVectorToPoint(p)

    def getGroundAngle(self, x):
        return self.getGroundSurface(x).angle

    def getNormalAngle(self, x):
        return self.getGroundAngle(x) - pi * 0.5

    def render(self, renderer, min, max, step):

        for x1 in range(int(min), int(max), step):
            x2 = x1 + step
            y1 = self.getHeight(x1)
            y2 = self.getHeight(x2)

            a = renderer.getDisplayPosition(x1, y1)
            b = renderer.getDisplayPosition(x2, y2)

            pygame.draw.line(renderer.window, (0, 255, 0), a, b, 8)
