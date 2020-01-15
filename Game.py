import pygame
from Keyboard import Keyboard
from Renderer import Renderer
from Wheel import Wheel
from Car import Car
from NewGround import NewGround
from Physics import Vector, Point, Function


# init

R = Renderer(1000, 500)
K = Keyboard()
NG = NewGround()
ground_display = 500/R.scale

WF = Wheel(NG, 128, -800)  # front wheel
WB = Wheel(NG, 0, -800)  # back wheel
C = Car(WB, WF)

run = True

# main loop

while run:
    R.delay(20)

    # event handle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        K.check(C)

    # engine update

    WF.update(1)
    WB.update(1)

    R.lookAt(WF.x, WF.y)

    c = WB.distance(WF)
    C.x = c[0]
    C.y = c[1]
    C.angle = c[2]

    WF.setLastRotation()
    WB.setLastRotation()

    # display update

    R.clearWindow()

    C.render(R)
    WF.render(R)
    WB.render(R)
    NG.render(R, WF.x - ground_display, WF.x + ground_display, 20)

    R.displayText("x: " + str(int(WF.x)), 100, 32)
    R.displayText("y: " + str(int(WF.y)), 100, 64)

    R.displayText("vx: " + str(int(WF.vx)), 300, 32)
    R.displayText("vy: " + str(int(WF.vy)), 300, 64)

    R.displayText("ax*100: " + str(int(WF.ax*100)), 500, 32)
    R.displayText("ay*100: " + str(int(WF.ay*100)), 500, 64)

    R.updateWindow()

# quit at the end

pygame.quit
