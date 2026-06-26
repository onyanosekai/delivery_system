class UserContoroller:
    def ligin(self,admin_id: int,password: str):
        admin = self.find_admin(admin_id)
        if admin is None:
            return False
        return
    
    admin.check_password(password)