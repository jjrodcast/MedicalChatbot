#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from flask import Flask, render_template, request, json
from bot_utils import check_document, check_name, verify_webhook, do_conversational_flow, create_bot
from file_utils import read_file
from predictor import load_encoder, load_model, load_vector
from preprocess import get_stemmer, get_stopwords
from vars import *

#region Cargar modelos y Stemmer
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

def process_message(text):
    """ Esta función es una prueba, tiene que ser removida en caso se quiera realizar
        una tarea más genérica.
    """
    message = text.lower()
    if message == "hola":
        chatbot_reply = "Hola!, un gusto saludarte. ¿Cómo te puedo ayudar?"
    elif message == "quiero agendar una cita médica":
        chatbot_reply = "Claro!, ¿Cuáles son tus síntomas?"
    return chatbot_reply

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Chatbot Medical")

@app.route("/webhook", methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return verify_webhook(request)
    elif request.method == 'POST':
        return do_flow_conversational(request)
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