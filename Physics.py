from math import sqrt, pi, sin, cos, asin, acos, copysign, exp


class Vector:

    def __init__(self, x=0.0, y=0.0, angle=0.0, value=0.0):

        self.value = 1
        self.angle = 0

        if value == 0:
            self.value = sqrt(x*x+y*y)
            if self.value != 0:
                self.angle = acos(x/self.value)
                self.angle = copysign(self.angle, asin(y/self.value))

        elif value < 0:
            self.value = -value
            if angle >= 0:
                self.angle = angle-pi
            else:
                self.angle = angle+pi
        else:
            self.angle = angle
            self.value = value

    def getDegree(self):
        return self.angle * 180/pi

    def getX(self):
        return cos(self.angle) * self.value

    def getY(self):
        return sin(self.angle) * self.value

    def getSum(self, vec):
        x = self.getX() + vec.getX()
        y = self.getY() + vec.getY()
        return Vector(x, y)

    def hit_surface(self, surface, bounce, bounceness=0.0):  # surface: vector, bounce: bool

        '''
        Sin = sin(surface.angle)
        Cos = cos(surface.angle)
        x = self.getX()
        y = self.getY()

        # v: vector.value
        y_from_y = Sin * Sin * y
        x_from_y = Sin * Cos * y
        v_from_y = Cos * y

        y_from_x = Sin * Cos * x
        x_from_x = Cos * Cos * x
        v_from_x = Sin * x

        new_x = x_from_x + x_from_y
        new_y = y_from_x + y_from_y

        if v_input == 0:
            v_input = 1
        mul = (v_lost / v_input)

        if bounce:
            normal = surface.angle - pi * 0.5
            new_x += cos(normal) * v_from_x * 0.8
            new_y += sin(normal) * v_from_y * 0.8

        return Point(new_x, new_y)
        '''

        angle = self.angle - surface.angle
        Sin = sin(angle)
        Cos = cos(angle)

        vec_input = self
        vec_bounce = Vector(angle=surface.angle - pi * 0.5, value=Sin * self.value * bounceness)
        vec_output = Vector(angle=surface.angle, value=Cos * self.value)

        # print("a: " + str(vec_input.angle) + " : " + str(vec_bounce.angle) + " : "
        # + str(vec_output.angle) + " : " + str(angle))
        # print("D: " + str(vec_input.getDegree()) + " : " + str(vec_bounce.getDegree()) + " : "
        # + str(vec_output.getDegree()) + " : " + str(angle))
        # print("v: " + str(vec_input.value) + " : " + str(vec_bounce.value) + " : "
        # + str(vec_output.value) + " : " + str(angle))

        if bounce:
            return vec_output.getSum(vec_bounce)
        return vec_output

    def show(self):
        print("value: " + str(self.value) + ", angle: " + str(self.angle))


class Point:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def getVectorToPoint(self, p):  # returns vector: self --> p
        x = p.x - self.x
        y = p.y - self.y
        return Vector(x, y)

    def getPointBetween(self, p):
        x = (p.x - self.x) * 0.5
        y = (p.y - self.y) * 0.5
        return Point(self.x + x, self.y + y)


class Function:

    def __init__(self, a):  # a0 + a1*x^1 + a2*x^2 + ...
        self.a = a
        # len(a) # size

    def getY(self, x):
        value = 0
        for i, a in enumerate(self.a):
            value += a * x ** i
        return value

    def getAngle(self, x):
        s = Point(x - 1, self.getY(x - 1))
        p = Point(x + 1, self.getY(x + 1))
        return s.getVectorToPoint(p).angle


def air(vx, vy):
    x = air_exp(vx)
    y = air_exp(vy)
    return Vector(x, y)


def air_exp(x):
    if x >= 0:
        a = -exp(x * 0.02)+1
    else:
        a = -(-exp(-x * 0.02)+1)
    return a
