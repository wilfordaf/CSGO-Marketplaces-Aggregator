from dataclasses import dataclass
from hashlib import sha256


@dataclass
class Item:
    price: float
    exterior: str
    float_value: float
    pattern_seed: int
    weapon: str
    skin: str

    def get_sha256_value(self) -> str:
        hasher = sha256()
        hasher.update(str(self.price).encode())
        hasher.update(self.exterior.encode())
        hasher.update(str(self.float_value).encode())
        hasher.update(str(self.pattern_seed).encode())
        hasher.update(self.weapon.encode())
        hasher.update(self.skin.encode())
        return hasher.hexdigest()
