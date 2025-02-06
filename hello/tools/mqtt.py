import random
import string
import time
import json
import os
import base64

import paho.mqtt.client as mqtt

from tools import crypto

current_path = os.getcwd()

mqtt_conf_path = os.path.join(current_path, "conf/mqtt.json")
mqtt_conf = json.loads(open(mqtt_conf_path, "r").read())

MQTT_BROKER = mqtt_conf["server"]
MQTT_PORT = mqtt_conf["port"]
MQTT_TOPIC = mqtt_conf["topic"]

if MQTT_TOPIC == "_secret":
    mqtt_topic_path = os.path.join(current_path, "secret/mqtt_topic.txt")
    MQTT_TOPIC = open(mqtt_topic_path, "r").read()

encrypted = False
public_key:bytes
private_key:bytes

def set_key(public_key_inp, private_key_inp):
    global public_key, private_key, encrypted
    encrypted = True
    public_key = public_key_inp
    private_key = private_key_inp

def random_str(length=15):
    characters = string.ascii_letters + string.digits  # 包含大小寫字母和數字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def base64_encode(payload, is_str = False):
    if is_str:
        # 將字串轉換為 bytes
        input_bytes = str(payload).encode('utf-8')
    else:
        input_bytes = payload
    # 進行 Base64 編碼
    base64_bytes = base64.b64encode(input_bytes)
    # 將編碼結果轉回字串
    base64_string:str = base64_bytes.decode('utf-8')
    return base64_string

def base64_decode(base64_string:str, is_str = False):
    # 將 Base64 字串轉換為 bytes
    base64_bytes = base64_string.encode('utf-8')
    # 進行 Base64 解碼
    decoded_bytes = base64.b64decode(base64_bytes)

    if is_str:
        # 將解碼結果轉回字串
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    else:
        return decoded_bytes

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    encrypted_payload = msg.payload
    try:
        decrypted_payload = crypto.decrypt_text(private_key, encrypted_payload)
        print(f"Received: {decrypted_payload}")
    except Exception as e:
        print(f"Decryption error: {e}")

def send_message(msg:str):
    msg_data = {}
    if encrypted:
        # 發佈加密訊息
        msg = crypto.encrypt_text(public_key, msg)
    else:
        msg = msg.encode('utf-8')
    msg_data["data"] = base64_encode(msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)