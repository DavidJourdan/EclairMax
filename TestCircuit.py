# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:10:02 2015

@author: jourdan

#######  Road 1 #######

Intended for testing purposes, this road is formed of elliptic, hyperbolic,
catenary, and sine curves. It was built from scratch, thus it may lack certain
geometrical properties to be a realistic candidate.
"""

from math import pi, sqrt, cosh
import EclairMax, Graphics
import numpy as np
import sympy as sp
t = sp.symbols('t')

a = (sqrt((2 * pi - 8.5) ** 2 + 4) + sqrt((2 * pi - 8.5) ** 2 + (10 - cosh(8.5 - 2 * pi)) ** 2)) / 2
b = sqrt(a ** 2 - (6 - cosh(8.5 - 2 * pi) / 2) ** 2)
L = 0.5
F = np.array([[t, -1 / t, -0.5, -9],
              [3 * sp.sin(t) - 9, 40 / 9. * sp.cos(t) + 41 / 9., -pi, 0],
              [t, sp.sin(t + 9 + pi / 2) + 8, -9, 2 * pi - 9],
              [t, 10 - sp.cosh(t + 9 - 2 * pi), 2 * pi - 9, -0.5],
              [b * sp.sin(t) + 2 * pi - 9, a * sp.cos(t) + 6 - cosh(8.5 - 2 * pi) / 2,
              pi / 2 - 0.3921415, pi / 2 + 0.3921415]])

step = 0.001
w = 1.0
r_min = 1.1
r_max = 2.0

r_arr, ratio, i = EclairMax.eclair_max(w, F, step, r_min, r_max, 1000)
road_arr = EclairMax.road_creator(F, step, w)
lamp_arr = EclairMax.eclaire(r_arr[i], road_arr)
Graphics.display_eclair_max(road_arr, lamp_arr, r_arr, ratio, r_arr[i])

R = 1.265