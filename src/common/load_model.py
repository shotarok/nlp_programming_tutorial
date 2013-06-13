# -*- coding:utf-8 -*-

def load_model(probability, model_filename = 'model.txt'):
    fin = open(model_filename)
    for line in iter(fin.readline, ""):
        ngram_and_prob = line.rstrip('\n').split()
        prob  = ngram_and_prob.pop()
        ngram = " ".join(ngram_and_prob)
        probability[ngram] = float(prob)
