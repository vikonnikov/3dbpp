import math
from variables import *
from utils import rotate_problem, choose_boxes, find_plist

def bound_one(bin, boxes):
    """Derive bound L_1 as the best of all L_1 bounds for three rotations"""
    lb = 0
    for i in range(WDIM, DDIM + 1): # rotations
        lbx = bound_one_x(bin, boxes)
        lb = max(lb, lbx)
        rotate_problem(bin, boxes)

    return lb

def bound_one_x(bin, boxes):
    """Derive bound L_1 for a fixed dimension""";
    if not boxes:
        return 0

    lb = 1; H = bin.h; H2 = H/2;
    chosen = choose_boxes(boxes, bin.w/2, bin.d/2)
    if not chosen: # Empty
        return lb

    plist = find_plist(chosen, H2, HDIM)

    for p in plist:
        j1 = j2 = j3 = j2h = j2hp = j3h = 0
        for box in chosen:
            h = box.h;
            if h > H - p:
                j1 += 1
            if (H - p >= h) and (h > H2):
                j2 += 1; j2h += h; j2hp += (H - h) / p;
            if (H2 >= h) and (h >= p):
                j3 += 1; j3h += h;

        alpha = math.ceil((j3h - (j2 * H - j2h)) / H);
        beta  = math.ceil((j3 - j2hp) / (H/p));
        if alpha < 0:
            alpha = 0
        if beta  < 0:
            beta  = 0
        lb_one = j1 + j2 + max(alpha, beta)
        if lb_one > lb:
            lb = lb_one

    return lb