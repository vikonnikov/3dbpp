from variables import *

def rotate_problem(bin, boxes):
    """Rotates the dimensions by one step"""

    for box in boxes:
        box.rotate()

    bin.rotate()

def choose_boxes(boxes, W2, D2):
    """Returns a set of boxes with w > W2 and d > D2.
        This set is used in bound_one"""
    selected = []
    for box in boxes:
        if (box.w > W2) and (box.d > D2):
            selected.append(box)

    return selected

def find_plist(boxes, value, dim):
    """Returns a zero-terimanted list of distinct dimensions"""
    k = []

    if dim == WDIM:
        for box in boxes:
            if box.w <= value:
                k.append(box.w)
    elif dim == HDIM:
        for box in boxes:
            if box.h <= value:
                k.append(box.h)
    elif dim == DDIM:
        for box in boxes:
            if box.d <= value:
                k.append(box.d)

    k = list(set(k))
    k.sort()

    return k