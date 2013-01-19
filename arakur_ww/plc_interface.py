#! -*-coding: utf8 -*-
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

ERROR_CODE = 0x80
M_ALARM_OFF = 23
M_STOP_SBR = 30
M_START_SBR = 31
M_RESET_VOL = 32
MARK_COUNT = 33
REGISTER_COUNT = 33

ACTUAL_PROGRAM = 8
PROGRAM_POINTER = 9 #Registro incial para escribir programas

MAX_VOL_SBR = 28

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
        'volumen_sbr': MAX_VOL_SBR,
    }

class ArakurPLC(ModbusClient):
    """Mantiene una interface de alto nivel con el PLC de operacion del SBR"""

    def detener_alarma(self):
        """Detiene la alarma"""
        response = self.write_coil(M_ALARM_OFF, True)
        return response.function_code < ERROR_CODE

    def iniciar_sbr(self):
        """Inicia el ciclo del sbr"""
        response = self.write_coil(M_START_SBR, True)
        return response.function_code  < ERROR_CODE

    def detener_sbr(self):
        """Detiene el ciclo sbr"""
        response = self.write_coil(M_STOP_SBR, True)
        return response.function_code  < ERROR_CODE

    def reset_acumulado(self):
        """Regresa la cuenta de volumen tratado a 0"""
        response = self.write_coil(M_RESET_VOL, True)
        return response.function_code  < ERROR_CODE

    def obtener_estado(self):
        marcas = self.leer_marcas()
        registros = self.leer_registros()
        #manejar la logica de novedades
        state = {}
        self._procesar_alarmas(state, marcas)
        self._procesar_eventos(state, marcas)
        self._procesar_valores_instantaneos(state, registros)
        self._procesar_programas(state, registros)
        return state

    def _procesar_alarmas(self, state, marcas):
        state['alarms'] = []
        for alarma, registro in alarms.iteritems():
            if marcas[registro]:
                state['alarms'].append(alarma)

    def _procesar_eventos(self, state, marcas):
        state['events'] = []
        for evt, registro in notificaciones.iteritems():
            if marcas[registro]:
                state['events'].append(evt)

    def _procesar_valores_instantaneos(self, state, registros):
        state['instant_values'] = {}
        for element, registro in niveles.iteritems():
            state['instant_values'][element] = registros[registro]

    def _procesar_programas(self, state, registros):
        state['programs'] = []
        values =  ['carga_aireada', 'aireacion', 'sedimentacion', 'descarga']
        for n in xrange(0, 4):
            program = {}
            for i, key in enumerate(values):
                registro = PROGRAM_POINTER + 4 * n + i
                program[key] = registros[registro]

            state['programs'].append(program)

    def leer_marcas(self):
        """Lee las marcas de memoria del twido"""
        response = self.read_coils(0, MARK_COUNT)
        if response.function_code < ERROR_CODE:
            return response.bits
        else:
            return False

    def leer_registros(self):
        """Lee los valores de todos los registros"""

        response = self.read_input_registers(0, REGISTER_COUNT)
        if response.function_code < ERROR_CODE:
            return response.registers
        else:
            return False

    def actualizar_programa(self, numero, carga_aireada, aireacion, sedimentacion, descarga):
        """Actualiza la configuracion para el programa dado."""
        if numero in xrange(1, 5):
            direccion = PROGRAM_POINTER + (numero - 1) * 4 #Aritmetica para escribir el programa

            response = self.write_registers(direccion, [carga_aireada, aireacion, sedimentacion, descarga])
            return response.function_code < ERROR_CODE
        return false

    def cambiar_programa(self, valor):
        return self._escribir_registro(ACTUAL_PROGRAM, valor)


    def configurar_volumen_maximo(self, valor):
        return self._escribir_registro(MAX_VOL_SBR, valor)


    def actualizar_niveles(self, min_oxigeno, max_oxigeno, max_turbiedad):

        response = self.write_registers(OXIGEN_MIN, [min_oxigeno, max_oxigeno, max_turbiedad])

        return response.function_code < ERROR_CODE


    def _escribir_registro(self, numero, valor):
        response = self.write_register(numero, valor)
        return response.function_code  < ERROR_CODE

    def iniciar_programa(self, programa):
        self.cambiar_programa(programa)
        self.iniciar_sbr()

