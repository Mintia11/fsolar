import base64

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_der_private_key,
    load_der_public_key,
)

KEY_PRIVATE_B64 = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCcAkTrymNZma1KDpkmz0Vm6AlcLpsFKW5NbqYm204s5qWOt0StWczkM035gXOkH2kDKxMSuNjVudJW4TBBLCm2epSOLsKHaoyPaf7R4Knynq+1KHv+0Wva6XycNG2SizAsA0AjC1ST8bzmKkymZjVbrjYsiacQmYaSR12VuNuPElNlZHmFz931w9Zv4BHvsvEUWsyKTdz7ji/WRCUg8U/oSMhs6+38u/t8dYP0kj9jM3jLWArsL9VB00a6KRDI2D7lbeuD15xh/0jm4sBDBj+HF4jeVs2wSt5uop7YRsnwDBw0gLSUMHPndKrQwvz1BqkS7Ld8H66m5y3EtQtUMJs3AgMBAAECggEBAJpdLHDaav9nLa3PT/60rAksosZRXxX2bquzRjfAW1PWTA4wjIWyCyfpE8hDLHdClReLcW3e9L5VBSjt3F9AIW3rUD53SgfPh5EH4hks4TuthFIN4tK5yKxsxt2QirKrgliqRrXmKiPQ14YuaHVlQHqcoAHlmia0ohDvCExzAtxGSr0ZzJIWD7IMRHDg27yJgqpeYVwP3PWQ4jSfVj982F2tYT9jZI80z0CveI7FXDqyGH4u+XAIG8lxW5a16BI8LjuZTQgrLusNRYBSLVgWtOrgtxsF+iCGZSkCk8vMWkWtkESBhAJO72+1nEIzkXinX9yvcgQ5uOx1gztPNDxABRECgYEA2hB0vfpwuzJ+SkgSO5bTCk4678olCQ7PPEzwKstwjwLQzEd6RDuHoJgvqWOC8ZNl0s9Pc706A6vK8mu+CjLqzuOiWKYY5rJhTmnF/Uu2DeIIxDZoJfO5L4OcRthqqxYf9+r1x58SR8W1wydqTPmYZd+i1cl98J4I/BnkLyVN/KMCgYEAtyYpHoxVF+nrwabY9bYDsgwhgXOjWyfOSx3g0xbm7nG2PQODkhLG2UduZJbU8YL4O5Lx4FcijllBXwU6QlznfYJosblyqaDiE3rhEGW/zXVwyuD3S+B58T5jS7pox+eLBI/285s26RBU7AlTjnrpA4mjUApee5mf7CKVO+1+HF0CgYBUOnr9TpjwlaZWRtRUFAPcPS9io6/+eavuXMF/pikJ9Ep2PT2q0Vun2mC+iuNvMEHqVY0Y5YRdGqQ/UwKKqfQsiZyRpUaFBW20fgKtverKHf7I20MLNcLX6XwZmUpKXzdl6WmZ+4VyF5oHkVfr95S39NPOxA9TO5e42L9cvooLBQKBgCwzAWll5INI6KRrZ6CktG+bjdp31cyB5r8qDr/inwicWKaQ2oe+EE8PdgzAedNvEAkQhV7mqGhCEgykblLlqNgZSLrbTlixgt3AoeAbLhafaQENGaEuIz+dFsmHyxGzR1FqjOZtZusIDfaIqamQ7/rylH8UgYjCol2SWwGDZxPhAoGBANkoInsxH2LXLA2hJTl3bgZZ7ndcWMt2dE/5SCqFHvt2/+iV1lGd13zxrQ3hhQgUY38etmLzdgDHqI0bLBJNvDMcXmeU+52rBDGKhtcIhH7nDOoTAbEj2oCtcrIkIquI+FWp3trnnqWUn7zcda/vTNM5qz8XI3cc4Xj94TOpd6Px"
KEY_PUBLIC_B64 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnAJE68pjWZmtSg6ZJs9FZugJXC6bBSluTW6mJttOLOaljrdErVnM5DNN+YFzpB9pAysTErjY1bnSVuEwQSwptnqUji7Ch2qMj2n+0eCp8p6vtSh7/tFr2ul8nDRtkoswLANAIwtUk/G85ipMpmY1W642LImnEJmGkkddlbjbjxJTZWR5hc/d9cPWb+AR77LxFFrMik3c+44v1kQlIPFP6EjIbOvt/Lv7fHWD9JI/YzN4y1gK7C/VQdNGuikQyNg+5W3rg9ecYf9I5uLAQwY/hxeI3lbNsErebqKe2EbJ8AwcNIC0lDBz53Sq0ML89QapEuy3fB+upuctxLULVDCbNwIDAQAB"

ENCRYPT_BLOCK_SIZE = 117
DECRYPT_BLOCK_SIZE = 128


def _load_private_key():
    der = base64.b64decode(KEY_PRIVATE_B64)
    return load_der_private_key(der, password=None)


def _load_public_key():
    der = base64.b64decode(KEY_PUBLIC_B64)
    return load_der_public_key(der)


def encrypt(plaintext: str) -> str | None:
    """Encrypts plaintext with the public key, chunking into 117-byte
    blocks (matching the original Java), returns Base64 ciphertext."""
    try:
        public_key = _load_public_key()
        data = plaintext.encode("utf-8")
        out = bytearray()

        for i in range(0, len(data), ENCRYPT_BLOCK_SIZE):
            chunk = data[i : i + ENCRYPT_BLOCK_SIZE]
            encrypted_chunk = public_key.encrypt(chunk, padding.PKCS1v15())
            out.extend(encrypted_chunk)

        return base64.b64encode(bytes(out)).decode("ascii")
    except Exception as e:
        print(e)
        return None


def decrypt(ciphertext_b64: str) -> str | None:
    """Decrypts Base64 ciphertext with the private key, chunking into
    128-byte blocks (matching the original Java), returns plaintext."""
    try:
        private_key = _load_private_key()
        ciphertext = base64.b64decode(ciphertext_b64)
        out = bytearray()

        for i in range(0, len(ciphertext), DECRYPT_BLOCK_SIZE):
            chunk = ciphertext[i : i + DECRYPT_BLOCK_SIZE]
            decrypted_chunk = private_key.decrypt(chunk, padding.PKCS1v15())
            out.extend(decrypted_chunk)

        return bytes(out).decode("utf-8")
    except Exception as e:
        print(e)
        return None
