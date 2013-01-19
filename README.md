# Monitoring system for wasted water plant 

## Architecture

The plant is operated by a Schneider Twido PLC, that have a MODBUS TCP/IP interface to read and set parameters.

The original design of SCADA is based on QT. But to make use of new browser technologies like event-stream, flask and many others, is now completly redesigned.

Main interface is Twitter Bootstrap based flask aplication.
Data adquisition is made with a custom thread based python daemon.

Modbus comunication is provided by twisted based *pymodbus* library.
All adquired data is stored in a MySQL Database, the selected ORM is peewee, that is lightweight and simple.

## Main Data entities

 * event_log 
 * alarm_log
 * level_log
 * oxigen_log
 * cloudiness_log

## Data Adquisition Strategy
To aquire data from PLC, we made a MODBUS/TCP client conection, and poll for data every second.
In this step all data is pushed in json format througth a event-stream connection to brower, updating graphs and aplication info.
 

