#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from flask import Flask, render_template, request, json
from bot_utils import check_document, check_name, verify_webhook, do_conversational_flow, create_bot
from file_utils import read_file, save_state
from predictor import load_encoder, load_model, load_vector
from preprocess import get_stemmer, get_stopwords
from vars import *

#region Cargar modelos y Stemmer. Estado inicial
"""Estado"""
save_state(STATE_WELCOME)
"""Fin de Estado"""

"""Cargamos los modelos y Stemmer"""
nltk.download('punkt')
nltk.download('stopwords')
model = load_model()
target = load_encoder()
encoder = load_encoder()
vector = load_vector()
stemmer = get_stemmer()
"""Fin de carga de modelos y Stemmer"""
#endregion

#region Crear clase Bot
bot = create_bot()
utterances = read_file('utterances.txt')
#endregion

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Chatbot Medical")

@app.route("/webhook", methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return verify_webhook(request)
    elif request.method == 'POST':
        return do_conversational_flow(bot, request, utterances, model, encoder, vector, stemmer, get_stopwords())
    else:
        return 'Error de solicitud'

@app.route("/testwebhook", methods=['POST', 'GET'])
def testwebhook():
    if request.method == 'GET':
        return verify_webhook(request)
    elif request.method == 'POST':
        return do_conversational_flow(bot, request, utterances, model, encoder, vector, stemmer, get_stopwords())
    else:
        return 'Error de solicitud'

if __name__ == "__main__":
    app.run(debug=True)