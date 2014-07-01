__author__ = 'sil'

from swampy.TurtleWorld import*
import math

def square(t, length):
    for i in range(4):
        fd(t, length)
        lt(t)

def polygon(t, length, n):
    angle = 360.0/n
    for i in range(n):
        fd(t, length)
        lt(t, angle)

def circle(t, r):
    arc(t, r, 360.)

def arc(t, r, angle):
    length = 2
    n = int(2.*math.pi*r /length * angle / 360.)
    a = float(angle) / n
    for i in range(n):
        fd(t, length)
        lt(t, a)

def petal(t, radius, angle):
    arc(t, radius, angle)
    lt(t, 180 - angle)
    arc(t, radius, angle)

def flower(t, NumofPetal, PetalRadius, PetalAngle):
    angle_step = 360. / NumofPetal
    for i in range(NumofPetal):
        petal(t, PetalRadius, PetalAngle)
        lt(t, 180 - PetalAngle)
        lt(t, angle_step)

def pieTriangle(t, n, radius):
    """ Draw one piece of Pie by given Number(1/n) and Radius"""
    angle = 360. / n
    print "Sin:", math.sin(float(angle)/2./180*math.pi)
    length = 2.*radius*math.sin(float(angle)/2./180*math.pi)
    fd(t, radius)
    lt(t, 180.-(180.-angle)/2)
    fd(t, length)
    lt(t, 180.-(180.-angle)/2)
    fd(t, radius)

def pie(t, n, radius):
    for i in range(n):
        pieTriangle(t, n, radius)
        lt(t, 180.)

if __name__ == "__main__":
    world = TurtleWorld()

    jack = Turtle()
    #jack.delay = 0.001

    #petal(jack, 200, 60)

    pie(jack, 8, 150)

    #flower(jack, 20, 200, 60)
    #flower(jack, 30, 150, 60)


    #circle(jack, 60)
    #arc(jack, 100, 360.)

    wait_for_user()