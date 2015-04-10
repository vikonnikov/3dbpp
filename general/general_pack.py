from variables import *
from general.repack import recpack

def general_pack(info, boxes):
    """General packing procedure, which tests whether boxes f..l can be packed
    into a single bin. The algorithm is based on constraint programming, where
    each pair of boxes initially has an associated relation with domain LEFT,
    RIGHT, UNDER, ABOVE, FRONT, BEHIND. Then the recursive algorithm "recpack"
    is called, which repeatedly tries to assign the relation a value, using
    constraint propagation to decrease the domains of remaining boxes.
    """
    feasible = False
    terminate = False
    bblevel = 1
    n = len(boxes)
#     n = l - f + 1
  
    if n > info.exactn:
        info.exactn = n

    for i in range(n):
        for j in range(n):
            relation[i][j] = UNDEF
            for k in range(LEFT, UNDEF + 1):
                domain[i][j][k] = True

    domain[0][1][RIGHT ] = False
    domain[0][1][ABOVE ] = False
    domain[0][1][BEHIND] = False

    recpack(info, 0, 0, n, boxes, UNDEF)
    
    return feasible