from tools import crypto

private_key = crypto.read_pem("Test", type="private")

encrypted_text = open("encrypt_message.txt", "rb").read()

raw_text = crypto.decrypt_text(private_key, encrypted_text)

print(raw_text)