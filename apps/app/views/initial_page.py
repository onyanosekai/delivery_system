import tkinter as tk
from tkinter import messagebox

from app.views.seach_page import SerchPage
from app.views.login_page import LoginPage
from app.views.Registration_page import RegistrationPage
from app.views.info_registration_page import InfoRegistrationPage
# ★ 削除ページをインポートに追加
from app.views.delete_page import DeletePage 
from app.views.product_list_page import ProductListPage

from app.controllers.product_controller import ProductController
from app.controllers.User_controller import UserController

class InitialPage:
    # ★ 引数に `is_logged_in` を追加（デフォルトは False）
    def __init__(self, root, controller=None, is_logged_in=False):
        self.root = root
        self.controller = controller
        self.is_logged_in = is_logged_in
        
        # 画面の基本設定（ボタン増えるので縦幅を少し広げます）
        self.root.title("初期メニュー画面")
        self.root.geometry("400x420")

        # --- 画面切り替え用の土台（フレーム）を作成 ---
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        
        # タイトルラベル
        self.label_title = tk.Label(self.frame, text="配送管理システム メニュー", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=20)
        
        # --- メニューボタンの配置 ---
        
        self.btn_search = tk.Button(
            self.frame, text="商品検索画面を開く", width=25, height=2,
            command=self.showSearchPage
        )
        self.btn_search.pack(pady=5)
        
        # 🚨 【ここを修正】ログインしていない時（False）だけ「ログイン」「登録」ボタンを出す！
        if not self.is_logged_in:
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

        # --- 省略（情報登録ボタンの pack などの後） ---

        # ★★★ ログイン状態のときだけ「商品削除ボタン」と「ログアウトボタン」を表示する ★★★
        if self.is_logged_in:
            self.btn_delete = tk.Button(
                self.frame, text="商品削除画面を開く", width=25, height=2,
                bg="orange", fg="white", font=("Arial", 9, "bold"),
                command=self.showSearchPage  
            )
            self.btn_delete.pack(pady=5)

            # 👇 【ここを再追加！】ログアウトボタンを配置
            self.btn_logout = tk.Button(
                self.frame, text="ログアウト", width=25, height=2,
                bg="red", fg="white", font=("Arial", 9, "bold"),
                command=self._on_logout_clicked  # ログアウト時の処理を呼ぶ
            )
            self.btn_logout.pack(pady=5)

    def _on_delete_button_clicked(self):
        """初期メニューの削除ボタンが押された時の処理"""
        target_pid = self.entry_delete_id.get().strip()
        target_customer = self.entry_delete_customer.get().strip()
        
        if not target_pid or not target_customer:
            messagebox.showwarning("入力エラー", "商品番号と顧客名を入力してください。")
            return

        p_ctrl = self.controller.product_controller
        target_product = p_ctrl.search_items(target_pid, target_customer)

        if target_product is None:
            messagebox.showerror("エラー", "該当する商品が見つかりません。")
            return

        self.controller.show_delete_page(
            target_product.product_name, 
            target_product.product_id, 
            target_product.deadline,
            target_product  
        )

    # --- 画面遷移メソッド群 ---

    def showSearchPage(self) -> None:
        self.frame.destroy()
        # ★ ↓ここ！ ログイン状態をSerchPageに渡すように書き換える
        SerchPage(self.root, self.controller, is_logged_in=self.is_logged_in)

    def showLoginPage(self) -> None:
        self.frame.destroy()
        LoginPage(self.root, self.controller)

    def showUserRegistrationPage(self) -> None:
        self.frame.destroy()
        RegistrationPage(self.root, self.controller)

    def showInfoRegistrationPage(self) -> None:
        self.frame.destroy()
        InfoRegistrationPage(self.root, self.controller)

    # ★★★ 新設：削除画面へ遷移するメソッド ★★★
    def showDeletePage(self) -> None:
        """削除画面へ遷移"""
        self.frame.destroy()
        DeletePage(self.root, self.controller)

    def _on_logout_clicked(self):
        """ログアウトボタンが押された時の処理"""
        # 1. 現在のメニュー画面（フレーム）を一度まるごと破壊する
        self.frame.destroy()
        
        # 2. ログイン状態を False（未ログイン）に戻して、自分自身（InitialPage）を初期化し直す！
        # これにより、ログイン・登録ボタンが復活し、削除・ログアウトボタンが消えます
        from app.views.initial_page import InitialPage
        app = InitialPage(self.root, self.controller, is_logged_in=False)
        
        # 3. コントローラー側の参照も未ログイン版の画面に更新しておく
        if self.controller:
            self.controller.initial_page = app
            
        messagebox.showinfo("ログアウト", "ログアウトしました。")

    def display(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    # テスト用：True にすると削除ボタンが出現し、ログイン・登録ボタンが消えます
    app = InitialPage(root, is_logged_in=True) 
    app.display()