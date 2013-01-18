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
        pass

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

        direccion = PROGRAM_POINTER + (numero - 1) * 4 #Aritmetica para escribir el programa

        response = self.write_registers(direccion, [carga_aireada, aireacion, sedimentacion, descarga])
        return response.function_code < ERROR_CODE

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



