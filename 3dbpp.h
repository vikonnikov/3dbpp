#ifndef __3DBPP_H__
#define __3DBPP_H__

#define IUNIT        1000  /* scaling factor of nodes and iterat */
#define MAXBOXES      101  /* max number of boxes (plus one box) */
#define MAXBPP    1000000  /* max numer of iterations in 1-dim bpp */
#define MAXITER      1000  /* max iterations in heuristic onebin_robot */
#define MAXCLOSE       16  /* max level for which try_close is applied */

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <time.h>
#include <limits.h>


/* ======================================================================
				   macros
   ====================================================================== */

#define TRUE  1           /* logical variables */
#define FALSE 0

#define WDIM  0           /* rotations of boxes */
#define HDIM  1
#define DDIM  2

#define GENERAL     0     /* packing type */
#define ROBOT       1

#define LEFT   0          /* relative placements */
#define RIGHT  1
#define UNDER  2
#define ABOVE  3
#define FRONT  4
#define BEHIND 5
#define UNDEF  6
#define RELMAX 8

#define STACKDEPTH (MAXBOXES*MAXBOXES*RELMAX)

#define VOL(i)            ((i)->w * (ptype) (i)->h * (i)->d)
#define MINIMUM(i,j)      ((i) < (j) ? (i) : (j))
#define MAXIMUM(i,j)      ((i) > (j) ? (i) : (j))
#define DIF(i,j)          ((int) ((j) - (i) + 1))
#define SWAPINT(a,b)      { register int t; t=*(a);*(a)=*(b);*(b)=t; }
#define SWAP(a,b)         { register box t; t=*(a);*(a)=*(b);*(b)=t; }
#define SWAPI(a,b)        { register itype t; t=(a);(a)=(b);(b)=t; }
#define SWAPP(a,b)        { register point t; t=*(a);*(a)=*(b);*(b)=t; }
#define DF(a,b)           ((r=(a).y-(b).y) != 0 ? r : (a).x-(b).x)


/* ======================================================================
				 type declarations
   ====================================================================== */

typedef short         boolean; /* logical variable      */
typedef short         ntype;   /* number of states,bins */
typedef short         itype;   /* can hold up to W,H,D  */
typedef long          stype;   /* can hold up to W*H*D  */
typedef long          ptype;   /* product multiplication */

/* box record */
typedef struct irec {
  ntype    no;           /* box number                            */
  itype    w;            /* box width  (x-size)                   */
  itype    h;            /* box height (y-size)                   */
  itype    d;            /* box depth  (z-size)                   */
  itype    x;            /* optimal x-position                    */
  itype    y;            /* optimal y-position                    */
  itype    z;            /* optimal z-position                    */
  ntype    bno;          /* bin number                            */
  boolean  k;            /* is the box chosen?                    */
  stype    vol;          /* volume of box                         */
  struct irec *ref;      /* reference to original box (if necessary) */
} box;

/* all problem information */
typedef struct {
  itype    W;            /* x-size of bin                         */
  itype    H;            /* y-size of bin                         */
  itype    D;            /* z-size of bin                         */
  stype    BVOL;         /* volume of a bin                       */
  ntype    n;            /* number of boxes                       */
  boolean  packtype;     /* packing type: GENERAL or ROBOT        */
  box      *fbox;        /* first box in problem                  */
  box      *lbox;        /* last box in problem                   */
  box      *fsol;        /* first box in current solution         */
  box      *lsol;        /* last box in current solution          */
  box      *fopt;        /* first box in optimal solution         */
  box      *lopt;        /* last box in optimal solution          */
  boolean  *closed;      /* for each bin indicator whether closed */
  box      *fclosed;     /* first box in closed bins              */
  box      *lclosed;     /* last box in closed bins               */
  ntype    noc;          /* number of closed bins                 */
  itype    mindim;       /* currently smallest box length         */
  itype    maxdim;       /* currently largest box length          */
  stype    maxfill;      /* the best filling found                */
  int      mcut;         /* how many siblings at each node in b&b */

  /* different bounds */
  ntype    bound0;       /* Bound L_0 at root node                */
  ntype    bound1;       /* Bound L_1 at root node                */
  ntype    bound2;       /* Bound L_2 at root node                */
  ntype    lb;           /* best of the above                     */
  ntype    z;            /* currently best solution               */

  /* controle of 3d filler */
  int      maxiter;      /* max iterations in onebin_robot        */
  int      miss;         /* number boxes not packed in onebin_robot */

  /* debugging and controle information */
  int      nodes;        /* nodes in branch-and-bound             */
  int      iterat;       /* iterations in onebin_decision         */
  int      subnodes;     /* nodes in branch-and-bound             */
  int      subiterat;    /* iterations in onebin_decision         */
  int      exfill;       /* number of calls to onebin_decision    */
  int      iter3d;       /* iterations in onebin_robot or general */
  int      zlayer;       /* heuristic solution layer              */
  int      zmcut;        /* heuristic solution mcut               */
  double   exacttopo;    /* number of topological sorts           */
  double   exacttopn;    /* number of topological sorts           */
  int      exactcall;    /* number of calls to exact              */
  int      exactn;       /* largest problem for exact             */
  double   genertime;    /* time used in onebin_general           */
  double   robottime;    /* time used in onebin_robot             */
  double   time;         /* computing time                        */
  double   lhtime;       /* layer heuristic computing time        */
  double   mhtime;       /* mcut heuristic computing time         */
  int      didpush;      /* did the lower bound push up bound     */
  int      maxclose;     /* max number of closed bins at any time */
  int      nodelimit;    /* maximum number of nodes in main tree  */
  int      iterlimit;    /* maximum number of iterations in ONEBIN*/
  int      timelimit;    /* maximum amount of time to be used     */
} allinfo;

/* structure for greedy algorithm */
typedef struct {
  int      lno;          /* layer number                          */
  int      d;            /* depth of layer                        */
  int      bno;          /* bin no assigned to layer              */
  int      z;            /* z level of layer within bin           */
  int      b;            /* temporary bin number                  */
} heurpair;

/* structure for extreme points in a single bin */
typedef struct {
  itype    x;            /* x-coordinate                          */
  itype    y;            /* y-coordinate                          */
  itype    z;            /* z-coordinate                          */
} point;

/* structure for a domain pair in constraint programming */
typedef struct {
  int i;                 /* index of box i                        */
  int j;                 /* index of box j                        */
  int relation;          /* relation between the two boxes        */
  boolean domain;        /* domain of the two boxes               */
} domainpair;


/* set of domains */
typedef char domset[RELMAX];
typedef domset domline[MAXBOXES];

/* pointer to comparison function */
typedef int (*funcptr) (const void *, const void *);

boolean general_pack(allinfo *a, box *f, box *l);

int bound_zero(allinfo *a, box *f, box *l);
int bound_one(allinfo *a, box *f, box *l);
int bound_two(allinfo *a, box *f, box *l);
void dfirst3_heuristic(allinfo *a);

#endif
