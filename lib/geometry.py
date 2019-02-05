# -*- coding: utf-8 -*-
"""
Created on Tue Dec 04 21:41:19 2012
@author: <Ronny Eichler> ronny.eichler@gmail.com

Geometry functions.
"""

import numpy as np
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def middle_point(coord_list):
    """Find center point of a list coordinates. E.g. find center of group of LEDs to track.
    Returns None if no valid LEDs found, and position of single LED if only one valid, etc.
    """
    # TODO: Proper type checking, corner cases, None etc.
    coord_list = [c for c in coord_list if c is not None]
    n = 1.0*len(coord_list)
    if n < 1:
        return None
    x =int(round(sum([c[0]/n for c in coord_list])))
    y =int(round(sum([c[1]/n for c in coord_list])))
    return [x, y]


def scale_points(pts, rng):
    """ Scale points in list of given normalized (0.0-1.0) points to a range
    i.e. 1.0 --> 640 etc.
    """
    try:
        is_list = len(pts[0]) > 1
    except:  # Exception as inst
        pts = [pts]
        is_list = False

    outpts = []
    if type(rng[0]) == int and type(rng[1]) == int:
        for p in pts:
            outpts.append([int(p[0]*rng[0]), int(p[1]*rng[1])])
    else:
        for p in pts:
            outpts.append([p[0]*rng[0], p[1]*rng[1]])

    if is_list:
        return outpts
    else:
        return outpts[0]


def norm_points(pts, rng):
    """ Normalize points in a list of points by dividing by their range
    in the respective axis.
    """
    try:
        is_list = len(pts[0]) > 1
    except: # Exception as inst
        pts = [pts]
        is_list = False

    outpts = []
    for p in pts:
        outpts.append( [p[0]*1.0/rng[0], p[1]*1.0/rng[1]] )

    if is_list:
        return outpts
    else:
        return outpts[0]


def map_points(pt_list, range1, range2):
    """ Map points from range 1 to range 2. """
    npt = norm_points(pt_list, range1)
#    print ('normalized: ', npt)
    scpt = scale_points(npt, range2)
    return scpt


def scale(val, range1, range2):
    """
    Maps val of numerical range 1 to numerical range 2.
    """
    # normalize by range of range1, multiply by range of range2, offset
    return ((float(val) - range1[0]) / (range1[1] - range1[0])) * (range2[1] - range2[0]) + range2[0]

#a better way for position guessing: autoregressive extrapolation with moving window
def extrapolateAutoReg(pos_hist, windowsize):
    t = np.linspace(0, windowsize + 1, windowsize + 1)
    fx = np.poly1d(np.polyfit(t[0:-1], x, 1))
    fy = np.poly1d(np.polyfit(t[0:-1], y, 1))
    return (fx(t[-1]), fy(t[-1]))


def extrapolateLinear(p1, p2):
    """
    Linear extrapolation of missing point
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    return tuple([p2[0]+dx, p2[1]+dy])

# a much better way for position guessing, but does it
def AutoregPosition(pos_hist):
    windowsize=4
    if len(pos_hist) >= windowsize:
        filtered=filter(pos_hist[-windowsize:])
        if (len(filtered)==windowsize):
            return extrapolateAutoReg(filtered, windowsize)
        elif len(filtered>0):
            windowsize=len(filtered)
            return extrapolateAutoReg(filtered, windowsize)
        else:
            return None
    else:
        return None

#linear extrapolation--> not necessary any more after the Kalman filter
def guessedPosition(pos_hist):
    if len(pos_hist) >= 3:
       # print pos_hist[-1], pos_hist[-2], pos_hist[-3]
        if not (pos_hist[-1] is None):
            return pos_hist[-1]
        elif not ((pos_hist[-2] is None) or (pos_hist[-3] is None)):
                return extrapolateLinear(pos_hist[-3], pos_hist[-2])
        else:
            return None
    else:
        return None


def distance(p1, p2):
    """ Euclidean distance between two points. """
    if p1 is not None and p2 is not None:
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    else:
        return None

def angle(dx, dy):
    """Used for movement direction calculation. Returns atan2(dy,dx) in degrees between 0 and 360"""

    if dx is not None and dy is not None:
        return int(math.fmod(math.degrees(math.atan2(dy, dx)) + 360, 360))
    else:
        return None
def norm_angle(p1, p2):
    """Used for orientation calculation. Returns the degree of the normal vector between the two points in degrees between 0 and 360"""
    if p1 is not None and p2 is not None:
        dx = (p2[0] - p1[0]) * 1.0  # x2-x1
        dy = (p2[1] - p1[1]) * 1.0
        #  important: dx and dy are changed up (atan2(dx,dy) instead of atan2(dy,dx)) to have a 90 degrees turn (because it's a normal vector)
        #  +360 is added to avoid negative values
        #  mod 360 is applied to have a result between 0 and 360
        return int(math.fmod(math.degrees(math.atan2(dy, dx)) + 90, 360))
    else:
        return None

def perp(a):
    """Line segment intersection using vectors. Modified and taken from:
    http://www.cs.mun.ca/~rod/2500/notes/numpy-arrays/numpy-arrays.html
    """
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def seg_intersect(a1, a2, b1, b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot(dap, dp)
    if denom == 0.0:
        return None
    else:
        return (num / denom)*db + b1


def point_in_poly(point, poly):
    """Improved point in polygon test which includes edge and vertex points
    From: http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html
    """
    x = point[0]
    y = point[1]
    n = len(poly)

    # check if point is a vertex
    if (x, y) in poly:
        return True

    # check if point is on a boundary
    for i in range(n):
        if i == 0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i-1]
            p2 = poly[i]
        if p1[1]==p2[1] and p1[1]==y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
            return True

    # check the actual polygon space
    inside = False

    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


if __name__ == "__main__":
    pass
    #a = np.array( [0.0, 0.0] )
    #b = np.array( [0.0, 1.0] )
    #c = np.array( [1.0, 1.0] )
    #d = np.array( [1.0, 0.0] )
    #print seg_intersect( a,d, b,c)
    #
    #p1 = np.array( [2.0, 2.0] )
    #p2 = np.array( [4.0, 3.0] )
    #p3 = np.array( [6.0, 0.0] )
    #p4 = np.array( [6.0, 3.0] )
    #print seg_intersect( p1,p2, p3,p4)
    #
    ## Test a vertex for inclusion
    #poly = [(-33.416032,-70.593016), (-33.415370,-70.589604),
    #(-33.417340,-70.589046), (-33.417949,-70.592351),
    #(-33.416032,-70.593016)]
    #point = (-33.416032,-70.593016)
    #print point_in_poly(point, poly)
    #
    ## test a boundary point for inclusion
    #poly = [(1,1), (5,1), (5,5), (1,5), (1,1)]
    #point = (3, 1)
    #print point_in_poly(point, poly)
