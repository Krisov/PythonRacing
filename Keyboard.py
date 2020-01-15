import pygame


class Keyboard:

    def __init__(self):
        self.a = False
        self.aCount = 0

    def check(self, car):

        wheel = car.WF
        key = pygame.key.get_pressed()

        if key[pygame.K_k]:
            wheel.jump()

        if key[pygame.K_j]:
            car.WB.jump()

        if key[pygame.K_r]:
            car.restart()

        if key[pygame.K_LEFT]:
            wheel.left()

        if key[pygame.K_RIGHT]:
            wheel.right()

        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            wheel.stop()

