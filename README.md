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
To aquire data from PLC, we made a MODBUS/TCP client conection, and poll for data ever half second.
In this step all data is pushed in json format througth a event-stream connection to brower, updating graphs and aplication info.

## How to test application
Yo need to have following packages installed:
 
 * Python 2.6 or 2.7 (preferred) 
 * Redis: http://redis.io
 * Python distribute #FIXME ¿Is virtualenv there??

### How to get this thing working

 * Create a new virtualenv for application: virtualenv env
 * Install requirements: pip install -r requirements.txt
 * Start redis (if you not started it yet)
 * Configure redis connection on arakur_ww/config.py
 * Start PLC mock: python mock_planta/server.py
 * Start adquisition daemon python arakur_ww/daemon.py 
 * Start Web server python arakur_ww/arakur_ww.py
 * Enter to http://localhost:5000 using a modern browser


## Production deploy

Target linux is Ubuntu 12.10

 * Install dependencies 
 * Create a new user "hmi"
 * Clone repository inside home directory of this user
 * Add execution rights to web.py and adquisitor.py (chmod +x)
 * Copy upstart jobs from upstart_jobs to /etc/init
 * Start jobs, manually: start sbr_daemon, start sbr_web
   
 
## FAQ

### Where is the PLC program?
Sorry, I only develop the HMI, but, if you write to the apropiate Modbus registers, (defined in arakur_ww/constants.py), everything have to work well


### Why you have twisted, and serve the application with Flask?

Is a design choice, Because flask is really confortable to work with, and really, web app and adquisition daemon are different services.

### Why this FAQ?

Because... you are reading It.

