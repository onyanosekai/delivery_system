from app.models.Administrator import Administrator
from app.views.login_page import LoginPage
import json
import os
from tkinter import messagebox
import tkinter as tk

class UserController:
    ADMIN_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Administrator.json")

    def __init__(self):
        self.admin_list = []
        self.load_admins()  

    def load_admins(self):
        if os.path.exists(self.ADMIN_JSON_PATH):
            with open(self.ADMIN_JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.admin_list = [
                Administrator(
                    item["admin_id"],
                    item["admin_name"],
                    item["password"]
                )
                for item in data
            ]

    # 1. ログイン処理 
    def login(self, admin_id: int, admin_name: str, password: str) -> bool:
        """すべてのアカウントをJSONファイルから正しくループで探して認証する"""
        import json
        import hashlib
        import os

        current_input_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if os.path.exists(self.ADMIN_JSON_PATH):
            with open(self.ADMIN_JSON_PATH, "r", encoding="utf-8") as f:
                try:
                    admin_data_list = json.load(f)
                    
                    
                    for user in admin_data_list:
                        if str(user.get("admin_id")) == str(admin_id) and str(user.get("admin_name")) == str(admin_name):
                            json_hash = user.get("password")
                            
                            if json_hash == current_input_hash:
                                return True
                except Exception as e:
                    print(f"[Debug] ログイン読み込みエラー: {e}")
        return False
        
    def showAdminLoginPage(self):
        self.initial_page.clear_frame()
        self.login_view = LoginPage(self.root, self)

    def show_initial_page(self):
        from app.views.initial_page import InitialPage
        
        for widget in self.root.winfo_children():
            widget.destroy()
        self.initial_page = InitialPage(self.root, self)

    def find_admin(self, admin_id: int) -> Administrator:
        """
        管理者リストから指定されたIDのオブジェクトを探す
        """
        self.load_admins()  
        for admin in self.admin_list:
            
            if admin.admin_id == admin_id:
                return admin
        return None

    # 2. ユーザー登録処理 (仕様書準拠 ＋ エンティティ生成)
    def validate_admin(self, admin_id: str, name: str, password: str) -> dict:
        self.load_admins()  # 最新の管理者情報を読み込む
        is_length_ok = len(password) >= 8
        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)
        
        if not (is_length_ok and has_letter and has_digit):
            return {
                "status": "error_password", 
                "message": "パスワードは【英数字混合の8文字以上】で設定してください。"
            }

        #  すでに同じIDの管理者が登録されていないかチェック
        try:
            int_id = int(admin_id)
            if self.find_admin(int_id) is not None:
                return {
                    "status": "error_duplicate",
                    "message": f"管理者ID「{admin_id}」はすでに使用されています。"
                }
        except ValueError:
            return {
                "status": "error_id",
                "message": "管理者IDは数値で入力してください。"
            }
        
    def register_admin(self):
            data = {Administrator.from_dict(admin.to_dict()) for admin in self.admin_list}
            with open(self.ADMIN_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump([admin.to_dict() for admin in self.admin_list], f, ensure_ascii=False, indent=4)
            self.show_initial_page()

    def register_User(self, admin_id: str, name: str, password: str) -> None:
        import json
        import hashlib
        import os

        validation_result = self.validate_admin(admin_id, name, password)
        if validation_result is not None:
            messagebox.showerror("エラー", validation_result["message"])
            return
        
        
        new_password_hash = hashlib.sha256(password.encode()).hexdigest()
        new_admin_data = {
            "admin_id": int(admin_id),
            "admin_name": name,
            "password": new_password_hash
        }

        
        admin_data_list = []
        if os.path.exists(self.ADMIN_JSON_PATH):
            with open(self.ADMIN_JSON_PATH, "r", encoding="utf-8") as f:
                try:
                    admin_data_list = json.load(f)
                except json.JSONDecodeError:
                    admin_data_list = []

        
        admin_data_list.append(new_admin_data)

       
        with open(self.ADMIN_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(admin_data_list, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("成功", "登録が完了しました。")
        self.show_initial_page()