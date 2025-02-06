from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_key_pair(name:str):
    # 產生 RSA 私鑰
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 取得 RSA 公鑰
    public_key = private_key.public_key()

    # 將私鑰儲存為 PEM 格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 將公鑰儲存為 PEM 格式
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 儲存至檔案
    with open(f"secret/{name}_private_key.pem", "wb") as f:
        f.write(private_pem)

    with open(f"secret/{name}_public_key.pem", "wb") as f:
        f.write(public_pem)
    
    return 0

def read_pem(name, type="public"):
    pem = open(f"secret/{name}_{type}_key.pem", "rb").read()

    if type == "public":
        # 解析 PEM 格式的公鑰
        public_key = serialization.load_pem_public_key(pem)
        return public_key
    elif type == "private":
        # 解析 PEM 格式的私鑰
        private_key = serialization.load_pem_private_key(
            pem,
            password=None  # 如果私鑰有密碼，請在此輸入 bytes 格式的密碼
        )
        return private_key

# 加密函數
def encrypt_text(public_key:rsa.RSAPublicKey, message:str):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

# 解密函數
def decrypt_text(private_key:rsa.RSAPrivateKey, encrypted_message:bytes):
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()
