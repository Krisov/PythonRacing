from math import sin, cos, atan, radians, pi, acos, asin, sqrt, copysign
import pygame
from Physics import Point, Vector, air
from NewGround import NewGround
import os


class Wheel:

    def __init__(self, new_ground, x, y):
        self.new_ground = new_ground
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.g = 1
        self.fly = True
        self.engineForce = 2.5
        self.move_right = False
        self.move_left = False
        self.rotation = 0
        self.last_rotation = 0
        self.prev_x = x
        self.prev_y = y

        self.img = pygame.image.load('player64_rot.png')

    def getHeight(self, x):
        # self.ground.countHeigth(x)
        # return self.ground.height
        return self.new_ground.getHeight(x)

    def getGroundVector(self, x):
        # self.ground.countAngle(x)
        # return -self.ground.angle
        return self.new_ground.getGroundAngle(x)

    def getGroundNormal(self, x):
        # self.ground.countAngle(x)
        # return -self.ground.angle - pi * 0.5
        return self.new_ground.getNormalAngle(x)

    def right(self):
        self.move_left = False
        self.move_right = True

    def left(self):
        self.move_right = False
        self.move_left = True

    def stop(self):
        self.move_right = False
        self.move_left = False
        self.ax = 0
        self.ay = 0

    def jump(self):
        self.vy -= 10

    def old_redirect_force(self, x, y, ground_angle, bounce):

        sinus = sin(ground_angle)
        cosinus = cos(ground_angle)

        y_from_y = sinus * sinus * y
        x_from_y = sinus * cosinus * y
        force_from_y = cosinus * y

        y_from_x = sinus * cosinus * x
        x_from_x = cosinus * cosinus * x
        force_from_x = sinus * x

        out = sqrt(force_from_x * force_from_x + force_from_y * force_from_y)
        inp = sqrt(y * y + x * x)
        if inp == 0:
            inp = 1
        mul = (out / inp)

        new_x = x_from_x + x_from_y
        new_y = y_from_x + y_from_y

        # print("mul: " + str(mul))
        # print("fx: " + str(force_from_x))
        if bounce:
            normal = ground_angle - pi * 0.5
            new_x += cos(normal) * force_from_x * 0.8
            new_y += sin(normal) * force_from_y * 0.8

        force_lost = out

        return new_x, new_y, force_lost, mul

    def show_v(self, N):
        print("N: " + str(N) + "vx: " + str(self.vx) + ", vy: " + str(self.vy) + ", ax: " + str(self.ax) + ", ay: " + str(self.ay))

    def distance(self, W):

        s = Point(self.x, self.y)
        p = Point(W.x, W.y)

        vec = s.getVectorToPoint(p)
        fromCenter = Vector(angle=vec.angle, value=64)
        center = s.getPointBetween(p)

        x = fromCenter.getX()
        y = fromCenter.getY()

        self.x = center.x - x
        self.y = center.y - y
        W.x = center.x + x
        W.y = center.y + y

        self.ax = W.ax
        self.ay = W.ay

        '''
        x = self.x - W.x
        y = self.y - W.y
        f = sqrt(pow(x, 2)+pow(y, 2))
        angle = 0
        if f != 0:
            if x > 0:
                angle = asin(y / f)
            else:
                angle = -acos(x / f)

        cx = self.x - x*0.5
        cy = self.y - y*0.5

        dst = 64

        W.x = cx - cos(angle) * dst
        W.y = cy - sin(angle) * dst

        self.x = cx + cos(angle) * dst
        self.y = cy + sin(angle) * dst

        x = self.x - W.x
        y = self.y - W.y
        f2 = sqrt(pow(x, 2) + pow(y, 2))
        '''

        # self.ax = W.ax
        # self.ay = W.ay

        # vx = (self.vx + W.vx)*0.5
        # vy = (self.vy + W.vy)*0.5
        # self.vx = vx
        # self.vy = vy
        # W.vx = vx
        # W.vy = vy

        # avg_vx = self.vx - (self.vx - W.vx) * 0.5
        # avg_vy = self.vy - (self.vy - W.vy) * 0.5

        # self.vx = avg_vx
        # self.vy = avg_vy
        # W.vx = avg_vx
        # W.vy = avg_vy

        # print("dst: "+str(f) + " : " + str(f2) + " : " + str(angle) + " : " + str(angle))

        # return cx, cy, angle
        return center.x, center.y, vec.angle

    def setLastRotation(self):
        if not self.fly:
            sign = 1
            sign = copysign(sign, self.prev_x - self.x)
            self.last_rotation = sign * sqrt(pow(self.prev_x - self.x, 2) + pow(self.prev_y - self.y, 2))

    def update(self, t):

        a = air(self.vx, self.vy)

        vx = self.vx * t + (self.ax + a.getX()) * t * t * 0.5
        vy = self.vy * t + (self.ay + a.getY() + self.g) * t * t * 0.5

        x = self.x + vx
        y = self.y + vy

        normal_left = self.getGroundNormal(x - 32)
        normal_right = self.getGroundNormal(x + 32)
        if abs(normal_left) > abs(normal_right):
            normal = normal_left
        else:
            normal = normal_right
        y2 = y - 32 * sin(normal)
        x2 = x - 32 * cos(normal)
        h2 = self.getHeight(x2)

        if h2 - 0.5 < y2:
            y += (h2 - y2)

            surface = self.new_ground.getGroundSurface(x)
            ground_angle = surface.angle

            if self.move_right:
                if ground_angle < 0.4:
                    self.ax = cos(self.getGroundVector(self.x)) * self.engineForce
                else:
                    self.ay = sin(self.getGroundVector(self.x)) * self.engineForce
            if self.move_left:
                if ground_angle > -0.4:
                    self.ax = -cos(self.getGroundVector(self.x)) * self.engineForce
                else:
                    self.ay = -sin(self.getGroundVector(self.x)) * self.engineForce

            v = Vector(vx, vy)
            new_v = v.hit_surface(surface, self.fly, 0.4)
            self.vx = new_v.getX()  # * 0.99
            self.vy = new_v.getY()  # * 0.99

            if abs(self.vx) < 0.1:
                self.vx = 0

            if abs(self.vy) < 0.1:
                self.vy = 0

            # print("ax: " + str(self.ax) + ", ay: " + str(self.ay) + ", vx: " + str(self.vx) + ", vy: " + str(self.vy))
            # print(self.vy)
            # print("vx_from_y: " + str(vx_from_y)+ ", vx: " + str(self.vx) + ", ax: "+ str(self.ax))
            # print("ax: " + str(self.ax) + ", ay: " + str(self.ay), ", angle: " + str(ground_angle))

            # self.setLastRotation(Point(self.x, self.y), Point(x, y))

            self.fly = False
        else:
            self.fly = True
            self.vx = vx
            self.vy = vy

        self.rotation += self.last_rotation
        if self.rotation > 2 * pi:
            self.rotation -= 2 * pi

        self.prev_x = self.x
        self.prev_y = self.y
        self.x = x
        self.y = y

        # print("vx: " + str(self.vx) + ", vy: " + str(self.vy))
        # print(self.fly)

        '''
        agy = self.ay + self.g
        ay = agy * t * t * 0.5

        move_x = self.vx * t + self.ax
        move_y = self.vy * t + ay
        x = self.x + move_x
        y = self.y + move_y

        self.ground.countHeigth(self.x)
        h1 = self.ground.height
        self.ground.countHeigth(x)
        h2 = self.ground.height
        # hm = (h1 + h2) * 0.5
        # xm = (x + self.x) * 0.5

        # diff_x = x - self.x
        # diff_y = h2 - h1

        # os.system('cls')
        # print("ax: " + str(self.ax) + ", ay: " + str(self.ay))
        print("vx: " + str(self.vx) + ", vy: " + str(self.vy))
        if self.ay < 0 and self.stick == True:
            self.stick = False
            print("take off")

        if h2 - 0.5 > y:  # above ground
            self.y = y
            self.vy = move_y
            self.x = x
            self.vx = move_x
            # print("ax: " + str(self.ax) + ", ay: " + str(self.ay))

        elif (abs(move_x) > 1 or abs(move_y) > 1) and self.stick == False: # bounce
            print("bounce")
            self.stick = True
            normal = self.getGroundNormal(self.x)
            ground_vector = self.getGroundVector(self.x)

            # /|\ -pi/2 rad, oś "minus" Y
            #  |
            #  |
            #  |-----------> 0 rad, oś X
            #  |
            #  |
            # \|/ pi/2 rad, oś Y

            force = sqrt(move_x * move_x + move_y * move_y)
            force_angle = -acos(move_x / force)
            angle_difference = abs(force_angle - normal)
            # force *= 0.4  # angle_difference*0.5

            angle = normal - (force_angle - normal)
            # angle = normal + pi*0.25

            # if abs(ground_vector - angle) < 0.4:
            #    angle -= 0.1
            # print("slide: " + str(ground_vector -angle))

            # print("move x: " + str(move_x) + ", move y: " + str(move_y) + ", force: " + str(force))
            # print("f: "+str(force_angle)+", n: "+str(normal)+", a: "+str(angle))

            self.vy = force * 0.5 * sin(angle)
            self.vx = force * 0.5 * cos(angle)

            self.y = h2
            self.x = x

        else: # stick to ground

            self.vy *= 0
            self.vx *= 0
            self.y = h2
            self.x = x
        '''

    def render(self, renderer):

        img = pygame.transform.rotozoom(self.img, self.rotation, renderer.scale)

        a = renderer.getDisplayPosition(self.x, self.y)
        x = a[0]
        y = a[1]

        w = img.get_rect().width * 0.5
        h = img.get_rect().height * 0.5

        renderer.window.blit(img, (int(x - w), int(y - h)))
