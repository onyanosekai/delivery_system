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
        self.btn_login.pack(pady=20)

    def inputLoginInfo(self, admin_id: str, name: str, password: str) -> None:
        """
        クラス図にある inputLoginInfo メソッド
        入力された情報を userController のログイン要求処理へ引き渡す
        """
        # クラス図の「requestLogin」の矢印に相当する処理
        # userController に入力された3つの情報を渡して認証を依頼する
        # ※実際の userController 側のメソッド名に合わせて呼び出します
        if hasattr(self.controller, 'requestLogin'):
            # 例: コントローラー側で検証をおこなう
            self.controller.requestLogin(admin_id, name, password)
        else:
            # まだコントローラー側に実装がない場合の仮ログ
            print(f"[Debug] userControllerへのログイン要求: ID={admin_id}, Name={name}, Pass={password}")
            
        # 本来はコントローラーの認証結果（True/False）を受けて画面を切り替えます
        messagebox.showinfo("送信完了", "ログイン要求を送信しました。")

    def _on_login_clicked(self):
        """
        「ログイン」ボタンが押された時の内部処理
        """
        # 各入力欄から文字列を取得
        admin_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        
        # 簡単な未入力チェック（バリデーション）
        if not admin_id or not name or not password:
            messagebox.showwarning("入力エラー", "すべての項目を入力してください。")
            return
            
        # クラス図の指定通り、inputLoginInfo メソッドに入力データを渡して実行
        self.inputLoginInfo(admin_id, name, password)

    def display(self):
        """画面を表示するための補助メソッド"""
        self.root.mainloop()