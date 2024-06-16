import RPi.GPIO as GPIO

SENSOR_PIN = 17  

GPIO.setmode(GPIO.BCM) 
GPIO.setup(SENSOR_PIN, GPIO.IN) 

def read_light_sensor():
    return GPIO.input(SENSOR_PIN)
