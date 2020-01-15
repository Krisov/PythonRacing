from math import sin, cos, atan, radians
import pygame
from Ground import Ground
class Player:
	
	def __init__(s, G, x = 1500, y = 100, speed = 6):
		
		s.x = x
		s.y = y
		s.speed = speed
		s.G = G

		s.vx = 0
		s.vy = 0

		s.ax = 0
		s.ay = 5

		s.w = 40
		s.h = 40

		s.onFloor = False
		s.jump = False
		#s.dash = False
		s.stomp = False

		s.g = 1.6

	def runLeft(s):
		s.ax = -s.speed
		if s.onFloor == False:
			s.ax *= 0.3
		elif s.G.angle < 0:
			s.ax *= cos(s.G.angle)
			s.ax -= s.g * sin(s.G.angle)
	
	def runRight(s):
			s.ax = s.speed
			if s.onFloor == False:
				s.ax *= 0.3
			elif s.G.angle > 0:
				s.ax *= cos(s.G.angle)
				s.ax -= s.g * sin(s.G.angle)

	def runStop(s):
		s.ax = 0
		if s.onFloor == True:
			s.ax -= s.g * sin(s.G.angle)
					
	def jumpFloor(s, key1, key2, count):
		if s.onFloor:
			if key1 == True:
				s.angle2 = s.G.angle - radians(15)
			elif key2 == True:
				s.angle2 = s.G.angle + radians(15)
			else:
				s.angle2 = s.G.angle
			s.jumpForce = 30 * s.g
			s.vy =  -s.jumpForce * cos(s.angle2)
			s.vx -=  s.jumpForce * sin(s.angle2)
			s.onFloor = False
			s.jump = True
		elif s.vy < 0 and s.jump == True:
			s.vy -=  11 - count


	def glide(s):
		if s.vy >= 0:
			s.vy -= s.vy/2

	def stamp(s):
		if s.stomp == False:
			if s.vy < 0:
				s.vy = 10
			else:
				s.vy += 10
			s.stomp == True			

	def checkStaticFriction(s):
		if s.onFloor == True:
			if abs(s.ax) < 0.9:
				s.ax = 0

	def countX(s):
		s.vx += s.ax
		if s.onFloor == True:
			s.vx -= s.g *cos(s.G.angle)*s.vx/15
		s.vx -= s.vx/20

		s.x += s.vx

	def countY(s):
		if s.vy <= 0:
			s.vy += s.ay * s.g * 0.8
		else:
			s.vy += s.ay * s.g * 0.5
		s.y += s.vy

	def checkFloor(s, heigth):
		if s.y > heigth:
			if s.onFloor == False:
				s.vx -= s.vy * sin(s.G.angle)
				if s.vy > 80 and abs(s.G.angle) < 15:
					s.vy = -s.vy * 0.6 * cos(s.G.angle)
				else:
					if abs(s.G.angle) > 45:
						s.vy = sin(s.G.angle)
					else:
						s.vy = 0
					s.onFloor = True
					s.jump = False
					s.stomp = False
			s.y = heigth

	def render(s, win):
		pygame.draw.rect(win, (0, 255, 0), (s.x, s.y, s.w, s.h))