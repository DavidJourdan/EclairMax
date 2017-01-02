# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:10:02 2015

@author: jourdan

#######  ECLAIRMAX #######

This module emulates a road (road_creator which takes
parametrical equations describing the road as inputs) which can then be
displayed with the Graphics module, it can place lights optimally on this road
assuming they cast light on a circle of radius r (eclaire), eventually it finds
the best radius for a given road using these assumptions (eclair_max)
"""

# import statements
import sys
from math import pi, sqrt, fabs
import sympy as sp
import numpy as np

# if the program returns a recursion error, just modify the recursion limit below
sys.setrecursionlimit(50000)

#Useful, general-purpose functions

def d(A, B):
    """The euclidian distance between two points

    :param A: a 2-dimensional point
    :param B: a 2-dimensional point
    :type A: array of len 2
    :type B: array of len 2
    :return: the euclidian distance
    :rtype: float

    :Example:
    >>> d([0,0],[0,1])
    1
    """
    return sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

def area(points):
    """Determines the area of a polygon

    Uses the shoelace formula

    :param points: the points of the polygon
    :type points: matrix of size 2*n
    :return: the area of the polygon
    :rtype: float

    :Example:

    >>> area([[0,1,0,1],[0,0,1,1]])
    1
    """
    n = len(points[0])
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[0, i] * points[1, j]
        area -= points[0, j] * points[1, i]
    area = abs(area) / 2.0
    return area

#Local, recursive and callback functions

def standard_placing(curve, r, B, C, i, n):
    """Places a lamp in case everything goes well

    Recursive function

    :param curve: the curve in which the program iterates
    :param r: radius
    :param B: intersection in upper curve
    :param C: intersection in lower curve
    :param i: index
    :param n: size of curve
    :type curve: matrix of size 2*n
    :type r: float
    :type B: array of len 2
    :type C: array of len 2
    :type i: int
    :type n: int
    :return: the point of the new lamp
    :return: the index of the new lamp in curve
    """
    A = curve[:, i]
    if d(A, B) <= r and d(A, C) <= r and i < n - 1:
        return standard_placing(curve, r, B, C, i + 1, n)
    else:
        return curve[:, i - 1], i - 1


def placing(curve, r, B, C, i, n):
    """General placing function

    If everything goes well (ie d(A,B)<r and d(A,C)<r) calls back standard_placing
    Else, ignores the farthest point and iterates through curve via recursion

    :param curve: the curve in which the program iterates
    :param r: radius
    :param B: intersection in upper curve
    :param C: intersection in lower curve
    :param i: index
    :param n: size of curve
    :type curve: matrix of size 2*n
    :type r: float
    :type B: array of len 2
    :type C: array of len 2
    :type i: int
    :type n: int
    :return: the point of the new lamp
    :return: the index of the new lamp in curve
    """
    A = curve[:, i]
    if d(A, C) <= r and d(A, B) > r and i < n - 1:
        return placing(curve, r, B, C, i + 1, n)
    elif d(A, B) <= r:
        return standard_placing(curve, r, B, C, i, n)
    else:
        return curve[:, i - 1], i - 1


def intersection(curve, r, A, i, n):
    """Determines the intersection between the circle of center A and the curve

    :param curve: the curve in which the program iterates
    :param r: radius
    :param A: a point
    :param i: index
    :param n: size of curve
    :type curve: matrix of size 2*n
    :type r: float
    :type A: array of len 2
    :type i: int
    :type n: int
    :return: the point of the new lamp
    :return: the index of the new lamp in curve

    """
    B = curve[:, i]
    while d(A, B) < r and i < n - 1:
        i += 1
        B = curve[:, i]
    return curve[:, i - 1], i - 1

#Main functions

def road_creator(F, step, w):
    """Return the upper, lower and middle curve of the road

    :param F: the formal description of the road
    :param step: step size of the array
    :param w: width of the road
    :type F: ndarray of shape (n,4) containing sympy functions and their range
    :type step: float
    :type w: float
    :return:the x-axis and y-axis of the central curve, lower curve and upper curve
    :rtype: ndarray with 6 lines

    """
    # define a symbolic variable
    t = sp.symbols('t')

    X, Y, LX, LY = [], [], [], []
    n = len(F)
    for k in range(n):
        x = sp.lambdify(t, F[k, 0], "numpy") #used to map the expressions in an array
        y = sp.lambdify(t, F[k, 1], "numpy")
        if F[k, 3] - F[k, 2] > 0: #if the curve goes backwards, compute the negative derivative
            dx = sp.lambdify(t, sp.diff(F[k, 0], t), "numpy")
            dy = sp.lambdify(t, sp.diff(F[k, 1], t), "numpy")
        else:
            dx = sp.lambdify(t, - sp.diff(F[k, 0], t), "numpy")
            dy = sp.lambdify(t, - sp.diff(F[k, 1], t), "numpy")
        #list of values for t
        A = np.linspace(F[k, 2], F[k, 3], fabs((F[k, 3] - F[k, 2]) / step), endpoint=False)
        X.append(x(A)) #list of values for x(t)
        Y.append(y(A)) #list of values for y(t)
        # formulas for finding the parallel curves
        LX.append(-w / 2. * dy(A) / np.sqrt(dy(A) ** 2 + dx(A) ** 2))
        LY.append(w / 2. * dx(A) / np.sqrt(dy(A) ** 2 + dx(A) ** 2))
    X, Y, LX, LY = np.array(X), np.array(Y), np.array(LX), np.array(LY)
    X, Y, LX, LY = np.concatenate(X), np.concatenate(Y), np.concatenate(LX), np.concatenate(LY)
    return np.array([X, Y, X - LX, Y - LY, X + LX, Y + LY])


def eclaire(r, road):
    """Return the list of lamps

    :param r: the radius
    :param road: the road in which iterates the function
    :type r: float
    :type road: ndarray of floats with 6 lines
    :return: the list of lamps
    :rtype: 1-dimensional ndarray
    """
    lower, upper = road[2:4], road[4:]
    i, j = 0, 0
    n = len(road[0])
    A = upper[:, 0]
    B = upper[:, 0]
    C = lower[:, 0]
    on_the_upper_side = True
    lst = [A]
    while i < n - 2 and j < n - 2:
        #get the intersections
        B, i = intersection(upper, r, A, i, n)
        C, j = intersection(lower, r, A, j, n)
        #start from that intersection, in the opposite curve
        if on_the_upper_side:
            A, j = placing(lower, r, B, C, j, n)
        else:
            A, i = placing(upper, r, C, B, i, n)
        lst.append(A)
        on_the_upper_side = not on_the_upper_side
    return np.vstack(lst[:])


def eclair_max(w, F, step, rmin, rmax, N):
    """Return the best radius in a given range

    We define the efficiency as the ratio between the area of the road and the
    sum of the areas cast by the lamps

    :param w: the width of the road
    :param F: the formal description of the road
    :param step: step size of the road array
    :param rmin: minimum radius in the range
    :param rmax: maximum radius in the range
    :param N: the number of values
    :type w: float
    :type F:
    :type step: float
    :type rmin: float
    :type rmax: float
    :type N: int
    :return: res[0]: an array containing the different radii
    :return: ratio: the road area divided by the total lit area
    :return: the index of the maximum value in res
    """
    road = road_creator(F, step, w)
    road_area = area(np.concatenate((road[2:4], np.fliplr(road[4:])), axis=1))
    res = np.empty((2, N), dtype=float)
    for k in range(N):
        r = rmin + k * (rmax - rmin) / float(N)
        lamp = eclaire(r, road)
        res[0, k] = r
        res[1, k] = len(lamp)
    ratio = road_area / (res[1] * pi * res[0] ** 2)
    return res[0], ratio, np.argmax(ratio)
