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
        # 1. 一旦、__init__を呼び出す（パスワードはハッシュ化されてしまうが後で上書きする）
        admin = cls(
            admin_id=data["admin_id"],
            admin_name=data["admin_name"],
            password=""  # 空文字などを渡しておく
        )
        
        # 2. ★修正：全変数デバッグログで確認した、正しい変数名 'password_hash' に直接上書きする
        # data["password"] に入っているJSONの一重ハッシュ値をそのまま代入します
        admin.password_hash = data["password"]
        
        return admin

    def to_dict(self) -> dict:
            return {
                "admin_id": self.admin_id,
                "admin_name": self.admin_name,
                "password": self.password_hash
            }