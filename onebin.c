#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <limits.h>

#include "3dbpp.h"

/* boolean general_pack(allinfo *a, box *f, box *l); */

int readtest(box *tab, itype *W, itype *H, itype *D, char *file)
{
  FILE *in;
  box *i;
  int n, w, h, d;

  printf("Read from file: %s\n", file);

  in = fopen(file, "r");
  if (in == NULL) { printf("wrong filename"); exit(-1); }

  fscanf(in,"%d %d %d %d", &n, &w, &h, &d);
  *W = w; *H = h; *D = d;
  for (i = tab; i < tab+n; i++) {
    fscanf(in,"%d %d %d", &w, &h, &d);
    i->w = w; i->h = h; i->d = d;
    printf("  Box: %2d %2d %2d\n", w, h, d);
  }
  fclose(in);
  return n;
}

void init(allinfo *a, int n, int W, int H, int D)
{
	box t0[MAXBOXES], t1[MAXBOXES], t2[MAXBOXES], t3[MAXBOXES];
	boolean cl[MAXBOXES];

	a.n = n; a.W = W; a.H = H; a.D = D;
	a.fbox     = t0;
	a.lbox     = a.fbox + a.n - 1;
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

	box tab[MAXBOXES];
	int n = readtest(tab, &W, &H, &D, filename);

	printf("Number of boxes: %d\n", n);

	allinfo a;
	init(a, n, W, H, D);

	printf("Bin: %d %d %d\n", W, H, D);

	printf("Bin volume: %d\n", W * H * D);
	printf("Bin volume: %s\n", a.n);

	return 0;
}

