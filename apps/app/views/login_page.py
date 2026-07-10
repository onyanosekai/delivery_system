import tkinter as tk
from tkinter import messagebox

class LoginPage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: userController のインスタンス
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている userController を保持
        
        # 画面の基本設定
        self.root.title("管理者ログイン画面")
        self.root.geometry("400x320")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="管理者ログイン", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # --- 入力項目の配置 ---
        
        # 1. 管理者ID
        self.label_id = tk.Label(root, text="管理者ID:")
        self.label_id.pack(anchor="w", padx=50, pady=2)
        self.entry_id = tk.Entry(root, width=30)
        self.entry_id.pack(padx=50, pady=5)
        
        # 2. 名前
        self.label_name = tk.Label(root, text="名前:")
        self.label_name.pack(anchor="w", padx=50, pady=2)
        self.entry_name = tk.Entry(root, width=30)
        self.entry_name.pack(padx=50, pady=5)
        
        # 3. パスワード
        self.label_pass = tk.Label(root, text="パスワード:")
        self.label_pass.pack(anchor="w", padx=50, pady=2)
        # show="*" を指定することで、入力文字を目隠し（●）にします
        self.entry_pass = tk.Entry(root, width=30, show="*")
        self.entry_pass.pack(padx=50, pady=5)
        
        # ログインボタン（クリックで入力処理を実行）
        self.btn_login = tk.Button(
            root, 
            text="ログイン", 
            bg="green", 
            fg="white", 
            font=("Arial", 11, "bold"),
            command=self._on_login_clicked
        )
        self.btn_login.pack(pady=10)

        self.btn_back = tk.Button(
            root,
            text="戻る",
            bg="gray",          # ログインボタンと区別しやすい色に
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_back_clicked # クリック時に実行するメソッド
        )
        self.btn_back.pack(pady=5)

    def inputLoginInfo(self, admin_id: str, name: str, password: str) -> None:
        if hasattr(self.controller, 'requestLogin'):
            self.controller.login(admin_id, name, password)
        else:
            # まだコントローラー側に実装がない場合の仮ログ
            print(f"[Debug] userControllerへのログイン要求: ID={admin_id}, Name={name}, Pass={password}")
            
        # 本来はコントローラーの認証結果（True/False）を受けて画面を切り替えます
        messagebox.showinfo("送信完了", "ログイン要求を送信しました。")

    def _on_login_clicked(self):
        """
        「ログイン」ボタンが押された時の内部処理
        """
        admin_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        
        # 簡単な未入力チェック（バリデーション）
        if not admin_id or not name or not password:
            messagebox.showwarning("入力エラー", "すべての項目を入力してください。")
            return
        try:
            int_id = int(admin_id) # IDを数値に変換
        except ValueError:
            messagebox.showerror("エラー", "IDは数値で入力してください。")
            return

        # main.pyなどから共有されている user_controller を使って認証
        if self.controller and self.controller.login(int_id, name, password):
            messagebox.showinfo("成功", "ログインに成功しました！")
            
            # ★★★ ここで「ログイン成功時の遷移処理」を行います！ ★★★
            self.root.set_menu_state(True) # (※下の補足を参照。メニューをログイン状態にする)
            self.frame.destroy()  # ログイン画面の土台を消す
            
            # 循環インポートを防ぐために、ここで InitialPage をインポートして呼び出す
            from app.views.initial_page import InitialPage
            InitialPage(self.root, self.controller, is_logged_in=True)
            
        else:
            messagebox.showerror("失敗", "IDまたはパスワードが違います。")
        # クラス図の指定通り、inputLoginInfo メソッドに入力データを渡して実行
        self.inputLoginInfo(admin_id, name, password)

    # ★ 追加: 「戻る」ボタンが押された時の内部処理
    # ==========================================
   # 各画面の「戻る」処理の修正イメージ
    def _on_back_clicked(self):
        self.frame.destroy()
        from app.views.initial_page import InitialPage
        # ログイン状態を True にしてメニューに戻る
        InitialPage(self.root, self.controller, is_logged_in=True)

    def display(self):
        """画面を表示するための補助メソッド"""
        self.root.mainloop()