# MQTT Transfer tool
## Using `broker.emqx.io` Server for Testing

### First setup
#### configuration file
The path of configuration file is `conf/`.
1. `conf/mqtt.json`:
   * server: The mqtt server you would like to use (by domain).
   * port: The server port you would like to use (Notice for TLS port).
   * topic: The topic you would like to subscribe (type "_secret" if you want to keep it secret, and you can setup it in the other file, mentioned below).

#### secret file
**Before this configuration, you must CREATE A DIRECTORY `secret/` IN THIS PATH**
1. In `secret/`, we could add `mqtt_topic.txt` inside if you type `_secret` in `conf/mqtt.json`.
2. Contents will NOT be tracked in this directory.
3. After finish settings the RSA encryption, the private key and public key will stored in this directory (.pem file).

#### Setup python environment
commands are shown below:
```shell
python -m venv venv
# Activate venv by using your method

pip install -r requirements.txt
```