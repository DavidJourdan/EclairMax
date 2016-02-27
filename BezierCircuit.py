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
t = sp.symbols('t')


def bernstein(i,n) :
    return(lambda t : (sc.binom(n,i)*(t**i)*(1-t)**(n-i)))


def bezier(abs,ord) :
    n = len(abs) - 1
    x=0
    y=0
    for i in range(n+1) :
        x+=Bernstein(i,n)(t)*abs[i]
        y+=Bernstein(i,n)(t)*ord[i]
    return x,y

