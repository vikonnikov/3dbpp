import math

from variables import *
from bounds.first import bound_one_x
from utils import find_plist, rotate_problem

def bound_two_x(bin, boxes):
    """Derive bound L_2 for a fixed dimension"""

    # derive bound_one
    lb = lb1 = bound_one_x(bin, boxes)

    W = bin.w; H = bin.h; D = bin.d; hlb1 = H * lb1;
    W2 = W/2; D2 = D/2; WD = W*D; BVOL = bin.volume;

    # run through all values of p, q
    plist = find_plist(boxes, W2, WDIM)
    qlist = find_plist(boxes, D2, DDIM)

    for p in plist:
        for q in qlist:
            k1h = k23v = 0
            for box in boxes:
                w = box.w; h = box.h; d = box.d;
                if (w > W - p) and (d > D - q):
                    k1h += h; continue;
                if (w >= p) and (d >= q):
                    k23v += box.volume
            fract = math.ceil((k23v - (hlb1 - k1h)*WD) / BVOL)
            if fract < 0:
                fract = 0
            lbx = lb1 + fract
            if lbx > lb:
                lb = lbx

    return lb

def bound_two(box, boxes):
    """Derive bound L_2 as the best of all L_2 bounds for three rotations"""
    lb = 0
    for i in range(WDIM, DDIM + 1):
        lbx = bound_two_x(box, boxes)
        lb = max(lb, lbx)
        rotate_problem(box, boxes)

    return lb