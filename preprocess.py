#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unidecode import unidecode
import nltk
import re
import string
from nltk.corpus import stopwords
import snowballstemmer
#from nltk.stem import SnowBallStemmer

def remove_punctiations(text):
    return re.sub('[%s]' % re.escape(string.punctuation), '',text)

def remove_accent(text):
    """Removemos los acentos de las palabras"""
    return unidecode(text).strip()

def convert_to_lower(text):
    """Cambiamos todos nuevos tokens a minusculas"""
    text = text.lower()
    return text

def remove_stopwords(text, stopwords):
    """Removemos los stopwords"""
    return [word for word in nltk.word_tokenize(text) if (word not in stopwords) and re.search('[a-zA-Z]', word)]

def stem_word(word, stemmer):
    return stemmer.stemWord(word)

def stem_text(text, stemmer, stopwords):
    """Realizamos stemming a los textos"""
    tokens = remove_stopwords(text, stopwords)
    text = [stem_word(word, stemmer) for word in tokens]
    return ' '.join(text)

def get_stemmer():
    """Retornamos el stemmer SnowBallStemer"""
    #return SnowBallStemmer('spanish')
    return snowballstemmer.stemmer('spanish')

def get_stopwords():
    """Obtener stopwords"""
    return stopwords.words('spanish')

def preprocess(text, stemmer, stopwords):
    """Realizamos pre-procesamiento del texto para la predicción"""
    text = remove_punctiations(text)
    text = remove_accent(text)
    text = convert_to_lower(text)
    text = stem_text(text, stemmer, stopwords)
    return text