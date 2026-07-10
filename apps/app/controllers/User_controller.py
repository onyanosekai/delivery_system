from app.models.Administrator import Administrator
from app.views.login_page import LoginPage
import json
import os
from tkinter import messagebox
import tkinter as tk

class UserController:
    ADMIN_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Administrator.json")

    def __init__(self):
        # 登録された Administrator オブジェクトを格納するリスト
        self.admin_list = []
        self.load_admins()  # JSONファイルから管理者情報を読み込む

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
        """すべてのアカウントで、正しくJSONファイルから認証を行うメソッド"""
        import json
        import hashlib
        import os

        # 1. 画面から入力された生パスワードをハッシュ化
        current_input_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # 2. キャッシュを疑い、毎回直接JSONファイルを綺麗に読み込む
        if os.path.exists(self.ADMIN_JSON_PATH):
            with open(self.ADMIN_JSON_PATH, "r", encoding="utf-8") as f:
                try:
                    admin_data_list = json.load(f)
                    
                    # 3. JSON内の全ユーザーをループで回して、IDと名前が一致する人を探す
                    for user in admin_data_list:
                        # 入力されたID・名前と一致するか（型を文字列に揃えて安全に比較）
                        if str(user.get("admin_id")) == str(admin_id) and str(user.get("admin_name")) == str(admin_name):
                            json_hash = user.get("password")
                            
                            print(f"[Debug] ログイン試行ユーザーを発見: {admin_name}")
                            print(f"[Debug] 入力ハッシュ: {current_input_hash}")
                            print(f"[Debug] JSONハッシュ : {json_hash}")
                            
                            # ハッシュ値が一致すればログイン成功！
                            if json_hash == current_input_hash:
                                return True
                                
                except Exception as e:
                    print(f"[Debug] ログイン処理中のエラー: {e}")
                    
        # 見つからない、またはパスワード不一致なら失敗
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
        self.load_admins()  # 最新の管理者情報を読み込む
        for admin in self.admin_list:
            # エンティティの属性名「admin_id」に合わせて比較
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
        validation_result = self.validate_admin(admin_id, name, password)
        
        if validation_result is not None:
            # バリデーションエラーがあればメッセージを表示して終了
            messagebox.showerror("エラー", validation_result["message"])
            return
        
        # バリデーションOKならAdministratorオブジェクトを生成してリストに追加
        new_admin = Administrator(int(admin_id), name, password)
        self.admin_list.append(new_admin)
        
        # JSONファイルに保存
        self.register_admin()
        
        messagebox.showinfo("成功", "登録が完了しました。")
        
