# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:10:02 2015

@author: jourdan

#######  Graphics #######

"""

from matplotlib.pyplot import plot, show, Circle, gcf, axis, xlabel, ylabel

def display_road(road):
    plot(road[0], road[1], 'y--')
    plot(road[2], road[3], 'k')
    plot(road[4], road[5], 'k')
    axis('equal')
    show()

def display_eclaire(road, lamp, R):
    plot(road[0], road[1], 'y--')
    plot(road[2], road[3], 'k')
    plot(road[4], road[5], 'k')
    plot(lamp[:, 0], lamp[:, 1], 'ro')
    axis('equal')
    n = len(lamp)
    graphe = gcf()
    for k in range(n):
        graphe.gca().add_artist(Circle((lamp[k, 0], lamp[k, 1]), R, fill=False))
    show()

def display_eclair_max(road, lamp, R, eta):
    subplot(2,1,1)
    plot(R, eta, '-')
    
    subplot(2,1,2)
    plot(road[0], road[1], 'y--'),
    plot(road[2], road[3], 'k')
    plot(road[4], road[5], 'k')
    plot(lamp[:, 0], lamp[:, 1], 'ro')
    axis('equal')
    n = len(lamp)
    graphe = gcf()
    for k in range(n):
        graphe.gca().add_artist(Circle((lamp[k, 0], lamp[k, 1]), R, fill=False))
    show()