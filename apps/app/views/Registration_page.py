import tkinter as tk
from tkinter import messagebox

class RegistrationPage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: userController のインスタンス
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている userController を保持
        
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
        """
        クラス図にある inputUserInfo メソッド
        入力された情報を userController のユーザー登録処理へ引き渡す
        """
        # クラス図の「registeruser」の矢印に相当する処理
        # userController に3つの情報を渡して新規登録を依頼する
        # ※実際の userController 側のメソッド名（registeruser 等）に合わせて呼び出します
        if hasattr(self.controller, 'registeruser'):
            self.controller.registeruser(admin_id, name, password)
        else:
            # まだコントローラー側に実装がない場合の仮ログ
            print(f"[Debug] userControllerへの新規登録要求: ID={admin_id}, Name={name}, Pass={password}")
            
        messagebox.showinfo("成功", "管理者アカウントの登録申請を送信しました。")
        self.root.destroy()  # 登録要求が終わったら画面を閉じる

    def _on_register_clicked(self):
        """
        「アカウントを作成する」ボタンが押された時の内部処理
        """
        # 各入力欄から文字列を取得
        admin_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()
        
        # 簡単な未入力チェック（バリデーション）
        if not admin_id or not name or not password:
            messagebox.showwarning("入力エラー", "すべての項目を入力してください。")
            return
            
        # クラス図の指定通り、inputUserInfo メソッドに入力データを渡して実行
        self.inputUserInfo(admin_id, name, password)

    def _on_back_clicked(self):
        """「戻る」ボタンが押された時に初期画面に戻る"""
        # ログイン画面の時と完全に同じ処理です！
        if hasattr(self.controller, 'show_initial_page'):
            self.controller.show_initial_page()

    def display(self):
        """画面を表示するための補助メソッド"""
        self.root.mainloop()