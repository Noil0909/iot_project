import RPi.GPIO as GPIO
from common import get_system_info, sio  # common.py에서 get_system_info 함수, sio 변수를 가져옵니다.
from light_sensor import read_light_sensor
from led_switch import start_led, stop_led, led_state
from ultrasonic_sensor import read_ultrasonic_sensor
from buzzer import start_buzzer, stop_buzzer

@sio.event
async def connect(sid, environ):
    print('클라이언트 연결', sid)

@sio.event
async def disconnect(sid):
    print('클라이언트 종료', sid)

@sio.on('get_system_info')
async def on_get_system_info(sid, data):
    #print("클라이언트에서 받은 data", data)
    systemInfo = get_system_info()
    await sio.emit('ret_system_info', systemInfo, room=sid)

@sio.on('get_temperature')
async def on_get_temperature(sid, data):
    await start_temperature(sio, sid)
    #data['state'] = await temperature_state()

@sio.on('get_light_sensor')
async def on_get_light_sensor(sid, data):
    light_level = read_light_sensor()
    light_level_str = "HIGH" if light_level == GPIO.HIGH else "LOW"
    await sio.emit('ret_light_sensor', {'light': light_level_str}, room=sid)

@sio.on('set_led')
async def on_set_led(sid, data):
    print("set_led", data)
    if data['data'] == 'on':
        await start_led()
    elif data['data'] == 'off':
        await stop_led()
    data['state'] = led_state()
    await sio.emit('ret_led', data, room=sid)

@sio.on('get_ultrasonic_sensor')
async def on_get_ultrasonic_sensor(sid, data):
    distance = read_ultrasonic_sensor()
    await sio.emit('ret_ultrasonic_sensor', {'distance': distance}, room=sid)

@sio.on('set_buzzer')
async def on_set_buzzer(sid, data):
    print("set_buzzer", data)
    if data['data'] == 'on':
        await start_buzzer()
    elif data['data'] == 'off':
        await stop_buzzer()