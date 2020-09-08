#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from vars import *
from pymessenger import Bot, Element
from predictor import predict_intent
from random import choice
from file_utils import read_state, save_state, read_file, load_info, save_info, reload_info

def is_email(text):
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return True if re.search(regex, text) else False

def is_phone_number(text):
    phones = re.findall('(?:\+ *)?\d[\d\- ]{7,}\d', text)
    elements = [phone.replace('-', '').replace(' ', '') for phone in phones]
    return True if len(elements) > 0 else False

def capitalize(text):
    names = text.split(' ')
    return ' '.join([name.capitalize() for name in names])

def check_document(text):
    """ Verifica si el texto ingresado es un documento válido"""
    text = text.strip()
    is_numeric = True if text.isnumeric() and len(text) == DOC_MAX_LENGTH else False
    return is_numeric

def check_name(text):
    """ Verifica si el texto ingresado es un nombre válido """
    text = text.strip()
    is_alpha = text.replace(' ', '').isalpha()
    return is_alpha

def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "<center>Servicio activo</center>"

def do_conversational_flow(bot, req, utterances, model, encoder, vector, stemmer, stopwords):
    payload = req.json
    events = payload['entry'][0]['messaging']
    conversation_type = check_message_type(events[0].keys())

    text, sender_id = "", ""
    for message in events:
        sender_id = get_sender_id(message)
        if conversation_type == TYPE_MESSAGE_CODE:
            text = get_message(message)
        elif conversation_type == TYPE_POSTBACK_CODE:
            text = get_postback(message)

    # Verificamos el tipo de respuesta [texto, postback]
    current_state = read_state()
    if conversation_type == TYPE_MESSAGE_CODE:
        if current_state == STATE_WELCOME:
            intent = predict_intent(text, model, encoder, vector, stemmer, stopwords)
            if intent == PREDICT_WELCOME: #si el intent es saludo_inicial
                send_text_message(bot, sender_id, choose_utterance(intent, utterances))
                send_button_message(bot, sender_id, create_options_buttons())
                reload_info()
            else: #si el intent es cualquier otra cosa que no sea saludo_inicial
                send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_ALTERNATIVE_WELCOME, utterances))
                send_button_message(bot, sender_id, create_options_buttons())
        elif current_state == STATE_NAME:
            if check_name(text):
                save_info(text) # Guardamos el nombre
                template = choose_utterance(QUERY_REPLAY_SENCOND_NAME, utterances)
                send_text_message(bot, sender_id, template.format(text.capitalize()))
                save_state(STATE_SECOND_NAME)
            else:
                send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_REENTRY_NAME, utterances))
                save_state(STATE_NAME)
        elif current_state == STATE_SECOND_NAME:
            if check_name(text):
                template = choose_utterance(QUERY_REPLAY_DNI, utterances)
                send_text_message(bot, sender_id, template.format(load_info().capitalize()))
                save_state(STATE_DNI)
            else:
                send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_REENTRY_SECOND_NAME, utterances))
                save_state(STATE_SECOND_NAME)
        elif current_state == STATE_DNI:
            if check_document(text):
                send_text_message(bot, sender_id, choose_utterance(RESPONSE_DATA_INITIAL_OK, utterances))
                send_text_message(bot, sender_id, choose_utterance(QUERY_SYMPTOM, utterances))
                save_state(STATE_SYMPTOM)
            else:
                send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_REENTRY_DNI, utterances))
                save_state(STATE_DNI)
        elif current_state == STATE_SYMPTOM:
            intent = predict_intent(text, model, encoder, vector, stemmer, stopwords)  # Realizamos la predicción
            send_text_message(bot, sender_id, choose_utterance(intent, utterances))
            send_carrusel_message(bot, sender_id, create_doctors(intent))
        elif current_state == STATE_CONTACT_NUMBER:
            if is_phone_number(text):
                template = choose_utterance(QUERY_REPLAY_EMAIL, utterances)
                send_text_message(bot, sender_id, template.format(load_info().capitalize()))
                save_state(STATE_EMAIL)
            else:
                send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_REENTRY_CONTACT_NUMBER, utterances))
                save_state(STATE_CONTACT_NUMBER)
        elif current_state == STATE_EMAIL:
            if is_email(text):
                template = choose_utterance(RESPONSE_RESERVATION_OK, utterances)
                send_text_message(bot, sender_id, template.format(load_info().capitalize()))
                save_state(STATE_FAREWELL)
            else:
                send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_REENTRY_EMAIL, utterances))
                save_state(STATE_EMAIL)
        elif current_state == STATE_FAREWELL: # Invocar Despedida
            intent = predict_intent(text, model, encoder, vector, stemmer, stopwords)
            send_text_message(bot, sender_id, choose_utterance(intent, utterances))
            save_state(STATE_WELCOME)
    elif conversation_type == TYPE_POSTBACK_CODE:
        if is_phone_number(text):
            send_text_message(bot, sender_id, CALL_REPLAY)
            save_state(STATE_WELCOME)
        elif text == OPTION_MEDICAL_QUERY:
            send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_INFO, utterances))
            send_text_message(bot, sender_id, choose_utterance(QUERY_REPLAY_NAME, utterances))
            save_state(STATE_NAME)
        elif text.find(DOCTOR_CONTAINS) != -1:
            doctor = text.split("_")[0]
            doctor = capitalize(doctor)
            send_text_message(bot, sender_id, DOCTOR_REPLAY.format(doctor))
            send_button_message(bot, sender_id, create_confirmation_buttons(), '¿Estás conforme con tu elección?')
            save_state(STATE_SYMPTOM_CONFIRMATION)
        elif text == OPTION_ALL_OK:
            send_text_message(bot, sender_id, choose_utterance(RESPONSE_SYMPTOMS_OK, utterances))
            send_button_message(bot, sender_id, create_schedule_buttons())
            save_state(STATE_DATE)
        elif text == OPTION_SYMPTOMS_AGAIN:
            send_text_message(bot, sender_id, choose_utterance(QUERY_SYMPTOM_AGAIN, utterances))
            save_state(STATE_SYMPTOM)
        elif text in SCHEDULE_VALUES:
            send_text_message(bot, sender_id, choose_utterance(RESPONSE_DATA_ALMOST_DONE, utterances))
            template = choose_utterance(QUERY_REPLAY_CONTACT_NUMBER, utterances)
            send_text_message(bot, sender_id, template.format(load_info().capitalize()))
            save_state(STATE_CONTACT_NUMBER)
    else:
        return 'No entiendo el mensaje'
    
    return 'Mensaje recibido'

def check_message_type(keys):
    if TYPE_MESSAGE in keys:
        return TYPE_MESSAGE_CODE
    elif TYPE_POSTBACK in keys:
        return TYPE_POSTBACK_CODE

def get_message(message):
    return message['message']['text'].lower()

def get_postback(message):
    return message['postback']['payload'].lower()

def get_sender_id(message):
    return message['sender']['id']

def is_symptom_key(intent, keys):
    intent_type = intent.split('_')[0]
    for k in keys:
        ks = k.split('_')[-1]
        if ks == intent_type:
            return (True, k)
    return (False, None)

def choose_utterance(intent, utterances):
    is_symptom, rintent = is_symptom_key(intent, utterances.keys())
    if intent in utterances.keys():
        answers = utterances[intent]
        return choice(answers)
    elif is_symptom:
        answers = utterances[rintent]
        return choice(answers)
    else: 
        return 'El intent es ' + intent

#region Funciones para enviar mensajes del bot por medio de Facebook
def create_bot():
    return Bot(ACCESS_TOKEN)

def send_text_message(bot, sender_id, utterance):
    bot.send_text_message(sender_id, utterance)

def send_button_message(bot, sender_id, buttons, title="Selecciona una opción"):
    bot.send_button_message(sender_id, title, buttons)

def send_carrusel_message(bot, sender_id, items):
    bot.send_generic_message(sender_id, items)

def create_options_buttons():
    return [{"type":"phone_number", 
             "title":"Emergencia", 
             "payload":"+51990092571"}, 
            {"type":"postback", 
             "title":"Agendar Consulta Médica", 
             "payload":OPTION_MEDICAL_QUERY}]

def create_confirmation_buttons():
    return [{"type":"postback", 
             "title":"Sí, continuemos", 
             "payload": OPTION_ALL_OK}, 
            {"type":"postback", 
             "title":"No, ingresar sintomas nuevamente", 
             "payload":OPTION_SYMPTOMS_AGAIN}]

def create_schedule_buttons():
    return [
        {"type":"postback", "title":"Lunes|16:00-17:00", "payload": SCHEDULE_VALUES[0]},
        {"type":"postback", "title":"Martes|11:00-12:00", "payload": SCHEDULE_VALUES[1]}, 
        {"type":"postback", "title":"Jueves|10:00-11:00", "payload": SCHEDULE_VALUES[3]}
        ]
    
def create_doctors(intent):
    content = read_file('doctors.txt')
    doctors = content[intent]
    elements = []
    for doctor in doctors:
        values = doctor.split("|")
        elements.append(
            {
                "title": values[0],
                "image_url": DOCTOR_IMG,
                "subtitle": values[2],
                "buttons": [ 
                    { "type": "web_url", "url": "https://petersfancybrownhats.com", "title": "Revisar Curriculum" },
                    { "type": "postback", "payload": values[0]+'_'+values[1], "title": "Agendar" }
                    ]
            }
        )
    return elements
#endregion