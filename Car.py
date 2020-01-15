import pygame
from math import pi


class Car:

    def __init__(self, WB, WF):

        self.WB = WB
        self.WF = WF
        self.x = 0
        self.y = 0
        self.angle = 0
        self.img = pygame.image.load('car.png')
        self.radianToDegree = 180 / pi

    def restart(self):
        self.WB.x = self.x - 64
        self.WF.x = self.x + 64
        self.WB.y = self.y - 200
        self.WF.y = self.y - 200

    def render(self, renderer):

        img = pygame.transform.rotozoom(self.img, -self.angle * self.radianToDegree, renderer.scale)

        a = renderer.getDisplayPosition(self.x, self.y)
        x = a[0]
        y = a[1]

        w = img.get_rect().width * 0.5
        h = img.get_rect().height * 0.5

        renderer.window.blit(img, (int(x - w), int(y - h)))
