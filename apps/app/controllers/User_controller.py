# 作成してもらった models/administrator.py から Administrator クラスをインポート
from models.administrator import Administrator

class UserContoroller:
    def __init__(self):
        # 登録された Administrator オブジェクトを格納するリスト
        self.admin_list = []

    # ==========================================
    # 1. ログイン処理 (エンティティ連動版)
    # ==========================================
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

    def find_admin(self, admin_id: int) -> Administrator:
        """
        管理者リストから指定されたIDのオブジェクトを探す
        """
        for admin in self.admin_list:
            # エンティティの属性名「admin_id」に合わせて比較
            if admin.admin_id == admin_id:
                return admin
        return None

    # ==========================================
    # 2. ユーザー登録処理 (仕様書準拠 ＋ エンティティ生成)
    # ==========================================
    def register_user(self, admin_id: str, name: str, password: str) -> dict:
        """
        ユースケース：ユーザー情報を登録する
        仕様書のバリデーションを行い、クリアしたら Administrator インスタンスを生成して保存する
        """
        
        # 【基本フロー 6 / 代替フロー 6b】 空欄チェック
        if not str(admin_id).strip() or not name.strip() or not password.strip():
            return {
                "status": "error_empty", 
                "message": "未入力の項目があります。すべての項目を正しく入力してください。"
            }

        # 【基本フロー 5 / 代替フロー 5a】 パスワード英数字混合8文字以上チェック
        is_length_ok = len(password) >= 8
        has_letter = any(char.isalpha() for char in password)
        has_digit = any(char.isdigit() for char in password)
        
        if not (is_length_ok and has_letter and has_digit):
            return {
                "status": "error_password", 
                "message": "パスワードは【英数字混合の8文字以上】で設定してください。"
            }

        # 【追加の安全策】 すでに同じIDの管理者が登録されていないかチェック
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

        # 【基本フロー 7】 管理者をユーザー一覧に登録する
        # 作成してもらった Administrator の __init__ にデータを渡してインスタンス化
        # これによって、内部で自動的にパスワードがハッシュ化されて保存されます
        new_admin = Administrator(
            admin_id=int_id,
            admin_name=name,
            password=password
        )
        
        # コントローラーの管理リストに追加
        self.admin_list.append(new_admin)

        return {
            "status": "success", 
            "message": f"管理者「{name}」さんの登録が完了しました！"
        }