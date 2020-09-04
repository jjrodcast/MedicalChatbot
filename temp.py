def webhook():
  carrusel = []
  if request.method == "GET":
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
      return request.args.get("hub.challenge")
    else:
      return "No conectado a Facebook."
  elif request.method == "POST":
    payload = request.json
    event = payload['entry'][0]['messaging']
    if 'message' in event[0].keys():
      type_conv = 1
    elif 'postback' in event[0].keys():
      type_conv = 2

    for msg in event:
      sender_id = msg['sender']['id']
      if type_conv == 1:
        text = msg['message']['text']
      elif type_conv == 2:
        text = msg['postback']['payload']

    chatbot_reply = 0
    message = text.lower()
    if type_conv == 1:
      if message == "hola":
        chatbot_reply = "Hola!, un gusto saludarte. Soy MedCheck, ¿Con cuál de las dos opciones te puedo ayudar?"
        bot.send_text_message(sender_id, chatbot_reply)
        buttons = [{"type":"phone_number", "title":"Emergencia", "payload":"+51990092570"}, {"type":"postback", "title":"Agendar Consulta Médica", "payload":"Consulta"}]
        bot.send_button_message(sender_id, "Selecciona una opción", buttons)
      if message == "sintomas":
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
                "payload":"Doctor1"
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
                "payload":"Doctor2"
              }]}]
        bot.send_generic_message(sender_id, elements)          
    elif type_conv == 2:
      if message == "emergencia":
        chatbot_reply = "Llamando a Emergencia..."
        bot.send_text_message(sender_id, chatbot_reply)
      elif message == "consulta":
        chatbot_reply = "De acuerdo, ¿cuáles son tus síntomas?"
        bot.send_text_message(sender_id, chatbot_reply)
      elif message == "doctor1":
        chatbot_reply = "Bien!, has seleccionado al Doctor 1"
        bot.send_text_message(sender_id, chatbot_reply)
      elif message == "doctor2":
        chatbot_reply = "Bien!, has seleccionado al Doctor 2"
        bot.send_text_message(sender_id, chatbot_reply)
    return "Mensaje Recibido"
  else:
    return "200"