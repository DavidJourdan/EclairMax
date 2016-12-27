# EclairMax

This is a small school project I did in my 2nd year to prepare for competitive exams. Given a vector or discretized representation of a road this program computes an optimal disposition of lights, meaning that all the road area is lit and the ratio between the total illuminated area and the area of the road is maximal.

This is a proof of concept so this ignores the limitations of the eletrical grid (although we can imagine the lamps are powered by solar energy) and it assumes the lamps cast light uniformly so the lit area is circular. However, this can be easily upgraded by changing the distance used (here the classic, cartesian one) by a less orthodox one to model elliptic lit areas (or even more complex geometries using more exotic metric spaces).

I first programmed it in Python during my school project but more recently when I discovered Haskell I realised it would be a good idea to write it in this language because I made an extensive use of recursion that sometimes caused problems with Python and its recursion limit.
