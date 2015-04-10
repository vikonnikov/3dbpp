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

def checksol(info, boxes):
    """Check correctnes of solution, i.e., no boxes overlap, no duplicated boxes.
    If the solution should be robot packable, it is checked that there
    exists an ordering of the boxes such that they can be removed one
    by one withouth having any other boxes behind/above/right of the
    current box."""
# {
#   box *i, *j, *m;
#   boolean stillboxes, foundextreme, extreme;
#   int b;
# 
#   for (i = f, m = l+1; i != m; i++) { 
#     if (!i->k) continue;  /* box currently not chosen */
#     for (j = f; j != m; j++) {
#       if (i == j) continue;
#       if (i->no == j->no) error("duplicated box %d\n", i->no); 
#       if (!j->k) continue;
#       if (i->bno != j->bno) continue;
#       if ((i->x + i->w > j->x) && (j->x + j->w > i->x) &&
#       (i->y + i->h > j->y) && (j->y + j->h > i->y) &&
#       (i->z + i->d > j->z) && (j->z + j->d > i->z)) {
#     error("overlap box %d,%d: [%d,%d,%d] [%d,%d,%d]",
#           i->no, j->no, i->w, i->h, i->d, j->w, j->h, j->d);
#       }
#     }
#   }
# 
#   if (a->packtype != ROBOT) return;
# 
#   /* check if robot packable */
#   for (b = 1; b <= a->z; b++) {
#     for (;;) {
#       stillboxes = FALSE; 
#       foundextreme = TRUE;
#       for (i = f; i <= m; i++) {
#         if ((i->bno == b) && (i->k == 1)) stillboxes = TRUE;
#       }
#       if (!stillboxes) break;
#   
#       foundextreme = FALSE;
#       for (i = f; i <= m; i++) { 
#         if ((i->bno != b) || (i->k != 1)) continue;
#         extreme = TRUE;
#         for (j = f; j <= m; j++) { 
#           if (j == i) continue;
#           if ((j->bno != b) || (!j->k != 1)) continue;
#           if ((i->x < j->x + j->w) || (i->y < j->y + j->h) 
#                                    || (i->z < j->z + j->d)) extreme = FALSE;
#         }
#         if (extreme) { i->k = -1; foundextreme = TRUE; }
#       }
#       if (!foundextreme) break;
#     }
#   
#     if (!foundextreme) {
#       for (i = f; i <= m; i++) {
#         if (i->bno == b) {
#           printf("no %d (%d %d %d) (%d %d %d) bin %d k %d\n",
#                  i->no, i->x, i->y, i->z, i->w, i->h, i->d, i->bno, i->k);
#         }
#       }
#       error("not robot packable");
#     }
#     /* restore k values */
#     for (i = f; i <= m; i++) if (i->k == -1) i->k = 1;
#   }
# }