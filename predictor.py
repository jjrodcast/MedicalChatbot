#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from preprocess import *

def load_model():
    model = None
    with open('mlmodels/model_decision_tree.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def load_encoder():
    encoder = None
    with open('mlmodels/label_encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    return encoder

def load_vector():
    vector = None
    with open('mlmodels/model_vector_tfidf.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def predict_intent(text, model, encoder, vector, stemmer, stopwords):
    text = preprocess(text, stemmer, stopwords)
    input = vector.transform([text])
    intent = encoder.inverse_transform(model.predict(input))[0]
    return intent