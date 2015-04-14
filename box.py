class Box:
    x = y = z = 0
    def __init__(self, w, h, d):
        w, d, h = float(w), float(d), float(h)
        self.w, self.d, self.h = w, d, h
        self.volume = w * d * h

    def rotate(self):
        w = self.w; self.w = self.h; self.h = self.d; self.d = w;
        x = self.x; self.x = self.y; self.y = self.z; self.z = x;

    def __repr__(self):
        return '%sx%sx%s (%s, %s, %s)' % (self.w, self.h, self.d, self.x, self.y, self.z)

class Bin(Box): pass