import RPi.GPIO as GPIO

# 핀 설정
BUZZER_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def start_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    print("buzzer_on")

def stop_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    print("buzzer.off")