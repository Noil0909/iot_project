from setting import SETTING
#import socket
#import socketio #pip install python-socketio
import secrets
import asyncio
#import aiohttp #pip install aiohttp
#from aiohttp import web
from aiohttp_session import setup #pip install aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage #pip install cryptography
#from jinja2 import Environment, FileSystemLoader #pip install Jinja2
import json
#import psutil #pip install psutil
#import subprocess
from common import web, app  # socket_events.py에서 sio 인스턴스를 가져옵니다.
from request_handlers import mainHandle, temperatureHandle, pianoHandle, smarthomeHandle # request_handlers.py에서 mainHandle 함수를 가져옵니다.
import socket_events
# 암호화 키 설정
SETTING['SECRET_KEY'] = secrets.token_bytes(32)
# 세션 미들웨어 설정
setup(app, EncryptedCookieStorage(SETTING['SECRET_KEY'], cookie_name=SETTING['COOKIE_NAME']))
async def web_server():
    app.router.add_static('/static/', path='static/', name='static')    
   
    app.router.add_get('/', mainHandle)
    app.router.add_get('/temperature', temperatureHandle)
    # 피아노
    app.router.add_get('/piano', pianoHandle)
    # 스마트홈
    app.router.add_get('/smarthome', smarthomeHandle)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'http://본인아이피:5000', 5000) # http://본인아이피:5000
    await site.start()

async def main():
    try:
        await web_server()  # 웹 서버 시작
        # 무한 루프로 서버가 계속 실행되도록 유지
        while True:
            await asyncio.sleep(3600)  # 예시로, 1시간마다 대기를 풀고 다시 대기함
    except KeyboardInterrupt:
        print("프로그램이 사용자에 의해 종료됨.")
    except Exception as e:
        print(f"예외 발생: {e}")
       
if __name__ == '__main__':
    asyncio.run(main())