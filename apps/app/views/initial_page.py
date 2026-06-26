import tkinter as tk
from tkinter import messagebox

class InitialPage:
    def __init__(self, root, controller=None):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: 必要に応じて全体のコントローラーを保持
        """
        self.root = root
        self.controller = controller
        
        # 画面の基本設定
        self.root.title("初期メニュー画面")
        self.root.geometry("400x350")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="配送管理システム メニュー", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=20)
        
        # --- メニューボタンの配置 ---
        
        # 1. 検索画面へのボタン
        self.btn_search = tk.Button(
            root, text="商品検索画面を開く", width=25, height=2,
            command=self.showSearchPage
        )
        self.btn_search.pack(pady=5)
        
        # 2. ログイン画面へのボタン
        self.btn_login = tk.Button(
            root, text="管理者ログイン画面を開く", width=25, height=2,
            command=self.showLoginPage
        )
        self.btn_login.pack(pady=5)
        
        # 3. ユーザー登録（管理者登録）画面へのボタン
        self.btn_register = tk.Button(
            root, text="管理者登録画面を開く", width=25, height=2,
            command=self.showUserRegistrationPage
        )
        self.btn_register.pack(pady=5)
        
        # 4. 情報登録画面へのボタン
        self.btn_info_reg = tk.Button(
            root, text="情報登録画面を開く", width=25, height=2,
            command=self.showInfoRegistrationPage
        )
        self.btn_info_reg.pack(pady=5)

    # --- クラス図に定義されているメソッド群（画面遷移） ---

    def showSearchPage(self) -> None:
        """クラス図：+ showSearchPage(): void"""
        messagebox.showinfo("画面遷移", "SearchPage（検索画面）へ遷移します。")
        # TODO: ここで別のウィンドウを開く、またはメインウィンドウのコンテンツを書き換える
        # 例: SearchPage(tk.Toplevel(self.root), self.controller)

    def showLoginPage(self) -> None:
        """クラス図：+ showLoginPage(): void"""
        messagebox.showinfo("画面遷移", "LoginPage（ログイン画面）へ遷移します。")
        # 例: LoginPage(tk.Toplevel(self.root), self.controller)

    def showUserRegistrationPage(self) -> None:
        """クラス図：+ showUserRegistrationPage(): void"""
        messagebox.showinfo("画面遷移", "RegistrationPage（管理者登録画面）へ遷移します。")
        # 例: RegistrationPage(tk.Toplevel(self.root), self.controller)

    def showInfoRegistrationPage(self) -> None:
        """クラス図：+ showInfoRegistrationPage(): void"""
        messagebox.showinfo("画面遷移", "InfoRegistrationPage（情報登録画面）へ遷移します。")
        # さっき作った InfoRegistrationPage を呼び出すイメージ

    def display(self):
        """画面を起動するメソッド"""
        self.root.mainloop()

# 単体テスト用のコード（このファイルを直接実行した時だけ動く）
if __name__ == "__main__":
    root = tk.Tk()
    app = InitialPage(root)
    app.display()