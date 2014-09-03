#! /usr/bin/env python

from collections import defaultdict

def make_tag(lst):
    return ",".join(map(str, lst))

def add_trans(phi, prev, curr):
    t = make_tag(["T", prev, curr])
    phi[t] = 1

def add_emit(phi, state, word):
    t = make_tag(["E", state, word])
    phi[t] = 1
    
def create_feature(X, Y):
    phi = defaultdict(lambda : 0.0)
    length_of_Y = len(Y)
    begin, end = "<s>", "</s>"
    for i in range(length_of_Y+1):
        prev = begin if i == 0 else Y[i-1]
        curr = end if i == length_of_Y else Y[i]
        add_trans(phi, prev, curr)
    for i in range(length_of_Y):
        add_emit(phi, Y[i], X[i])
        if (i == 0 or i == length_of_Y-1):
            t = make_tag(["CAPS", Y[i]])
            phi[t] = 1
    return phi
