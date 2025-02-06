import paho.mqtt.client as mqtt
from tools import crypto

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = open("secret/mqtt_topic.txt", "r").read()

private_key = crypto.read_pem("Test", "private")
public_key = crypto.read_pem("Test", "public")

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

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 發佈加密訊息
encrypted_message = crypto.encrypt_text(public_key, "Secure MQTT Message")
client.publish(MQTT_TOPIC, encrypted_message)

client.loop_forever()
