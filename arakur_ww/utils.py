#! -*-coding: utf8 -*-

import json
import math
import uuid


class RemoteCommand(object):

    def __init__(self, function_name=None, *args, **kwargs):
        if function_name:
            self.id = str(uuid.uuid4())
            self.function_name = function_name
            self.args = args
            self.kwargs = kwargs

    def to_dict(self):
        data_dict = {
                'id': self.id,
                'function_name' : self.function_name,
                'args' : self.args,
                'kwargs': self.kwargs,
            }
        return data_dict

    def serialize(self):
        """Convierte los parametros a un string JSON"""
        return json.dumps(self.to_dict())

    def unserialize(self, data):
        """Popula los campos del objeto, con el string JSON provisto"""
        data_dict = json.loads(data)
        self.id = data_dict['id']
        self.function_name = data_dict['function_name']
        self.args = data_dict['args']
        self.kwargs = data_dict['kwargs']

    def execute(self, instance):
        """ejecuta el commando en la instancia dada"""
        f = getattr(instance, self.function_name)
        return f(*self.args, **self.kwargs)

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

