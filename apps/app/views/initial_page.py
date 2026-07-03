import tkinter as tk
from tkinter import messagebox

# クラス図とディレクトリ構成に基づいて各ビューをインポートします
# （※フォルダの画像にあった 'seach_page' というファイル名に仮で合わせています）
from app.views.seach_page import SerchPage
from app.views.login_page import LoginPage
from app.views.Registration_page import RegistrationPage
from app.views.info_registration_page import InfoRegistrationPage
from app.controllers.product_controller import ProductController
from app.controllers.User_controller import UserController

class InitialPage:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller
        
        # 画面の基本設定
        self.root.title("初期メニュー画面")
        self.root.geometry("400x350")

        # --- 画面切り替え用の土台（フレーム）を作成 ---
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        # タイトルラベル（rootではなく、self.frameに配置します）
        self.label_title = tk.Label(self.frame, text="配送管理システム メニュー", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=20)
        
        # --- メニューボタンの配置（すべてself.frameに配置） ---
        
        self.btn_search = tk.Button(
            self.frame, text="商品検索画面を開く", width=25, height=2,
            command=self.showSearchPage
        )
        self.btn_search.pack(pady=5)
        
        self.btn_login = tk.Button(
            self.frame, text="管理者ログイン画面を開く", width=25, height=2,
            command=self.showLoginPage
        )
        self.btn_login.pack(pady=5)
        
        self.btn_register = tk.Button(
            self.frame, text="管理者登録画面を開く", width=25, height=2,
            command=self.showUserRegistrationPage
        )
        self.btn_register.pack(pady=5)
        
        self.btn_info_reg = tk.Button(
            self.frame, text="情報登録画面を開く", width=25, height=2,
            command=self.showInfoRegistrationPage
        )
        self.btn_info_reg.pack(pady=5)

    # --- クラス図に定義されているメソッド群（画面遷移） ---

    def showSearchPage(self) -> None:
        """検索画面へ遷移"""
        self.frame.destroy() # 現在の画面（土台）を消す
        SerchPage(self.root, self.controller) # 次の画面を呼び出す

    def showLoginPage(self) -> None:
        """ログイン画面へ遷移"""
        self.frame.destroy()
        LoginPage(self.root, self.controller)

    def showUserRegistrationPage(self) -> None:
        """管理者登録画面へ遷移"""
        self.frame.destroy()
        RegistrationPage(self.root, self.controller)

    def showInfoRegistrationPage(self) -> None:
        """配達登録画面へ遷移"""
        self.frame.destroy()
        InfoRegistrationPage(self.root, self.controller)

    def display(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = InitialPage(root)
    app.display()