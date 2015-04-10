from variables import *

#===============================================================================
# The routine "fitsm" checks whether a given subset of boxes fits into a single
# bin. To improve performance, specialized algorithms are derived for cases with
# two to three boxes
#===============================================================================

def fits2(ibox, jbox, W, H, D):
    """all coordinates are initialized to zero, so just adjust changes!
    the 2-box solution is always guillotine cuttable"""
    if ibox.w + jbox.w <= W:
        jbox.x = ibox.w
    elif ibox.h + jbox.h <= H:
        jbox.y = ibox.h
    elif ibox.d + jbox.d <= D:
        jbox.z = ibox.d
    else:
        return False
      
    return True

def fits2p(ibox, jbox, W, H, D):
    if ibox.w + jbox.w <= W:
        return True
    if ibox.h + jbox.h <= H:
        return True
    if ibox.d + jbox.d <= D:
        return True
    
    return False

def fits3(ibox, jbox, kbox, W, H, D, packtype):
    """all coordinates are initialized to zero, so just adjust changes!
    the 3-box solution can either be cut by guillotine cuts"""
#   box *t;
#   itype w, h, d, r;

    # cut (ibox, jbox) and (kbox) in one of three dimensions
    for i in range(1, 4):
        w = W - kbox.w; h = H - kbox.h; d = D - kbox.d; 
        if (ibox.w <= w) and (jbox.w <= w) and fits2(ibox, jbox, w, H, D):
            kbox.x = w; return True
        if (ibox.h <= h) and (jbox.h <= h) and fits2(ibox, jbox, W, h, D):
            kbox.y = h; return True
        if (ibox.d <= d) and (jbox.d <= d) and fits2(ibox, jbox, W, H, d):
            kbox.z = d; return True
         
        box = ibox; ibox = jbox; jbox = kbox; kbox = box;
    
    # or by a sticky arrangement which is not guillotine packable
    if (packtype != GENERAL) and (packtype != ROBOT):
        return False
    
    # (xi,yi,zi) = (0,0,0); (xj,yj,zj) = (wi,0,0); (xk,yk,zk) = (0,hi,dj)
    if (ibox.w + jbox.w <= W) and (ibox.h + kbox.h <= H) and (jbox.d + kbox.d <= D):
        jbox.x = ibox.w; kbox.y = ibox.h; kbox.z = jbox.d; return True;
    
    # (xi,yi,zi) = (0,0,0); (xj,yj,zj) = (wk,0,di); (xk,yk,zk) = (0,hi,0)
    if (jbox.w + kbox.w <= W) and (ibox.h + kbox.h <= H) and (ibox.d + jbox.d <= D):
        jbox.x = kbox.w; jbox.z = ibox.d; kbox.y = ibox.h; return True;
    
    # (xi,yi,zi) = (0,0,0); (xj,yj,zj) = (0,hi,dk); (xk,yk,zk) = (wi,0,0)
    if (ibox.w + kbox.w <= W) and (ibox.h + jbox.h <= H) and (kbox.d + jbox.d <= D):
        jbox.y = ibox.h; jbox.z = kbox.d; kbox.x = ibox.w; return True;
    
    # (xi,yi,zi) = (0,0,0); (xj,yj,zj) = (0,hi,0); (xk,yk,zk) = (wj,0,di)
    if (jbox.w + kbox.w <= W) and (ibox.h + jbox.h <= H) and (kbox.d + ibox.d <= D):
        jbox.y = ibox.h; kbox.x = jbox.w; kbox.z = ibox.d; return True;
    
    # (xi,yi,zi) = (0,0,0); (xj,yj,zj) = (wi,0,0); (xk,yk,zk) = (0,hj,di) 
    if (ibox.w + jbox.w <= W) and (jbox.h + kbox.h <= H) and (ibox.d + kbox.d <= D): 
        jbox.x = ibox.w; kbox.y = jbox.h; kbox.z = ibox.d; return True;
    
    # (xi,yi,zi) = (0,0,0); (xj,yj,zj) = (0,0,di); (xk,yk,zk) = (wi,hj,0) 
    if (ibox.w + kbox.w <= W) and (jbox.h + kbox.h <= H) and (ibox.d + jbox.d <= D): 
        jbox.z = ibox.d; kbox.x = ibox.w; kbox.y = jbox.h; return True;
    
    return False 