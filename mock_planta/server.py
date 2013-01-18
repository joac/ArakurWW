from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

identity = ModbusDeviceIdentification()
identity.VendorName = 'Joac-Automation'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/joac/ArakurWW/'
identity.ProductName = 'Servidor Test Arakur'
identity.ModelName = 'Servidor Test Arakur'
identity.MajorMinorRevision = '0.1'

marcas = ModbusSequentialDataBlock(0, [0] * 34)
registros = ModbusSequentialDataBlock(0, [0] * 34)



store = ModbusSlaveContext(di = marcas, co= marcas, hr = registros, ir =registros)

context = ModbusServerContext(slaves=store, single=True)


StartTcpServer(context, identity=identity, address=("localhost", 5020))

