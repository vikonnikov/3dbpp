import random
from pprint import pprint, pformat
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

from logger import log, set_console_handler, set_file_handler
# set_console_handler()
set_file_handler('./py', 'w')

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

        self.log()

    def log(self):
        log.debug('Bin: %s', self.bin)
        log.debug('Boxes:')
        log.debug(pformat(self.boxes))

class TestBounds(Initial, TestCase):
    def test_bound(self):
        log.debug('L_0: %s', bound_zero(self.bin, self.boxes))

    def test_bound_one_x(self):
        log.debug('L_1x: %s', bound_one_x(self.bin, self.boxes))

    def test_bound_one(self):
        self.test_bound()
        log.debug('L_1: %s', bound_one(self.bin, self.boxes))

    def test_bound_two_x(self):
        log.debug('L_2x: %s', bound_two_x(self.bin, self.boxes))

    def test_bound_two(self):
        self.test_bound_one()
        log.debug('L_2: %s', bound_two(self.bin, self.boxes))

class TestUtils(Initial, TestCase):
    def test_choose_boxes(self):
        w2 = self.bin.w/2
        d2 = self.bin.d/2
        boxes = choose_boxes(self.boxes, w2, d2)
        log.debug('Choose boxes W > %s and D > %s', w2, d2)
        log.debug(pformat(boxes))

    def test_rotate_problem(self):
        rotate_problem(self.bin, self.boxes)
        log.debug('Rotate problem')
        log.debug(pformat(self.bin))
        log.debug(pformat(self.boxes))

class TestFits(TestCase):
    def setUp(self):
        self.bin = Box(10, 10, 10)
        
        for attr in ['ibox', 'jbox', 'kbox']:
            dimentions = random.sample(range(1, 5), 3)
            box = Box(*dimentions)
            setattr(self, attr, box)
            
    def test_fits2(self):
        log.debug(fits2(
            self.ibox, self.jbox, \
            self.bin.w, self.bin.h, self.bin.d), \
            self.ibox, self.jbox)
        
    def test_fits3(self):
        log.debug(fits3(
            self.ibox, self.jbox, self.kbox, \
            self.bin.w, self.bin.h, self.bin.d, \
            GENERAL), \
            self.ibox, self.jbox, self.kbox)
        
class TestDomain(TestCase):
    def test_domain(self):
        log.debug('DomainPair: %s', DomainPair(0, 0, LEFT, True))
    
    def test_modifyandpush(self):
        for i in xrange(5):
            for j in xrange(5):
                modifyandpush(i, j, random.randint(1, 6), bool(random.randint(0,1)))
        
        log.debug('-*- modifyandpush -*-')
        log.debug(pformat(domain))
        log.debug(pformat(relation))
        log.debug(pformat(domstack))
    
    def test_popdomains(self):
        pair = domstack[10]
        popdomains(pair)
        
        log.debug('-*- popdomains -*-')
        log.debug(pair)
        log.debug(pformat(domstack))

class TestGeneralPack(Initial, TestCase):
    def setUp(self):
        Initial.setUp(self)
#         self.bin = Bin(10, 10, 10)
#         self.boxes = [
#             Box(1, 1, 2),
#             Box(2, 2, 2),
#             Box(3, 3, 3),]
            # Box(4, 4, 4)]
        w, h, d = self.bin.w, self.bin.h, self.bin.d
        self.info = TaskInfo(w, h, d, self.boxes)
        self.log()
        
    def test_general_pack(self):
        general_pack(self.info, self.boxes)
        
        self.log()

        # log.debug('-*- GeneralPack -*-'
        # pprint(domain)
        # pprint(relation)
        # pprint(domstack)
        
        