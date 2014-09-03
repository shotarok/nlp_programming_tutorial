# -*- coding:utf-8 -*-

from collections import defaultdict
from math import copysign

def predict_one(weight, phi):
    """
    predict a binary label from weight and feature vector.
    
    @param weight : weight hash, which has default fungtion is lambda : 0.
    @param phi    : feature hash, which has default fungtion is lambda : 0.
    """
    # Asume that weight and phi is
    # a hash whose default fungtion is lambda : 0.0.
    score = get_simple_score(weight, phi)
    return copysign(1, score)
    
    
def get_simple_score(weight, phi):
    score = 0.0
    # Asume that weight and phi is
    # a hash whose default fungtion is lambda : 0.0.
    for name, value in phi.items():
        score += weight[name] * value
    return score

def getw(weight, name, c, it, last):
    if it != last[name]:
        c_size = c * (it - last[name])
        if abs(weight[name]) <= c_size:
            weight[name] = 0
        else:
            weight[name] -= copysign(c_size, weight[name])
        last[name] = it
    return weight[name]

def get_score(weight, phi, c, it, last):
    score = 0.0
    for name, value in phi.items():
        score += getw(weight, name, c, it, last)
    return score
