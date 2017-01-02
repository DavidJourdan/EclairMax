# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:10:02 2015

@author: jourdan

#######  Bézier Curves #######

This module creates random Bézier curves and tests the EclairMax module on them.

Bézier Curves have certain geometrical properties that makes them suited for
the kind of simulation we want because we can easily 'assemble' them using G1
continuity and make any polynomial curve with it.
"""


import numpy as np
import scipy.special as sc
import sympy as sp
from random import random, uniform
import EclairMax, Graphics
t = sp.symbols('t')


def bernstein(i,n):
    return(lambda t : (sc.binom(n,i)*(t**i)*(1-t)**(n-i)))


def bezier(abs,ord):
    n = len(abs) - 1
    x=0
    y=0
    for i in range(n+1):
        x+=bernstein(i,n)(t)*abs[i]
        y+=bernstein(i,n)(t)*ord[i]
    return np.array([[x, y, 0.0, 1.0]])

abs, ord = [0.0, random(), random(), 1.0], [0.0, uniform(-2.0, 2.0), uniform(-2.0, 2.0), 1.0]
step = 0.001
w = 0.1
r_min = 0.101
r_max = 0.4
F = bezier(abs, ord)

r_arr, ratio, i = EclairMax.eclair_max(w, F, step, r_min, r_max, 1000)
road_arr = EclairMax.road_creator(F, step, w)
lamp_arr = EclairMax.eclaire(r_arr[i], road_arr)
Graphics.display_eclair_max(road_arr, lamp_arr, r_arr, ratio, r_arr[i])