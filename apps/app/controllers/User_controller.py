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
        # 管理者ID（数値）でエンティティを検索
        admin = self.find_admin(admin_id)
        
        # 見つからなければFalse
        if admin is None:
            return False
            
        # 作成してもらった check_password(password) メソッドをここで呼び出す
        # 入力された平文パスワードをハッシュ化して比較
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
        """
        ユースケース：ユーザー情報を登録する
        仕様書のバリデーションを行い、クリアしたら Administrator インスタンスを生成して保存する
        """
        # パスワード英数字混合8文字以上チェック
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
        

    def registeruser(self, admin_id: str, name: str, password: str) -> dict:
        # 管理者をユーザー一覧に登録する
        # 作成してもらった Administrator の __init__ にデータを渡してインスタンス化
        # これによって、内部で自動的にパスワードがハッシュ化されて保存されます
        new_admin = Administrator(
            admin_id=admin_id,
            admin_name=name,
            password=password
        )
        
        # コントローラーの管理リストに追加
        self.admin_list.append(new_admin)
        file_path = self.ADMIN_JSON_PATH
        # 既存データ読込
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    admins = json.load(f)
                except json.JSONDecodeError:
                    admins = []
        else:
            admins = []
        
        # 新しい管理者を追加
        admins.append({
            "admin_id": new_admin.admin_id,
            "admin_name": new_admin.admin_name,
            "password": new_admin.password
        })
        
        # JSONへ書込
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(admins, f, ensure_ascii=False, indent=4)

        return {
            "status": "success", 
            "message": f"管理者「{name}」さんの登録が完了しました！"
        }