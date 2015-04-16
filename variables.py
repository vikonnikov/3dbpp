import numpy

IUNIT = 1000  # scaling factor of nodes and iterat
MAXBOXES = 20  # max number of boxes (plus one box)
MAXBPP = 1000000  # max numer of iterations in 1-dim bpp
MAXITER = 1000  # max iterations in heuristic onebin_robot
MAXCLOSE = 16  # max level for which try_close is applied

# TRUE = 1           # logical variables
# FALSE = 0

WDIM = 0           # rotations of boxes
HDIM = 1
DDIM = 2

GENERAL = 0     # packing type
ROBOT = 1

LEFT = 0          # relative placements
RIGHT = 1
UNDER = 2
ABOVE = 3
FRONT = 4
BEHIND = 5
UNDEF = 6
RELMAX = 8

STACKDEPTH = MAXBOXES * MAXBOXES * RELMAX

#===============================================================================
#                         global variables
#===============================================================================


# boolean variable to indicate time-out situation
stopped = None 

# int counter used to ensure that 1D BPP at most performs MAXBPP iterations
bpiterat = None

# boolean variables to indicate when 1D packing algorithm should terminate
feasible, terminate = None, None

# stack of domain pairs
domstack = []
indexes2dpair = {}
# domainpair domstack[STACKDEPTH];
# domainpair *dompos, *domend; 

# set of domains
# domset = numpy.empty(RELMAX, dtype=int)
# domline = numpy.empty([MAXBOXES, RELMAX], dtype=int)

# domain of each box / boolean 3d array
domain = []
for i in xrange(MAXBOXES):
    domain.append([])
    for j in xrange(MAXBOXES):
        domain[i].append([])
        for k in xrange(RELMAX):
            domain[i][j].append(True)

# current relation between two boxes / int 2d array
relation = numpy.full([MAXBOXES, MAXBOXES], UNDEF, dtype=numpy.int)

# int debug variable to see level in recursive packing algorithm
bblevel = None
