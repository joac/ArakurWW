#! -*-coding: utf8 -*-

import json
import math

def remote_plc_command(function_name, *args, **kwargs):
    """Convierte los argumentos en un JSON, para poder llamar una
    funcion remotamente usando pubsub de Redis"""

    data = {
            'name': function_name,
            'args': args,
            'kwargs' : kwargs,
            }
    return json.dumps(data)

def execute_command(instance, message):
    """Ejecuta un metodo de instance, a partir de un json generado
    con remote_plc_command"""

    c = json.loads(message)
    return getattr(instance, c['name'])(*c['args'], **c['kwargs'])

def programas_validos():
    """devuelve una lista de programas validos"""
    return [1, 2, 3]

def programa_valido(programa):
    """devuelve un booleano para saber si es un numero válido de programa"""
    return programa in programas_validos()


def generar_onda(componentes):
    """Generador por sintesis para generar ondas complejas"""
    n = 1
    while True:
        total = 0
        for index, value in enumerate(componentes):
            if index % 2:
                total += math.sin(n * value)
            else:
                total += math.cos(n * value)
        yield 50 + (50 * (total / len(componentes)) * math.cos(0.1*n))
        n += 0.1
        n %= 2000

