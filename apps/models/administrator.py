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