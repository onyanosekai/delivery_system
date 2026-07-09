import hashlib
class Administrator:
    def __init__(self, admin_id, admin_name, password):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == self._hash_password(password)
    
    def __str__(self):
        return f"Admin({self.admin_id}, {self.admin_name})"
    
@classmethod
def from_dict(cls, data: dict):
        return cls(
            admin_id=data["admin_id"],
            admin_name=data["admin_name"],
            password=data["password"]
        )

def to_dict(self) -> dict:
        return {
            "admin_id": self.admin_id,
            "admin_name": self.admin_name,
            "password": self.password_hash
        }