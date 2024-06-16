import board
import adafruit_dht
import asyncio
import time
import threading
# DHT22 센서 설정 (GPIO 18)
dht_device = adafruit_dht.DHT22(board.D18)
# 스레드 중지를 위한 플래그
is_temperature = False
temperature_thread = None
humidity = 0
humidity = 0

async def send_temperature_data(sio, data, sid):
    #클라이언트한테 수신(비동기)
    await sio.emit('ret_temperature', data, room=sid)
def cycle_temperature(sio, sid):
    global is_temperature, temperature_thread
   
    while is_temperature :
        try:
            # 센서에서 온도와 습도 읽기
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            # 데이터 출력
            if humidity is not None and temperature is not None:
                print(f'온도: {temperature:.1f}°C')
                print(f'습도: {humidity:.1f}%')
            else:
                humidity = 0
                temperature = 0
            data = {
                "humidity" : humidity,
                "temperature" : temperature
            }
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # 이벤트 루프 내에서 비동기 함수 실행
            try:
                loop.run_until_complete(send_temperature_data(sio, data, sid))
            finally:
                loop.close()
        except RuntimeError as error:
            # 센서에서 데이터를 읽는 중 오류 발생 처리
            print(error.args[0])
       
        except Exception as error:
            dht_device.exit()
            raise error
        # 10초 동안 대기
        time.sleep(2)
async def start_temperature(sio, sid):
    global is_temperature, temperature_thread
    if temperature_thread is None or not temperature_thread.is_alive():
        is_temperature = True
        temperature_thread = threading.Thread(target=cycle_temperature, args=(sio, sid))
        temperature_thread.start()