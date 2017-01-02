# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:10:02 2015

@author: jourdan

#######  Graphics #######

"""

from matplotlib.pyplot import plot, show, Circle, gcf, axis, xlabel, ylabel, subplot

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
    graph = gcf()
    for k in range(n):
        graph.gca().add_artist(Circle((lamp[k, 0], lamp[k, 1]), R, fill=False))
    show()

def display_eclair_max(road, lamp, r_arr, eta, r_max):
    subplot(211)
    xlabel("radius")
    ylabel("ratio")
    plot(r_arr, eta, '-')

    subplot(212)
    plot(road[0], road[1], 'y--')
    plot(road[2], road[3], 'k')
    plot(road[4], road[5], 'k')
    plot(lamp[:, 0], lamp[:, 1], 'ro')
    axis('equal')
    n = len(lamp)
    graph = gcf()
    for k in range(n):
        graph.gca().add_artist(Circle((lamp[k, 0], lamp[k, 1]), r_max, fill=False))
    show()
