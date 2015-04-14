#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <limits.h>

#include "3dbpp.h"

/* boolean general_pack(allinfo *a, box *f, box *l); */

int readtest(box *boxes, itype *W, itype *H, itype *D, char *file)
{
  FILE *in;
  box *i;
  int n, w, h, d, k;

  printf("Read from file: %s\n", file);

  in = fopen(file, "r");
  if (in == NULL) { printf("wrong filename"); exit(-1); }

  fscanf(in,"%d %d %d %d", &n, &w, &h, &d);
  *W = w; *H = h; *D = d;
  for (k = 0, i = boxes; i < boxes+n; i++, k++) {
    fscanf(in,"%d %d %d", &w, &h, &d);
    i->w = w; i->h = h; i->d = d; i->no = k; i->vol = VOL(i);
    printf("  Box-%d: %2d %2d %2d\n", k, w, h, d);
  }
  fclose(in);
  return n;
}

allinfo init(int n, int W, int H, int D, box *boxes)
{
	allinfo a;
	box t0[MAXBOXES], t1[MAXBOXES], t2[MAXBOXES], t3[MAXBOXES];
	boolean cl[MAXBOXES];

	/* printf("  Box: %2d\n", boxes->no, boxes->w, boxes->h, boxes->d); */

	a.n = n; a.W = W; a.H = H; a.D = D;
	a.fbox     = boxes;
	a.lbox     = boxes + a.n - 1;
	a.fsol     = t1;
	a.lsol     = a.fsol + a.n - 1;
	a.fopt     = t2;
	a.lopt     = a.fopt + a.n - 1;
	a.fclosed  = t3;
	a.lclosed  = a.fclosed - 1;
	a.noc      = 0;
	a.closed   = cl;
	a.BVOL     = W * (ptype) H * D;
	a.packtype = GENERAL;
	a.maxfill  = 0;
	a.exfill   = 0;
	a.nodelimit= 0;
	a.iterlimit= 0;
	a.timelimit= 0;
	a.nodes    = 0;
	a.subnodes = 0;
	a.iterat   = 0;
	a.subiterat= 0;
	a.didpush  = 0;
	a.maxclose = 0;
	a.genertime= 0;
	a.robottime= 0;
	a.z        = a.n+1;

	return a;
}

int main(int argc, char *argv[])
{

/*
	  copyboxes(&a, w, h, d, W, H, D);


	  a.bound0 = bound_zero(&a, a.fbox, a.lbox);
	  a.bound1 = bound_one(&a, a.fbox, a.lbox);
	  a.bound2 = bound_two(&a, a.fbox, a.lbox);

	  printf("lb0: %d lb1: %d lb2: %d\n", a.bound0, a.bound1, a.bound2);

	  a.lb = a.bound2;
*/
	itype W, H, D;

	char filename[100];
	strcpy(filename, argv[1]);

	box boxes[MAXBOXES];
	int n = readtest(boxes, &W, &H, &D, filename);

	printf("Number of boxes: %d\n", n);

	allinfo a = init(n, W, H, D, boxes);

	printf("FBox: %d LBox: %d\n", a.fbox->no, a.lbox->no);

	a.bound0 = bound_zero(&a, a.fbox, a.lbox);
	a.bound1 = bound_one(&a, a.fbox, a.lbox);
	a.bound2 = bound_two(&a, a.fbox, a.lbox);
	a.lb = a.bound2;

	printf("Bin: %d %d %d Volume: %d\n", W, H, D, a.BVOL);
	printf("L0: %d L1: %d L2: %d\n", a.bound0, a.bound1, a.bound2);

/*	dfirst3_heuristic(&a); */
	general_pack(&a, a.fbox, a.lbox);

	int i;
	  for (i = 0; i < n; i++) {
	    printf("Box: (%d, %d, %d)\n", boxes[i].x, boxes[i].y, boxes[i].z);
	  }

	return 0;
}

