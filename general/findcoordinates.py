from variables import *

def findcoordinates(info, boxes):
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

    W = info.W; H = info.H; D = info.D;
    n = info.n

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
    # info.exacttopo += 1
    print "-*- findcoordinates -*-"
    
    for k in range(n):
        # info.exacttopn += 1
        changed = False
        print "-*- findcoordinates K=%d -*-" % k
        for i in range(n):
            gbox = boxes[i]
            log =''
            for j in range(i + 1, n):
                hbox = boxes[j]
                rel = relation[i][j]
                log += '[%2d][%2d](%d) ' % (i, j, rel)
                
                # print 'coords', k, i, j, gbox, hbox, rel
                
                if rel == UNDEF:
                    pass # do nothing
                elif rel == LEFT:
                    summ = gbox.x + gbox.w;
                    log += 'L'
                    if hbox.x < summ:
                        hbox.x = summ; changed = True
                        if summ + hbox.w > W:
                            log += ' stop LEFT'
                            return False
                elif rel == RIGHT:
                    log += 'R'
                    summ = hbox.x + hbox.w;
                    if gbox.x < summ:
                        gbox.x = summ; changed = True
                        if summ + gbox.w > W:
                            log += ' stop RIGHT'
                            return False
                elif rel == UNDER:
                    log += 'U'
                    summ = gbox.y + gbox.h;
                    if hbox.y < summ:
                        hbox.y = summ; changed = True
                        if summ + hbox.h > H:
                            log += ' stop UNDER'
                            return False
                elif rel == ABOVE:
                    log += 'A'
                    summ = hbox.y + hbox.h;
                    if gbox.y < summ:
                        gbox.y = summ; changed = True
                        if summ + gbox.h > H:
                            log += ' stop ABOVE'
                            return False
                elif rel == FRONT:
                    log += 'F'
                    summ = gbox.z + gbox.d;
                    if hbox.z < summ:
                        hbox.z = summ; changed = True
                        if summ + hbox.d > D:
                            log += ' stop FRONT'
                            return False
                elif rel == BEHIND:
                    log += 'B'
                    summ = hbox.z + hbox.d;
                    if gbox.z < summ:
                        gbox.z = summ; changed = True
                        if summ + gbox.d > D:
                            log += ' stop BEHIND'
                            return False
            
            print log
            
        if not changed:
            print 'not changed'
            return True
        else:
            print 'changed'
    
    # there must be a loop in the graph
    return False