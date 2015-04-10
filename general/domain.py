from variables import *
from general.core import DomainPair
from general.findcoordinates import findcoordinates

def modifyandpush(i, j, rel, dom):
    """Push the relation "rel" between box i and box j to info stack. If "dom"
    is True, the relation is removed from the domain. If "dom" is False,
    the relation "rel" is imposed between boxes "i" and "j"."""
    
    if dom:
        r = rel
        domain[i][j][rel] = False
    else:
        r = relation[i][j]
        relation[i][j] = rel
        
    pair = DomainPair(i, j, r, dom)
    domstack.append(pair)
    
    if len(domstack) == STACKDEPTH:
        raise Exception("Stack filled")

def popdomains(pair):
    """Pop all relations between boxes from the stack. The stack is emptied
    downto the depth given by "pos"."""
    
    for p in domstack[domstack.index(pair):]:
        domstack.remove(p)
    
        if pair.domain:
            domain[pair.i][pair.j][pair.relation] = True
        else:
            relation[pair.i][pair.j] = pair.relation
 
def checkdomain(info, i, j, n, boxes, value):
    """Temporarily impose the relation "value" between boxes "i" and "j",
    and check whether a feasible assignment of coordinates exists which
    respects all currently imposed relations. 
      If the relation cannot be satisfied, it is removed from the domain
    and pushed to a stack, so that it can be restored upon backtracking."""

    if domain[i][j][value] == False:
        return # not allowed in any case
    
    relation[i][j] = value
    
    if findcoordinates(info, n, boxes) == False:
        modifyandpush(i, j, value, True)
 
def reducedomain(info, n, boxes):
    """Constraint propagation algorithm. For each relation in the domain of
    boxes "i" and "j", check if the relation has the posibility of being
    satisfied. If some of the relations cannot be satisfied any more, they
    are removed from the domain (and pushed to a stack, so that they can
    be restored when the master search algorithm backtracks). If only one
    relation remains in the domain, the relation is imposed at this node
    and all descendant nodes."""
    m = 0
    for i in range(0, n - 1):
        for j in range(i + 1, n - 1):
            if relation[i][j] == UNDEF:
                checkdomain(info, i, j, n, boxes, LEFT);
                checkdomain(info, i, j, n, boxes, RIGHT);
                checkdomain(info, i, j, n, boxes, UNDER);
                checkdomain(info, i, j, n, boxes, ABOVE);
                checkdomain(info, i, j, n, boxes, FRONT);
                checkdomain(info, i, j, n, boxes, BEHIND);
                relation[i][j] = UNDEF;
                for k in range(LEFT, UNDEF):
                    l = 0
                    if domain[i][j][k]:
                        l += 1; m = k;
                    if l == 0:
                        return False
                    if l == 1:
                        modifyandpush(i, j, m, False)

    return True