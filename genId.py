import os
import random
import hashlib
import time
def generate_hash():
    timestamp = str(int(time.time() * 1000000))  # 현재 시간값을 마이크로초 단위로 변환
    rand_str = ''.join(random.choice('') for _ in range(16))
    return hashlib.sha256((timestamp + rand_str).encode('utf-8')).hexdigest()[:8]
   
def generate_client_id():
    if os.path.exists("client_id.txt"):
        # 파일이 존재한다면 파일을 읽어서 변수에 저장
        with open("client_id.txt", "r") as f:
            client_id = f.read().strip()
    else:
        # 파일이 존재하지 않는다면 새로운 id 생성
        # 현재 시간값을 기반으로 랜덤한 문자열 생성 후 sha256 해시 적용
        client_id = generate_hash()
        # 생성한 client_id를 파일에 저장
        with open("client_id.txt", "w") as f:
            f.write(client_id)
    return client_id
def generate_admin_id():
    if os.path.exists("admin.txt"):
        # 파일이 존재한다면 파일을 읽어서 변수에 저장
        with open("admin.txt", "r") as f:
            admin_id = f.read().strip()
    else:
        admin_id = ""
        # 생성한 admin_id를 파일에 저장
        with open("admin.txt", "w") as f:
            f.write(admin_id)
    return admin_id