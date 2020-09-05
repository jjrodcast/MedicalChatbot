#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vars import *
from pymessenger import Bot, Element
from predictor import predict_intent
from random import choice
from file_utils import *

def check_document(text):
    """ Verifica si el texto ingresado es un documento válido"""
    text = text.strip()
    is_numeric = True if text.isnumeric() and len(text) == DOC_MAX_LENGTH else False
    #reply = "next_question" if is_numeric else False
    return is_numeric

def check_name(text):
    """ Verifica si el texto ingresado es un nombre válido """
    text = text.strip()
    is_alpha = text.replace(' ', '').isalpha()
    #reply = "next_question" if is_alpha else "try_again"
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
    estado = Leer_Estado()
    if conversation_type == TYPE_MESSAGE_CODE:
      if estado == "Saludo_Inicio":
          intent = predict_intent(text, model, encoder, vector, stemmer, stopwords) # Realizamos la predicción
          if intent == PREDICT_WELCOME: #si el intent es saludo_inicial
            chatbot_reply = "Hola!, un gusto saludarte. Soy MedCheck, ¿Con cuál de las dos opciones te puedo ayudar?"
            bot.send_text_message(sender_id, chatbot_reply)
            buttons = [{"type":"phone_number", "title":"Emergencia", "payload":"+51990092571"}, {"type":"postback", "title":"Agendar Consulta Médica", "payload":"consulta"}]
            bot.send_button_message(sender_id, "Selecciona una opción", buttons)
          else: #si el intent es cualquier otra cosa que no sea saludo_inicial
            chatbot_reply = "Dejame primero introducirme. Soy MedCheck y tengo estas dos opciones con las que te puedo ayudar."
            buttons = [{"type":"phone_number", "title":"Emergencia", "payload":"+51990092571"}, {"type":"postback", "title":"Agendar Consulta Médica", "payload":"consulta"}]
            bot.send_button_message(sender_id, "Selecciona una opción", buttons)
            bot.send_text_message(sender_id, chatbot_reply)
      elif estado == "Solicita_DNI":
          if check_document(text) == False:
            chatbot_reply = "Uy, el formato es incorrecto. Por favor vuelve a ingresar tu DNI"
            bot.send_text_message(sender_id, chatbot_reply)
            Guardar_Estado("Solicita_DNI")
          else:
            chatbot_reply = "¿Cuál es tu Nombre?"
            bot.send_text_message(sender_id, chatbot_reply)
            Guardar_Estado("Solicita_Nombre") 
      elif estado == "Solicita_Nombre":
          if check_name(text) == False:
            chatbot_reply = "Uy, el formato es incorrecto. Por favor vuelve a ingresar tu Nombre"
            bot.send_text_message(sender_id, chatbot_reply)
            Guardar_Estado("Solicita_Nombre")
          else:
              chatbot_reply = "¿Cuál es tu Apellido?"
              bot.send_text_message(sender_id, chatbot_reply)
              Guardar_Estado("Solicita_Apellido")    
      elif estado == "Solicita_Apellido":
          if check_name(text) == False:
            chatbot_reply = "Uy, el formato es incorrecto. Por favor vuelve a ingresar tu Apellido"
            bot.send_text_message(sender_id, chatbot_reply)
            Guardar_Estado("Solicita_Apellido")
          else:
            chatbot_reply = "Listo!, ahora pasemos a registrar tus síntomas. Cuéntame, ¿cuáles son?"
            bot.send_text_message(sender_id, chatbot_reply)
            Guardar_Estado("Solicita_Sintomas")
      elif estado == "Solicita_Sintomas":
          sintoma = predict_intent(text, model, encoder, vector, stemmer, stopwords) # Realizamos la predicción
          if sintoma == "sintoma_asma":
            chatbot_reply = "En base a lo que nos has contado, te recomendamos los siguientes especialistas."
            bot.send_text_message(sender_id, chatbot_reply)
            elements = [{
                "title":"Doctor 1",
                "image_url":"https://petersfancybrownhats.com/company_image.png",
                "subtitle":"Especialista en traumatología",
                "buttons":[{
                    "type":"web_url",
                    "url":"https://petersfancybrownhats.com",
                    "title":"Revisa su Curriculum"},
                    {
                    "type":"postback",
                    "title":"Agendar",
                    "payload":"doctor1"
                  }]}, {
                "title":"Doctor 2",
                "image_url":"https://petersfancybrownhats.com/company_image.png",
                "subtitle":"Especialista en hipertensión",
                "buttons":[{
                    "type":"web_url",
                    "url":"https://petersfancybrownhats.com",
                    "title":"Revisa su Curriculum"},
                    {
                    "type":"postback",
                    "title":"Agendar",
                    "payload":"doctor2"
                  }]}]
            bot.send_generic_message(sender_id, elements) 

        ##if intent == PREDICT_WELCOME:
        ##    send_text_message(bot, sender_id, choose_utterance(intent, utterances))
        ##    send_text_message(bot, sender_id, choose_utterance('solicita_datos_inicio', utterances))
        ##    send_text_message(bot, sender_id, choose_utterance('solicita_dni', utterances))
        ##elif intent == PREDICT_FAREWELL:
        ##    send_text_message(bot, sender_id, choose_utterance(intent, utterances))
        ##else:# Se está prediciendo un sintoma
        ##    send_text_message(bot, sender_id, choose_utterance(intent, utterances))
        ##    create_doctors_temp(bot, sender_id)

    elif conversation_type == TYPE_POSTBACK_CODE:
      if text == "+51990092571":
        chatbot_reply = "Llamando a Emergencia..."
        bot.send_text_message(sender_id, chatbot_reply)
        Guardar_Estado("Saludo_Inicio")
      elif text == "consulta":
        chatbot_reply = "De acuerdo, para comenzar ayúdame con la siguiente información."
        bot.send_text_message(sender_id, chatbot_reply)
        chatbot_reply = "¿Cuál es el número de tu DNI?"
        bot.send_text_message(sender_id, chatbot_reply)
        Guardar_Estado("Solicita_DNI")
      elif text == "doctor1":
        chatbot_reply = "Bien!, has seleccionado al Doctor 1"
        bot.send_text_message(sender_id, chatbot_reply)
      elif text == "doctor2":
        chatbot_reply = "Bien!, has seleccionado al Doctor 2"
        bot.send_text_message(sender_id, chatbot_reply)        
        
        
       # response = ""
       # if text == OPTION_EMERGENCY_CALL:
       #     response = CALL_REPLAY
       # elif text == OPTION_DOCTOR_SELECTED:
       #     response = QUERY_REPLAY
       # else:# Se está consultando por un doctor
       #     response = DOCTOR_REPLAY.format(text)     
       # send_text_message(bot, sender_id, response)
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

"""
def enable_prediction(sender_id):
    # Leemos en que paso se quedó el bot
    name = f'step_{sender_id}.json'
    step = read_json(name)
    last_step = step['last_step']

    step = last_step.split('_')[-1]
    possibles = ['saludo', 'sintoma', 'despedida']

    if step in possibles:
        return False if step == possibles[1] else True
    return True
"""
#region Funciones para enviar mensajes del bot por medio de Facebook
def create_bot():
    return Bot(ACCESS_TOKEN_TEST)

def send_text_message(bot, sender_id, utterance):
    bot.send_text_message(sender_id, utterance)

def send_button_message(bot, sender_id, buttons):
    bot.send_button_message(sender_id, "Selecciona una opción", buttons)

def send_carrusel_message(bot, sender_id, items):
    bot.send_generic_message(sender_id, items)

def create_doctors_temp(bot, sender_id):
    elements = [
        {
            "title":"Doctor 1",
            "image_url":"https://petersfancybrownhats.com/company_image.png",
            "subtitle":"Especialista en traumatología",
            "buttons":[
                {
                    "type":"web_url",
                    "url":"https://petersfancybrownhats.com",
                    "title":"Revisa su Curriculum"
                },
                {
                    "type":"postback",
                    "title":"Agendar",
                    "payload":"Doctor1"
                }
        ]}, 
        {
            "title":"Doctor 2",
            "image_url":"https://petersfancybrownhats.com/company_image.png",
            "subtitle":"Especialista en hipertensión",
            "buttons":[
                {
                    "type":"web_url",
                    "url":"https://petersfancybrownhats.com",
                    "title":"Revisa su Curriculum"
                },
                {
                    "type":"postback",
                    "title":"Agendar",
                    "payload":"Doctor2"
                }
        ]}
    ]
    send_carrusel_message(bot, sender_id, elements)
#endregion