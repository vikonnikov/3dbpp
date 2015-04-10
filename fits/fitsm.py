from variables import *
from bounds.second import bound_two

def fitsm(info, boxes, fast):
    lb = bound_two(bin, boxes) 
    if (lb > 1):
        return False
    
    info.exfill += 1
    
    fits = False
    
    if info.packtype == GENERAL:
        fits = onebin_general(info, boxes, fast)
    elif info.packtype == ROBOT:
        fits = onebin_robot(a, boxes, fast)
    
    return fits