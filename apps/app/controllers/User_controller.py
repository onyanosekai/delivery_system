from app.models.Administrator import Administrator
from app.views.login_page import LoginPage
import json
import os

class UserController:
    ADMIN_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Administrator.json")

    def __init__(self):
        # 登録された Administrator オブジェクトを格納するリスト
        self.admin_list = []

    # 1. ログイン処理 
    def login(self, admin_id: int, password: str) -> bool:
        """
        管理者のログイン認証を行うメソッド
        """
        admin = self.find_admin(admin_id)
        
        # 見つからなければFalse
        if admin is None:
            return False
            
        return admin.check_password(password)
        
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
        for admin in self.admin_list:
            # エンティティの属性名「admin_id」に合わせて比較
            if admin.admin_id == admin_id:
                return admin
        return None

    # 2. ユーザー登録処理 (仕様書準拠 ＋ エンティティ生成)
    def validate_admin(self, admin_id: str, name: str, password: str) -> dict:
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
