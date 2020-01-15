from math import atan

class Ground:

	def __init__(s):
		s.function = [-0.001, 2.15, -200]
		#s.function = [-0.6, 1100]
		s.countDiff()

		s.angle = 0
		s.heigth = 0

	def countDiff(s):
		s.diff = []
		for i, part in enumerate(s.function[:-1:]):
			temp = part * (len(s.function) - 1 - i)
			s.diff.append(temp)

	def countAngle(s, x):
		s.angle = 0
		for i, part in enumerate(reversed(s.diff)):
			s.angle += part * (x ** i)
		s.angle = -atan(s.angle)
		#return s.angle

	def countHeigth(s, x):
		s.heigth = 0
		for i, part in enumerate(reversed(s.function)):
			s.heigth += part * (x ** i)
		#return s.heigth