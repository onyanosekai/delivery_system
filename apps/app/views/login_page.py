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

<<<<<<< HEAD
def _on_login_clicked(self):
        """「ログイン」ボタンが押された時の内部処理"""
=======
    def _on_login_clicked(self):
        """
        「ログイン」ボタンが押された時の内部処理
        """
>>>>>>> a87deaa25c1c048134fd2853f999abfe21b51f94
        admin_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        password = self.entry_pass.get().strip()

        # 簡単な入力チェック
        if not admin_id or not name or not password:
            messagebox.showwarning("入力エラー", "すべての項目を入力してください。")
            return

        # --- ここから修正：コントローラーの認証結果で画面を切り替える ---
        try:
            int_id = int(admin_id)  # IDを数値に変換
        except ValueError:
            messagebox.showerror("エラー", "IDは数値で入力してください。")
            return

<<<<<<< HEAD
        # 1. main.pyで用意したUserControllerを使ってログイン認証を行う
        user_ctrl = self.controller  # main.pyの main() 内で controller = UserController() としているため

        if user_ctrl.login(int_id, password):
=======
        # main.pyなどから共有されている user_controller を使って認証
        if self.controller and self.controller.login(int_id, name, password):
>>>>>>> a87deaa25c1c048134fd2853f999abfe21b51f94
            messagebox.showinfo("成功", "ログインに成功しました！")

            # 2. 現在のログイン画面（土台のフレーム）を消し去る
            # ※もしログイン画面で self.frame を使っていなければ、画面全体を消すために
            # カスタムした破棄処理にするか、パーツを消してください。ここでは self.frame.destroy() とします。
            if hasattr(self, "frame"):
                self.frame.destroy()
            else:
                # もし Frame を使わず root に直配置していた場合の安全策
                for widget in self.root.winfo_children():
                    widget.destroy()

            # 3. 循環インポートを防ぐために、この関数内で InitialPage をインポート
            from app.views.initial_page import InitialPage

            # 4. ログイン状態フラグを `is_logged_in=True` にして初期画面を開く！
            # これにより、削除ボタンが出現した状態のメニューになります
            app = InitialPage(self.root, self.controller, is_logged_in=True)

            # 5. main.py側の参照も最新の初期画面に上書きしておく
            self.controller.initial_page = app

        else:
            messagebox.showerror(
                "失敗", "IDまたはパスワードが違います。"
            )