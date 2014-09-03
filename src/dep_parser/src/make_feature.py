#! /usr/bin/env python

from collections import defaultdict
import dparser_util as util

def make_tag(kinds, tokens):
    kinds = map(str, kinds)
    tokens = map(str, tokens)
    return ",".join(map(lambda x: "".join(x), zip(kinds, tokens)))

def make_feature(stack, queue):
    phi = defaultdict(lambda : 0.0)
    W0, W1, W2 = queue[0].word, stack[-1].word, stack[-2].word
    P0, P1, P2 = queue[0].pos, stack[-1].pos, stack[-2].pos
    phi[make_tag((util.W2, util.W1), (W2, W1))] = 1
    phi[make_tag((util.W2, util.P1), (W2, P1))] = 1
    phi[make_tag((util.P2, util.W1), (P2, W1))] = 1
    phi[make_tag((util.P2, util.P1), (P2, P1))] = 1
    phi[make_tag((util.W1, util.W0), (W2, W0))] = 1
    phi[make_tag((util.W1, util.P0), (W1, P0))] = 1
    phi[make_tag((util.P1, util.W0), (P1, W0))] = 1
    phi[make_tag((util.P1, util.P0), (P1, P0))] = 1
    return phi
