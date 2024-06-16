import RPi.GPIO as GPIO

BLUE_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_PIN, GPIO.OUT)

def start_led():
    GPIO.output(BLUE_PIN, GPIO.HIGH)

def stop_led():
    GPIO.output(BLUE_PIN, GPIO.LOW)

def led_state():
    return GPIO.input(BLUE_PIN)