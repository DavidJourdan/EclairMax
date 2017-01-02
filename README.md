# EclairMax

This is a small school project I did in my 2nd year to prepare for competitive exams. Given a vector or discretized representation of a road this program computes an optimal disposition of lights, meaning that all the road area is lit and the ratio between the total illuminated area and the area of the road is maximal.

It uses many python scientific libraries so you might want to install a complete scientific distribution such as Anaconda or an IDE such as Spyder.

If you're on Linux running from the command line, install the required libraries :

```pip install sympy, numpy, matplotlib, scipy```

also, matplotlib requires tkinter, in Debian-like environments : ``` apt-get install tk-inter ```

Now you can modify check the test files ```TestBezier.py``` and ```TestCircuit.py``` and try them :

```python3 TestCircuit.py```
