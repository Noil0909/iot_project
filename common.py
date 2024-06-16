import psutil
import subprocess
import aiohttp
from aiohttp import web
from aiohttp_session import get_session
import socketio
import genId
from jinja2 import Environment, FileSystemLoader
from setting import SETTING

app = aiohttp.web.Application()
sio = socketio.AsyncServer(cors_allowed_origins='*')
sio.attach(app) #http와 socket.io 통합

async def session_check(request):
    session = await get_session(request)
    if 'authenticated' not in session:
        raise web.HTTPFound('/login')
    return session

def response_html(page, data=None):
    global SETTING
    try:
        rand = genId.generate_hash()
        template_loader = FileSystemLoader('html')
        template_env = Environment(loader=template_loader)
        template = template_env.get_template(page)
        if data:
            rendered_template = template.render(system_mode=SETTING['SYSTEM_MODE'], rand=rand, data=data)
        else:
            rendered_template = template.render(system_mode=SETTING['SYSTEM_MODE'], rand=rand)
        return web.Response(text=rendered_template, content_type='text/html')
    except Exception as e:
        # 오류 발생 시의 응답
        return aiohttp.web.Response(text=str(e), status=500)

''' CPU 온도를 얻는 함수 '''
def get_cpu_temperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        temp = f.read()
        temp = int(temp) / 1000  # millidegree to degree
    return temp

''' 디스크 사용량을 얻는 함수 '''
def get_disk_usage():
    try:
        df_output = subprocess.check_output(['df', '/home'], text=True)
        lines = df_output.strip().split('\n')
        if len(lines) >= 2:
            fields = lines[1].split()
            if len(fields) >= 5:
                total_disk = int(fields[1]) * 1024  # 1K 블록 단위
                used_disk = int(fields[2]) * 1024
                disk_percent = float(fields[4].replace('%', ''))
                disk_free = int(fields[3]) * 1024
                return total_disk, used_disk, disk_percent, disk_free
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None

''' 시스템 전방적인 사용량 확인 함수 '''
def get_system_info():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    total_memory = memory.total
    used_memory = memory.used
    memory_percent = memory.percent
    cpu_temp = get_cpu_temperature()
    total_disk, used_disk, disk_percent, disk_free = get_disk_usage()

    system_info = {
        'cpu_percent': cpu_percent,
        'total_memory': total_memory,
        'used_memory': used_memory,
        'memory_percent': memory_percent,
        'total_disk': total_disk,
        'used_disk': used_disk,
        'disk_percent': disk_percent,
        'cpu_temp': cpu_temp
    }

    return system_info