import secrets
from dishka.integrations.fastapi import FromDishka
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.services import Service
from app.config import Config

ENCRYPTION_KEY_LENGTH = 32
IV_LENGTH = 12

class EncryptionService(Service):
    def __init__(self, config: FromDishka[Config]):
        super().__init__(config)

        if len(self.config.security.encryption_key) != ENCRYPTION_KEY_LENGTH:
            raise ValueError(f"Encryption key must be {ENCRYPTION_KEY_LENGTH} bytes")

        self.cipher = AESGCM(self.config.security.encryption_key)

    def _generate_iv(selft) -> bytes:
        return secrets.token_bytes(IV_LENGTH)

    def encrypt(self, data: bytes) -> bytes:
        iv = self._generate_iv()
        encrypted = self.cipher.encrypt(iv, data, associated_data=None)
        return iv + encrypted

    def decrypt(self, data: bytes) -> bytes:
        try:
            iv = data[:IV_LENGTH]
            encrypted = data[12:]
            return self.cipher.decrypt(iv, encrypted, associated_data=None)
        except Exception as e:
            raise ValueError("Invalid encrypted data") from e
