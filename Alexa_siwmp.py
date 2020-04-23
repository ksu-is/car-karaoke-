

#This is code for sensing moisture of plants on raspberry pi
#!/usr/bin/python3

LIGHT_PIN = 20
PUMP_PIN = 12

import threading
import schedule
import time
import atexit

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

GPIO.setmode(GPIO.BCM)

GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(PUMP_PIN, GPIO.OUT)

class GardenerAction(object):
	turnOn = "on"
	turnOff = "off"

def threaded(job_func, action=GardenerAction.turnOn, forLength=None):
    job_thread = threading.Thread(target=job_func, kwargs={'action': action, 'forLength': forLength})
    job_thread.start()

#def water(action=GardenerAction.turnOn, forLength=None):
	#toggleComponent(PUMP_PIN, action, forLength)

def light(action=GardenerAction.turnOn, forLength=None):
	toggleComponent(LIGHT_PIN, action, forLength)

def toggleComponent(pin, action=GardenerAction.turnOn, forLength=None):
	if (forLength is not None):
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(forLength)
		GPIO.output(pin, GPIO.LOW)
	else:
		if action == GardenerAction.turnOn: GPIO.output(pin, GPIO.HIGH)
		else: GPIO.output(pin, GPIO.LOW)

def exit_handler():
    GPIO.cleanup()

atexit.register(exit_handler)



# Turn water on every 30 minutes for 10 seconds
schedule.every(30).minutes.do(threaded, water, forLength=10)

# Other scheduling examples
#schedule.every().hour.do(threaded, light, forLength=300)
#schedule.every().day.at("10:30").do(threaded, light, action=GardenerAction.turnOn)
#schedule.every().day.at("12:30").do(threaded, light, action=GardenerAction.turnOff)
#schedule.every().monday.do(threaded, water, forLength=30)
#schedule.every().wednesday.at("13:15").do(threaded, light, forLength=30)




while True:
    schedule.run_pending()
    time.sleep(1)


from time import sleep
import RPi.GPIO as GPIO
from pi_sht1x import SHT1x

def moisture():
    mqtt = MQTT() 
    mode = GPIO.BCM
    with SHT1x(12, 8, vdd="5V") as sensor_one:
        temp = sensor_one.read_temperature()
        humidity = sensor_one.read_humidity(temp)
        sensor_one.calculate_dew_point(temp, humidity)
        print(sensor_one)
        f.write("%s," % str(temp))
        f.write("%s\n" % str(humidity))
        f.close()
        sleep(2)

    with SHT1x(18, 16, vdd="5V") as sensor_two:
        temp = sensor_two.read_temperature()
        humidity = sensor_two.read_humidity(temp)
        sensor_two.calculate_dew_point(temp, humidity)
        mqtt("hackeriet/plant0/temperature", temp)
        mqtt("hackeriet/plant0/humidity", humidity)
        f = open("/home/pi/plant_mon/plant0", "w")
        f.write("%s," % str(temp))
        f.write("%s\n" % str(humidity))
        f.close()
        print(sensor_two)
        sleep(2)

if __name__ == "__main__":
    main()
    
    
 #This is code to send the data from raspberry pi to alexa
#logging into alexa 
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
coloredlogs.DEFAULT_FIELD_STYLES = {
	'hostname': {'color': 'purple'},
	'programname': {'color': 'cyan'},
	'name': {'color': 'blue'},
	'levelname': {'color': 'magenta', 'bold': True},
	'asctime': {'color': 'green'}
}
coloredlogs.DEFAULT_LEVEL_STYLES = {
	'info': {'color': 'blue'},
	'critical': {'color': 'red', 'bold': True},
	'error': {'color': 'red'},
	'debug': {'color': 'green'},
	'warning': {'color': 'yellow'}
}
