import random
from pprint import pprint
from unittest import TestCase

from box import Box, Bin
from bounds.zero import bound_zero
from bounds.first import bound_one, bound_one_x
from bounds.second import bound_two, bound_two_x
from utils import choose_boxes, rotate_problem

class Initial:
    def setUp(self):
        self.boxes = []
        self.bin = Bin(10, 10, 10)
        for i in range(20):
            box = Box(
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 10))
            self.boxes.append(box)

        print 'Bin:', self.bin
        print 'Boxes:'
        pprint(self.boxes)

class TestBounds(Initial, TestCase):
    def test_bound(self):
        print 'L_0:', bound_zero(self.bin, self.boxes)

    def test_bound_one_x(self):
        print 'L_1x:', bound_one_x(self.bin, self.boxes)

    def test_bound_one(self):
        self.test_bound()
        print 'L_1:', bound_one(self.bin, self.boxes)

    def test_bound_two_x(self):
        print 'L_2x:', bound_two_x(self.bin, self.boxes)

    def test_bound_two(self):
        self.test_bound_one()
        print 'L_2:', bound_two(self.bin, self.boxes)

class TestUtils(Initial, TestCase):
    def test_choose_boxes(self):
        w2 = self.bin.w/2
        d2 = self.bin.d/2
        boxes = choose_boxes(self.boxes, w2, d2)
        print 'Choose boxes W > %s and D > %s' % (w2, d2)
        pprint(boxes)

    def test_rotate_problem(self):
        rotate_problem(self.bin, self.boxes)
        print 'Rotate problem'
        pprint(self.bin)
        pprint(self.boxes)
