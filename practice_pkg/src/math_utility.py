#!/usr/bin/env python

import math

def deg2rad(th):
    return (th*math.pi/180.0)

def rad2deg(th):
    return (th*180.0/math.pi)

def wrap_pi_2(th):
    if(th<=-math.pi/2.0):
        return (th + math.pi)
    elif(th>= math.pi/2.0):
        return (th - math.pi)
    else:
        return th

def wrap_pi(th):
    if(th<=-math.pi):
        while not(th>=-math.pi):
            th = th + 2*math.pi
        return th
    elif(th>= math.pi):
        while not(th<= math.pi):
            th = th - 2*math.pi
        return th
    else:
        return th 