import random
from pprint import pprint
from unittest import TestCase

from box import Box, Bin
from bounds.zero import bound_zero
from bounds.first import bound_one, bound_one_x
from bounds.second import bound_two, bound_two_x

from utils import choose_boxes, rotate_problem

from fits.core import fits2, fits2p, fits3

from general.core import TaskInfo, DomainPair
from general.domain import modifyandpush, popdomains
from general.general_pack import general_pack

from variables import *
from inspect import stack

class Initial:
    def setUp(self):
        self.boxes = []
        lines = file('short.txt').readlines()
        n, W, H, D = [int(i) for i in lines[0].split()]
        self.bin = Bin(W, H, D)
        # for i in range(20):
        #     box = Box(
        #         random.randint(1, 10),
        #         random.randint(1, 10),
        #         random.randint(1, 10))
        #     self.boxes.append(box)
        # self.boxes = [
        #     Box(2, 2, 2),
        #     Box(2, 2, 2),
        #     Box(3, 3, 3),
        #     Box(4, 4, 4),
        #     Box(1, 1, 1),
        #     Box(5, 3, 1),
        #     Box(1, 1, 1),
        #     Box(1, 2, 1),
        # ]
        for line in lines[1:]:
            box = Box(*[int(i) for i in line.split()])
            self.boxes.append(box)
#             print box

        # self.log()

    def log(self):
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

class TestFits(TestCase):
    def setUp(self):
        self.bin = Box(10, 10, 10)
        
        for attr in ['ibox', 'jbox', 'kbox']:
            dimentions = random.sample(range(1, 5), 3)
            box = Box(*dimentions)
            setattr(self, attr, box)
            
    def test_fits2(self):
        print fits2(
            self.ibox, self.jbox, \
            self.bin.w, self.bin.h, self.bin.d), \
            self.ibox, self.jbox
        
    def test_fits3(self):
        print fits3(
            self.ibox, self.jbox, self.kbox, \
            self.bin.w, self.bin.h, self.bin.d, \
            GENERAL), \
            self.ibox, self.jbox, self.kbox
        
class TestDomain(TestCase):
    def test_domain(self):
        print 'DomainPair:', DomainPair(0, 0, LEFT, True)
    
    def test_modifyandpush(self):
        for i in range(5):
            for j in range(5):
                modifyandpush(i, j, random.randint(1, 6), bool(random.randint(0,1)))
        
        print '-*- modifyandpush -*-'
        pprint(domain)
        pprint(relation)
        pprint(domstack)
    
    def test_popdomains(self):
        pair = domstack[10]
        popdomains(pair)
        
        print '-*- popdomains -*-'
        print pair
        pprint(domstack)

class TestGeneralPack(Initial, TestCase):
    def setUp(self):
        Initial.setUp(self)
#         self.bin = Bin(10, 10, 10)
#         self.boxes = [
#             Box(1, 1, 2),
#             Box(2, 2, 2),
#             Box(3, 3, 3),]
            # Box(4, 4, 4)]
        self.info = TaskInfo(self.boxes)
        self.log()
        
    def test_general_pack(self):
        general_pack(self.info, self.boxes)

        self.log()

        # print '-*- GeneralPack -*-'
        # pprint(domain)
        # pprint(relation)
        # pprint(domstack)
        
        