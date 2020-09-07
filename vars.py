import os

ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN', None)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', None)
ACCESS_TOKEN_TEST = os.environ.get('TEST_ACCESS_TOKEN', None)

DOC_MAX_LENGTH = 8
TYPE_MESSAGE = 'message'
TYPE_MESSAGE_CODE = 1
TYPE_POSTBACK = 'postback'
TYPE_POSTBACK_CODE = 2

# Opciones para las opciones de Postback
OPTION_MEDICAL_QUERY = 'consulta'
OPTION_ALL_OK = 'conforme'
OPTION_SYMPTOMS_AGAIN = 'solicita_reingresar_informacion_medica'

# Opciones para los valores de Predicción
PREDICT_WELCOME = 'saludo'
PREDICT_SYMPTOM = 'sintoma'

# Valores para respuestas de Postback
CALL_REPLAY = "Llamando a Emergencia..."

QUERY_REPLAY_INFO = "solicita_datos_inicio"
QUERY_REPLAY_ALTERNATIVE_WELCOME = "presentacion_bot_alternativa"

QUERY_REPLAY_DNI = "solicita_dni"
QUERY_REPLAY_REENTRY_DNI = "solicita_reingresar_dni"

QUERY_REPLAY_NAME = "solicita_nombre"
QUERY_REPLAY_REENTRY_NAME = "solicita_reingresar_nombre"

QUERY_REPLAY_SENCOND_NAME = "solicita_apellido"
QUERY_REPLAY_REENTRY_SECOND_NAME = "solicita_reingresar_apellido"

RESPONSE_DATA_INITIAL_OK = "ingreso_datos_inicio_ok"
RESPONSE_SYMPTOMS_OK = "conforme_informacion_medica"
RESPONSE_DATA_ALMOST_DONE = "informacion_parcial"
RESPONSE_RESERVATION_OK = "confirmacion_final"

QUERY_SYMPTOM = "solicita_informacion_medica"
QUERY_SYMPTOM_AGAIN = "solicita_reingresar_informacion_medica"

DOCTOR_REPLAY = "Bien! has seleccionado al Doctor(a): {}"
DOCTOR_CONTAINS = "doc"

SCHEDULE_VALUES = ['agenda_lunes', 'agenda_martes', 'agenda_miercoles', 'agenda_jueves', 'agenda_viernes']

QUERY_REPLAY_CONTACT_NUMBER =  "solicita_celular"
QUERY_REPLAY_REENTRY_CONTACT_NUMBER = ""

QUERY_REPLAY_EMAIL = "solicita_correo"
QUERY_REPLAY_REENTRY_EMAIL = "solicita_reingresar_correo"


DOCTOR_IMG = "https://www.latercera.com/resizer/OAVKkZIw7P9vcLBx0W7TR7RlJRM=/900x600/filters:focal(1910x1610:1920x1600)/arc-anglerfish-arc2-prod-copesa.s3.amazonaws.com/public/BIKTL5UC5FE4VAIZJMVMKDCOAI.JPG"

#region Valores de estados
STATE_WELCOME = "saludo_inicial"
STATE_DNI = "solicita_dni"
STATE_NAME = "solicita_nombre"
STATE_SECOND_NAME = "solicita_apellidos"
STATE_SYMPTOM = "solicita_sintoma"
STATE_SYMPTOM_CONFIRMATION = 'solicita_conforme'
STATE_DATE = "solicita_date_hour"
STATE_EMAIL = "solicita_email"
STATE_CONTACT_NUMBER = "solicita_phone"
STATE_FAREWELL = "saludo_despedida"
#endregion