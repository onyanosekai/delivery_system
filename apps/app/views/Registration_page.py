import tkinter as tk
from tkinter import messagebox
from app.controllers import User_controller
from app.controllers import product_controller



class RegistrationPage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: User_controller のインスタンス
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている userController を保持
        self.product_controller = product_controller.ProductController()  # ProductController のインスタンスも保持
        
        # 画面の基本設定
        self.root.title("管理者アカウント新規登録画面")
        self.root.geometry("400x320")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="新規管理者登録", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # --- 入力項目の配置 ---
        
        # 1. 管理者ID
        self.label_id = tk.Label(root, text="希望する管理者ID:")
        self.label_id.pack(anchor="w", padx=50, pady=2)
        self.entry_id = tk.Entry(root, width=30)
        self.entry_id.pack(padx=50, pady=5)
        
        # 2. 名前
        self.label_name = tk.Label(root, text="管理者名（氏名）:")
        self.label_name.pack(anchor="w", padx=50, pady=2)
        self.entry_name = tk.Entry(root, width=30)
        self.entry_name.pack(padx=50, pady=5)
        
        # 3. パスワード
        self.label_pass = tk.Label(root, text="パスワード:")
        self.label_pass.pack(anchor="w", padx=50, pady=2)
        # 登録時もセキュリティのために目隠し（●）にします
        self.entry_pass = tk.Entry(root, width=30, show="*")
        self.entry_pass.pack(padx=50, pady=5)
        
        # 登録ボタン（クリックで inputUserInfo を実行）
        self.btn_register = tk.Button(
            root, 
            text="アカウントを作成する", 
            bg="orange", 
            fg="white", 
            font=("Arial", 11, "bold"),
            command=self._on_register_clicked
        )
        self.btn_register.pack(pady=20)

        #戻るボタン
        self.btn_back = tk.Button(
            root,
            text="戻る",
            bg="gray",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_back_clicked # 下で定義するメソッドを呼ぶ
        )
        self.btn_back.pack(pady=5)

    def inputUserInfo(self, admin_id: str, name: str, password: str) -> None:
        if hasattr(self.controller, 'validate_admin'):
            self.controller.validate_admin(admin_id, name, password)
        else:
            # まだコントローラー側に実装がない場合の仮ログ
            print(f"[Debug] userControllerへの新規登録要求: ID={admin_id}, Name={name}, Pass={password}")

    def _on_register_clicked(self):
        """
        「アカウントを作成する」ボタンが押された時の内部処理
        """
        # 各入力欄から文字列を取得
        admin_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        
        # 簡単な未入力チェック（バリデーション）
        if self.controller.register_User(admin_id, name, password):
            messagebox.showinfo("成功", "登録が完了しました。")
            self.controller.show_initial_page()
                        

    def _on_back_clicked(self):
        """「戻る」ボタンが押された時に初期画面に戻る"""
        # ログイン画面の時と完全に同じ処理です！
        if hasattr(self.controller, 'show_initial_page'):
            self.controller.show_initial_page()

    def display(self):
        """画面を表示するための補助メソッド"""
        self.root.mainloop()