from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES

from Crypto.Random import get_random_bytes


# NOTE do I want to keep the hash length static(32)?
# TODO possibly extract these values into static variables.
def hash_password(password: bytes, salt_override: bytes | None, num_hashes: int | None = 1) -> bytes | list[bytes]:
    """Hashes the password along with the salt provided or generated when none is given.

    Args:
        password (bytes): Target password to hash.
        salt_override (bytes | None): Target salt for the hash.
        num_hashes (int | None, optional): How many hashes are generated. Defaults to 1.

    Returns:
        bytes | list[bytes]: _description_
    """
    return scrypt(password, salt_override or get_random_bytes(32), 32, N=2**14, r=8, p=1, num_keys=num_hashes)



def encrypt_data(password: bytes, data: bytes) -> tuple[bytes, bytes]:
    """Encrypts data using AES.

    Args:
        password (bytes): Target password to encrypt data with.
        data (bytes): Target data to encrypt.

    Returns:
        tuple[bytes, bytes]: Encrypted data, AES nonce.
    """
    cipher = AES.new(password, mode=AES.MODE_EAX)

    return cipher.encrypt(data), cipher.nonce
