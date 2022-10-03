#!/usr/bin/env python

import math

def Lemiscate_trajectory(t):
    tx = 5.544444
    ty = 5.544444
    A_x = 4.0
    A_y = 2.0
    T = 100.0
    w = 2*math.pi/T
    # print(t)
    xg = tx + A_x* math.sin(w*t)
    yg = ty + A_y* math.sin(2*w*t)
    return xg, yg

def lemiscate_of_bernoulii(t):
    # print(t)
    tx = 5.544444
    ty = 5.544444
    a = 5.0
    T = 200.0
    w = 2*math.pi/T
    xg = tx + a*math.cos(w*t)/(1+(math.sin(w*t))**2)
    yg = ty + a*math.sin(w*t)*math.cos(w*t)/(1+(math.sin(w*t))**2)
    return xg, yg

def hippopede_traj(t):
    tx = 5.544444
    ty = 5.544444
    a = 2.5
    b = 2.49999  
    T = 50.0
    w = 2*math.pi/T
    r = abs(math.sqrt(4*b*(a - b*(math.sin(w*t))**2)))
    xg = tx + r*math.cos(w*t)
    yg = ty + r*math.sin(w*t)
    return xg, yg

def circular_trajectory(t):
    tx = 5.544444
    ty = 5.544444
    r = 1.0
    T = 200.0
    w = 2*math.pi/T
    xg = tx + r*math.cos(w*t)
    yg = ty + r*math.sin(w*t)
    return xg, yg

def logarithmic_spiral(t):
    tx = 5.544444
    ty = 5.544444
    a = 0.2
    b = 0.02
    T = 50.0
    w = 2*math.pi/T
    xg = tx + a*math.exp(b*t)*math.cos(w*t)
    yg = ty + a*math.exp(b*t)*math.sin(w*t)
    return xg, yg

def archimedean_spiral(t):
    tx = 5.544444
    ty = 5.544444
    T = 50.0
    w = 2*math.pi/T
    a = 0.02
    xg = tx + a*t*math.cos(w*t)
    yg = ty + a*t*math.sin(w*t)
    return xg, yg