#! -*-coding: utf8 -*-
import datetime
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from constants import *

class ArakurPLC(ModbusClient):
    """Mantiene una interface de alto nivel con el PLC de operacion del SBR"""
    def __init__(self, *args, **kwargs):
        self.prev_marcas = [False] * MARK_COUNT
        self.change_times = [False] * MARK_COUNT
        super(ArakurPLC, self).__init__(*args, **kwargs)

    def detener_alarma(self):
        """Detiene la alarma"""
        return self._escribir_marca(M_ALARM_OFF, True)

    def iniciar_sbr(self):
        """Inicia el ciclo del sbr"""
        return self._escribir_marca(M_START_SBR, True)

    def detener_sbr(self):
        """Detiene el ciclo sbr"""
        return self._escribir_marca(M_STOP_SBR, True)

    def reset_acumulado(self):
        """Regresa la cuenta de volumen tratado a 0"""
        return self._escribir_marca(M_RESET_VOL, True)

    def obtener_estado(self):
        marcas = self.leer_marcas()
        registros = self.leer_registros()
        state = {}
        self._procesar_alarmas(state, marcas)
        self._procesar_eventos(state, marcas)
        self._procesar_valores_instantaneos(state, registros)
        self._procesar_programas(state, registros)
        self._procesar_parametros(state, registros)
        #faltaria timestamp para la informacion
        #guardamos las marcas viejas, para poder ver si cambiaron
        self.prev_marcas = marcas
        return state

    def _procesar_alarmas(self, state, marcas):
        state['alarms'] = []
        state['new_alarms'] = []
        now_str = self._now_str()

        for alarma, registro in alarms.iteritems():

            alarm_dict = {'text':alarma, 'time':self.change_times[registro]}
            if marcas[registro] and not self.prev_marcas[registro]:
                alarm_dict['time'] = now_str
                state['new_alarms'].append(alarm_dict)
                state['alarms'].append(alarm_dict)
                self.change_times[registro] = now_str;
            elif marcas[registro]:
                #donde guardamos
                state['alarms'].append(alarm_dict)

    def _procesar_eventos(self, state, marcas):
        state['events'] = []
        state['new_events'] = []
        now_str = self._now_str()

        for evt, registro in notificaciones.iteritems():
            event_dict = {'text':evt, 'time':self.change_times[registro]}
            if marcas[registro] and not self.prev_marcas[registro]:
                event_dict['time'] = now_str
                state['events'].append(event_dict)
                state['new_events'].append(event_dict)
                self.change_times[registro] = now_str
            elif marcas[registro]:
                state['events'].append(event_dict)

    def _procesar_valores_instantaneos(self, state, registros):
        state['instant_values'] = {}
        for element, registro in niveles.iteritems():
            value = registros[registro]
            if formatters.has_key(element):
                value *= formatters[element]

            state['instant_values'][element] = value

    def _procesar_parametros(self, state, registros):
        state['params'] = {}
        for element, registro in parametros.iteritems():
            value = registros[registro]
            if formatters.has_key(element):
                value *= formatters[element]
            state['params'][element] = value

    def _procesar_programas(self, state, registros):
        state['programs'] = []
        values =  ['carga_aireada', 'aireacion', 'sedimentacion', 'descarga']
        for n in xrange(0, 3):
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
        if numero in xrange(1, 4):
            direccion = PROGRAM_POINTER + (numero - 1) * 4 #Aritmetica para escribir el programa

            response = self.write_registers(direccion, [carga_aireada, aireacion, sedimentacion, descarga])
            return response.function_code < ERROR_CODE

        return False

    def cambiar_programa(self, valor):
        return self._escribir_registro(ACTUAL_PROGRAM, valor)

    def actualizar_parametros(self, min_oxigeno, max_oxigeno, max_turbiedad):
        response = self.write_registers(OXIGEN_MIN, [min_oxigeno, max_oxigeno, max_turbiedad])
        return response.function_code < ERROR_CODE

    def _escribir_registro(self, numero, valor):
        response = self.write_register(numero, valor)
        return response.function_code  < ERROR_CODE

    def _escribir_marca(self, numero, valor):
        response = self.write_coil(numero, valor)
        return response.function_code  < ERROR_CODE

    def iniciar_programa(self, programa):
        self.cambiar_programa(programa)
        return self.iniciar_sbr()
    def _now_str(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
