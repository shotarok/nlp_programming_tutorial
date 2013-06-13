# -*- coding:utf-8 -*-

from collections import defaultdict

def predict_one(weight, phi):
    """
    predict a binary label from weight and feature vector.
    
    @param weight : weight hash, which has default fungtion is lambda : 0.
    @param phi    : feature hash, which has default fungtion is lambda : 0.
    """
    score = 0.0
    # Asume that weight and phi is
    # a hash whose default fungtion is lambda : 0.0.
    for name, value in phi.items():
        score += weight[name] * value

    if score >= 0:
        return 1
    return -1
    
    
