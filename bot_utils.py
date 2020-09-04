#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vars import *
from pymessenger import Bot, Element
from predictor import predict_intent
from random import choice

def check_document(text):
    """ Verifica si el texto ingresado es un documento válido"""
    text = text.strip()
    is_numeric = True if text.is_numeric() and len(text) == DOC_MAX_LENGTH else False
    reply = "next_question" if is_numeric else "try_again"
    return reply

def check_name(text):
    """ Verifica si el texto ingresado es un nombre válido """
    text = text.strip()
    is_alpha = text.replace(' ', '').isalpha()
    reply = "next_question" if is_alpha else "try_again"
    return reply

def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "Servicio activo"

def do_conversational_flow(bot, req, utterances, model, encoder, vector, stemmer, stopwords):
    payload = req.json
    events = payload['entry'][0]['messaging']
    conversation_type = check_message_type(events[0].keys())

    text = ""
    sender_id = ""
    for message in events:
        sender_id = get_sender_id(message)
        if conversation_type == TYPE_MESSAGE_CODE:
            text = get_message(message)
        elif conversation_type == TYPE_POSTBACK_CODE:
            text = get_postback(message)

    # Predecimos el intent del usuario
    intent = predict_intent(text, model, encoder, vector, stemmer, stopwords)

    print(text, sender_id, intent)
    sent_text_message(bot, sender_id, choose_utterance(intent, utterances))

    return "Mensaje recibido"

def check_message_type(keys):
    if TYPE_MESSAGE in keys:
        return TYPE_MESSAGE_CODE
    elif TYPE_POSTBACK in keys:
        return TYPE_POSTBACK_CODE

def get_message(message):
    return message['message']['text']

def get_postback(message):
    return message['postback']['payload']

def get_sender_id(message):
    return message['sender']['id']

def choose_utterance(intent, utterances):
    if intent in utterances.keys():
        answers = utterances[intent]
        return choice(answers)
    else: 
        return 'No entiendo'


#region Funciones para enviar mensajes del bot por medio de Facebook
def create_bot():
    return Bot(ACCESS_TOKEN_TEST)

def sent_text_message(bot, sender_id, utterance):
    bot.send_text_message(sender_id, utterance)

def send_button_message(bot, sender_id, buttons):
    bot.send_button_message(sender_id, "Selecciona una opción", buttons)

def send_carrusel_message(bot, sender_id, items):
    bot.send_genetic_message(sender_id, items)

#endregion