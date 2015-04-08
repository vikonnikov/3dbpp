import math

def bound_zero(bin, boxes):
    """The continuous bound L_0"""
    vsum = 0
    for box in boxes:
        vsum += box.volume

    lb = math.ceil(float(vsum) / bin.volume)

    return lb