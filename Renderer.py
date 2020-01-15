import pygame


class Renderer:

    def __init__(self, width, height):

        pygame.init()
        pygame.display.set_caption("Game Window")
        self.window = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.scale = 0.5
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def clearWindow(self):
        self.window.fill((0, 0, 0))

    def updateWindow(self):
        pygame.display.update()

    def getDisplayPosition(self, x, y):
        return x * self.scale + self.x, y * self.scale + self.y

    def delay(self, milis):
        pygame.time.delay(milis)

    def lookAt(self, x, y):
        a = self.getDisplayPosition(x, y)

        centerX = self.x + self.width * 0.5
        centerY = self.y + self.height * 0.5

        self.x = centerX - a[0]
        self.y = centerY - a[1]

    def displayText(self, msg, x, y):
        text = self.font.render(msg, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.window.blit(text, textRect)
