#! /usr/bin/env python

from collections import namedtuple

ROOT = "ROOT"
NONE = None
SHIFT = 0
LEFT_REDUCE = 1 
RIGHT_REDUCE = 2


W2 = "W-2"
W1 = "W-1"
W0 = "W0"
P2 = "P-2"
P1 = "P-1"
P0 = "P0"

Token = namedtuple('Token', 'id word pos head')

