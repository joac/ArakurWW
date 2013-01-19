#! -*-coding: utf8-*-
"""Constantes que se utilizan en la interfaz con el plc"""

ERROR_CODE = 0x80
M_ALARM_OFF = 23
M_STOP_SBR = 30
M_START_SBR = 31
M_RESET_VOL = 32
MARK_COUNT = 33
REGISTER_COUNT = 33

ACTUAL_PROGRAM = 8
PROGRAM_POINTER = 9 #Registro incial para escribir programas


OXIGEN_MIN = 5
OXIGEN_MAX = 6

CLOUDINESS_MAX= 7

alarms = {
        'No hay alarmas presentes': 0,
        'Parada de emergencia': 1,
        'Generador de emergencia en marcha': 2,
        'Alto nivel en pozo de bombeo inicial': 3,
        'Alto nivel en pileta equalizadora': 4,
        'Alto nivel en reactor SBR': 5,
        'Alto nivel en pozo de bombeo de salida': 6,
        'Fallo Bomba de pozo inicial 1': 7,
        'Fallo Bomba de pozo inicial 2': 8,
        'Fallo Bomba transvase 1': 9,
        'Fallo Bomba transvase 2': 10,
        'Fallo aireador equalizadora': 11,
        'Fallo aireador SBR 1': 12,
        'Fallo aireador SBR 2': 13,
        'Fallo válvula de descarga': 14,
        'Fallo válvula de espumas': 15,
        'Fallo dosificador de cloro': 16,
        'Fallo bomba pozo salida 1': 17,
        'Fallo bomba pozo salida 2': 18,
        'Fallo bomba recirculadora': 19,
        'Oxigeno disuelto fuera de rango': 20,
        'Turbiedad fuera de rango': 21,
        'Fallo válvula de recirculación': 22,
        }

notificaciones = {
        'Reactor en carga aireada' : 25,
        'Reactor en aireacion' : 26,
        'Reactor en sedimentacion' : 27,
        'Reactor en descarga' : 28,
        'Reactor detenido' : 29,
    }

niveles = {
        'level' : 0,
        'oxigen' : 1,
        'cloudiness' : 2,
        'volumen_tratado' : 3,
        'volumen_tratado_parcial' : 4,
        'oxigen_min' : OXIGEN_MIN,
        'oxigen_max' : OXIGEN_MAX,
        'cloudiness_max' : CLOUDINESS_MAX,
        'programa_actual' : ACTUAL_PROGRAM,
        'carga_aireada' : 21,
        'aireacion' : 22,
        'sedimentacion' : 23,
        'descarga' : 24,
    }
