import tkinter as tk
from tkinter import messagebox

from app.views.seach_page import SerchPage
from app.views.login_page import LoginPage
from app.views.Registration_page import RegistrationPage
from app.views.info_registration_page import InfoRegistrationPage
# ★ 削除ページをインポートに追加
from app.views.delete_page import DeletePage 

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

        # ★★★ ログイン状態のときだけ「商品削除ボタン」を表示する ★★★
        if self.is_logged_in:
            self.btn_delete = tk.Button(
                self.frame, text="商品削除画面を開く", width=25, height=2,
                bg="orange", fg="white", font=("Arial", 9, "bold"),
                command=self.showDeletePage  # 下で定義するメソッドを呼ぶ
            )
            self.btn_delete.pack(pady=5)

    def _on_delete_button_clicked(self):
        """初期メニューの削除ボタンが押された時の処理"""
        
        # 1. 画面上の入力欄から、削除したい「商品番号」と「顧客名」を取得する
        # ※ もし検索用の入力欄をまだ作っていない場合は、事前に配置してください
        target_pid = self.entry_delete_id.get().strip()
        target_customer = self.entry_delete_customer.get().strip()
        
        if not target_pid or not target_customer:
            messagebox.showwarning("入力エラー", "商品番号と顧客名を入力してください。")
            return

        # 2. product_controller に実装されている `search_items` をそのまま利用！
        # これにより、自動的に Product.json から読み込まれたデータ内を検索します。
        p_ctrl = self.controller.product_controller
        target_product = p_ctrl.search_items(target_pid, target_customer)

        # 3. JSONからデータが見つからなかった場合
        if target_product is None:
            messagebox.showerror("エラー", "該当する商品が見つかりません。")
            return

        # 4. 見つかった本物の商品データ（オブジェクト）をそのまま丸ごと削除画面に引き渡す！
        # main.py の画面切り替えメソッドを呼び出す
        self.controller.show_delete_page(
            target_product.product_name, 
            target_product.product_id, 
            target_product.deadline,
            target_product  # ★ 実際のオブジェクトも一緒に渡しておくと後で削除が楽になります
        )

    # --- 画面遷移メソッド群 ---

    def showSearchPage(self) -> None:
        self.frame.destroy()
        SerchPage(self.root, self.controller)

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

    def display(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    # テスト用：True にすると削除ボタンが出現します
    app = InitialPage(root, is_logged_in=True) 
    app.display()