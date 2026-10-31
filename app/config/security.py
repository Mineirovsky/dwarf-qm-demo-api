import os

class SecurityConfig:
    def __init__(self):
        self.encryption_key = bytes.fromhex(os.getenv("ENCRYPTION_KEY", "358c16cf3390187934842a621276c4a5a94f1571f133293063b3d5ecb654280f"))
        self.hmac_key = bytes.fromhex(os.getenv("HMAC_KEY", "622c1cc2b2ff3ca34bf1aa65edbb4b55a8de859d3dd6f57d128eb0d429f65216"))
