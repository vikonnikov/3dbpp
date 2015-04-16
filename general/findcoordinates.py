from variables import *
from logger import log

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
    for i in xrange(n):
        for j in xrange(i + 1, n):
            if relation[i][j] != UNDEF:
                pass
            elif any(domain[i][j][LEFT:UNDEF]):
                pass
            else:
                return False
    
    # now determine the coordinates
    # info.exacttopo += 1
    log.debug("-*- findcoordinates -*-")
    
    for box in boxes:
        box.reset()
    
    for k in xrange(n):
        # info.exacttopn += 1
        changed = False
        log.debug("-*- findcoordinates K=%d -*-", k)
        for i in xrange(n):
            gbox = boxes[i]
            msg = ''
            msg += "\n/%dx%dx%d/\n" % (gbox.w, gbox.h, gbox.d)
            for j in xrange(i + 1, n):
                hbox = boxes[j]
                rel = relation[i][j]
                msg += '[%2d][%2d](%d) ' % (i, j, rel)
                msg += "/%d, %d, %d/ " % (hbox.x, hbox.y, hbox.z)
                
                # print 'coords', k, i, j, gbox, hbox, rel
                
                if rel == UNDEF:
                    msg += '-'
                    pass # do nothing
                elif rel == LEFT:
                    summ = gbox.x + gbox.w;
                    if hbox.x < summ:
                        msg += 'L'
                        hbox.x = summ; changed = True
                        if summ + hbox.w > W:
                            msg += ' stop LEFT'
                            log.debug(msg)
                            return False
                elif rel == RIGHT:
                    summ = hbox.x + hbox.w;
                    if gbox.x < summ:
                        msg += 'R'
                        gbox.x = summ; changed = True
                        if summ + gbox.w > W:
                            msg += ' stop RIGHT'
                            log.debug(msg)
                            return False
                elif rel == UNDER:
                    summ = gbox.y + gbox.h;
                    if hbox.y < summ:
                        msg += 'U'
                        hbox.y = summ; changed = True
                        if summ + hbox.h > H:
                            msg += ' stop UNDER'
                            log.debug(msg)
                            return False
                elif rel == ABOVE:
                    summ = hbox.y + hbox.h;
                    if gbox.y < summ:
                        msg += 'A'
                        gbox.y = summ; changed = True
                        if summ + gbox.h > H:
                            msg += ' stop ABOVE'
                            log.debug(msg)
                            return False
                elif rel == FRONT:
                    summ = gbox.z + gbox.d;
                    if hbox.z < summ:
                        msg += 'F'
                        hbox.z = summ; changed = True
                        if summ + hbox.d > D:
                            msg += ' stop FRONT'
                            log.debug(msg)
                            return False
                elif rel == BEHIND:
                    summ = hbox.z + hbox.d;
                    if gbox.z < summ:
                        msg += 'B'
                        gbox.z = summ; changed = True
                        if summ + gbox.d > D:
                            msg += ' stop BEHIND'
                            log.debug(msg)
                            return False
                else:
                    msg += '*'
                    
                msg += "/%d, %d, %d/ " % (hbox.x, hbox.y, hbox.z)
            
            log.debug(msg)
            
        if not changed:
            log.debug('not changed')
            return True
        else:
            log.debug('changed')
    
    # there must be a loop in the graph
    return False