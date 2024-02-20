# So, to keep service clean I'm going to handle encryption, decryption herer so it's nice and contained :)
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def hash_password(password: str, salt: bytes | None = None, salt_length: int | None = 32) -> tuple[bytes, bytes, bytes]:
    """Converts password into scrypt hash.

    Args:
        password (str): Target password to hash.
        salt_length (int | None, optional): Salt to prevent rainbow attacks. Defaults to 32.

    Returns:
        bytes: password salt
        bytes: password hash
        bytes: encryption key
    """

    salt = salt or get_random_bytes(salt_length)
    keys = scrypt(password, salt, 32, N=2**16, r=8, p=1, num_keys=2)

    password_hash = keys[0]
    encryption_key = keys[1]

    return salt, password_hash, encryption_key


def encrypt_data(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    cipher = AES.new(key=key, mode=AES.MODE_EAX)
    return cipher.encrypt(data), cipher.nonce


def decrypt_data(data: bytes, key: bytes, nonce: bytes) -> bytes:
    cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(data)