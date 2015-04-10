from variables import *

def findcoordinates(info, n, boxes):
    """Find coordinates of boxes according to the currently pending relations.
    In principle this can be done by topologically sorting the boxes according
    to e.g. the left-right relations, and then assigning coordinates from
    the left-most box to the right-most box.
      The following implementation is a simplified version, which runs through
    all pairs of boxes, and checks whether they satisfy the relation, otherwise
    moving one of the boxes right, up or behind, according to the given
    relation. The process is repeated until no pairs of boxes violate a
    relation. Computational experiments have shown that the present approach
    for the considered instances is faster than a topological sorting followed
    by a critical path calculation.
      If a box during the process gets moved outsides of the bin, then
    the algorithm terminates with FALSE. Otherwise TRUE is returned, saying
    that a feasible packing exists which respects the current relations."""

#   register box *g, *h;
#   register int sum;
#   int i, j, k, W, H, D;
#   boolean changed;
#   char *dom, *relij;
#   domset *domij;

    W = info.W; H = info.H; D = info.D;

    # check if feasible, i.e., at least one choice for each relation
    for i in range(n): 
        for j in range(i + 1, n):
            if relation[i][j] != UNDEF: 
                pass
            elif any(domain[i][j][LEFT:UNDEF]):
                pass
            else:
                return False
    
    # now determine the coordinates
    info.exacttopo += 1
    for k in range(n):
        info.exacttopn += 1
        changed = False
        for i in range(n):
            gbox = boxes[i]
            for j in range(i + 1, n):
                hbox = boxes[j]
                rel = relation[i][j]
                
                if rel == UNDEF:
                    pass # do nothing
                elif rel == LEFT:
                    summ = gbox.x + gbox.w;
                    if hbox.x < summ:
                        hbox.x = summ; changed = True
                        if summ + hbox.w > W:
                            return False
                elif rel == RIGHT:
                    summ = hbox.x + hbox.w;
                    if gbox.x < summ:
                        gbox.x = summ; changed = True
                        if summ + gbox.w > W:
                            return False
                elif rel == UNDER:
                    summ = gbox.y + gbox.h;
                    if hbox.y < summ:
                        hbox.y = summ; changed = True
                        if summ + hbox.h > H:
                            return False
                elif rel == ABOVE:
                    summ = hbox.y + hbox.h;
                    if gbox.y < summ:
                        gbox.y = summ; changed = True
                        if summ + gbox.h > H:
                            return False
                elif rel == FRONT:
                    summ = gbox.z + gbox.d;
                    if hbox.z < summ:
                        hbox.z = summ; changed = True
                        if summ + hbox.d > D:
                            return False
                elif rel == BEHIND:
                    summ = hbox.z + hbox.d;
                    if gbox.z < summ:
                        gbox.z = summ; changed = True
                        if summ + gbox.d > D:
                            return False
    
        if not changed:
            return True
    
    # there must be a loop in the graph
    return False