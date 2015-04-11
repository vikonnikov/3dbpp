from variables import *
from general.domain import reducedomain, popdomains
from general.findcoordinates import findcoordinates

def recpack(info, i, j, n, boxes, rel): # box -> box *f
    """Recursive algorithm based on constraint programming used for assigning
    relative positions to each pair of boxes. Each pair of boxes initially 
    has an associated relation with domain LEFT, RIGHT, UNDER, ABOVE, FRONT, 
    BEHIND. In each iteration of the algorithm a pair of boxes "i" and "j"
    is assigned the relation "rel". Constraint propagation is then used to 
    decrease the domains of remaining relations. 
      If it is not possible to assign coordinates to the boxes such that the 
    currently imposed relations between pairs of boxes are respected, we 
    backtrack.
      If each pair of boxes has been assigned a relation, and it is possible
    to assign coordinates to the boxes such that the currently imposed 
    relations between pairs of boxes are respected, we save the solution 
    and return.
      Otherwise, constraint propagation is used to decrease the domains
    of relations corresponding to each pairs of boxes. If a domain only
    contains a single relation, the relation is fixed.
      The recursive step selects the next pair of boxes following "i" and "j"
    and repeatedly assigns each relation from the domain to the relation 
    variable."""

#     int i1, j1;
#     domainpair *pos;
#     boolean feas;

    # if stopped:
    #     return
     
    # info.iter3d += 1
    
    # if (info.iter3d == info.maxiter) and (info.maxiter != 0):
    #     terminate = True
        
    # info.subiterat += 1
     
    # if info.subiterat == IUNIT:
    #     info.subiterat = 0
    #     info.iterat += 1
#         check_iterlimit(info.iterat, info.iterlimit)
#         check_timelimit(info.timelimit)

    # if terminate:
    #     return
 
    relation[i][j] = rel
    
    i1 = j1 = 0
    while i1 != i and j1 != j:
        i1 += 1
        if i1 >= j1:
            i1 = 0; j1 += 1;
        if relation[i1][j1] == UNDEF:
            raise Exception("Relation error %d %d\n" % (i1, j1))


 
    feas = findcoordinates(info, boxes)




    if not feas:
        return
 
    if (i == n-2) and (j == n-1): 
        # feasible = True
        # terminate = True
#         memcpy(info.fsol, f, sizeof(box) * n) !!!
        return

    if domstack:
        dpair = domstack[-1]
    else:
        dpair = None

    feas = reducedomain(info, n, boxes);

    print feas

    if feas:
        i += 1
        if i >= j:
            i = 0; j += 1;
        
        # bblevel += 1
        rel = relation[i][j]
        
        if domain[i][j][LEFT]:
            recpack(info, i, j, n, boxes, LEFT);
        if domain[i][j][RIGHT]:
            recpack(info, i, j, n, boxes, RIGHT);
        if domain[i][j][UNDER]:
            recpack(info, i, j, n, boxes, UNDER);
        if domain[i][j][ABOVE]:
            recpack(info, i, j, n, boxes, ABOVE);
        if domain[i][j][FRONT]:
            recpack(info, i, j, n, boxes, FRONT);
        if domain[i][j][BEHIND]:
            recpack(info, i, j, n, boxes, BEHIND);
        
        relation[i][j] = rel;
        # bblevel -= 1

    if dpair:
        popdomains(dpair)
