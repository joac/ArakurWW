"""Este Archivo contiene los modelos de datos para utilizar en la aplicacion"""

from elixir import *
import datetime

class Digital_IO(Entity):
    """Las Entradas/salidas digitales"""
    
    using_options(tablename='digital_IOs')
    
    name = Field(Unicode(30))
    status = Field(Binary)
    address = Field(Integer, primary_key=True)
    description = Field(UnicodeText)
    group = Field(Unicode(30))
    type = Field(Binary) #0 si es solo lectua
    last_change = Field(DateTime, default=datetime.datetime.now)

class Analog_IO(Entity):
    """Las Entradas/salidas analogicas"""
    
    using_options(tablename='analog_IOs')
    
    name = Field(Unicode(30))
    status = Field(Binary)
    address = Field(Integer, primary_key=True)
    description = Field(UnicodeText)
    group = Field(Unicode(30))
    value = Field(Integer) 
    last_change = Field(DateTime, default=datetime.datetime.now)

class Events(Entity):
    """Los Eventos"""
    
    using_options(tablename='events')
    
    description = Field(UnicodeText)
    cicle_time = Field(Integer)
    timestamp = Field(DateTime, default=datetime.datetime.now)

class Alarms(Entity):
    """Las Alarmas"""
    
    using_options(tablename='alarms')
    
    description = Field(UnicodeText)
    timestamp = Field(DateTime, default=datetime.datetime.now)

class Oxigen_Record(Entity):
    """Los valores historicos de Oxigeno"""
    
    using_options(tablename='oxigen_recors')
    
    value = Field(Integer)
    timestamp = Field(DateTime, default=datetime.datetime.now)

class Level_Record(Entity):
    """Los valores historicos de nivel"""
    
    using_options(tablename='level_recors')
    
    value = Field(Integer)
    timestamp = Field(DateTime, default=datetime.datetime.now)

class Cloudiness_Record(Entity):
    """Los valores historicos de turbiedad"""
    
    using_options(tablename='cloudiness_records')
    
    value = Field(Integer)
    timestamp = Field(DateTime, default=datetime.datetime.now)

