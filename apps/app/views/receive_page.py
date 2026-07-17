import tkinter as tk
from tkinter import messagebox
from app.controllers.product_controller import ProductController
from app.models.Product import Product

class ReceivePage:
    def __init__(self, root, controller,product_controller, product):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        :param product: 受領する商品の情報
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている productController を保持
        self.product_controller = product_controller  # ProductController のインスタンスも保持
        self.product = product  # 受領する商品の情報

        # 画面の基本設定
        self.root.title("商品の受領確認画面")
        self.root.geometry("400x600")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="以下の商品を受領（確認）します", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # 商品情報を表示するためのラベル群（初期値は空文字）
        self.label_item_name = tk.Label(root, 
                                        text=f"商品名: {self.product.product_name}", 
                                        font=("Arial", 12)
                                        )
        self.label_item_name.pack(pady=5)
        
        self.label_item_number = tk.Label(root,
                                           text=f"商品番号: {self.product.product_id}", 
                                           font=("Arial", 12)
                                           )
        self.label_item_number.pack(pady=5)
        
        # 受領確定ボタン（クリックでコントローラーへ通知）
        self.btn_confirm = tk.Button(
            root, 
            text="受領を確定する", 
            bg="green", 
            fg="white", 
            font=("Arial", 11, "bold"),
            command=self._on_confirm_clicked
        )
        self.btn_confirm.pack(pady=20)

        # 👇 【ここを追加】戻るボタン
        self.btn_back = tk.Button(
            root,
            text="戻る",
            bg="gray",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_back_clicked
        )
        self.btn_back.pack(pady=5)

    def receive_product(self, product):
        print("変更前:", product.status)

        product.status = "受取り済み"

        print("変更後:", product.status)

        self.save_products_to_json()
        
    def _on_confirm_clicked(self):
        """
        「受領を確定する」ボタンが押された時の内部処理
        """
        # ユーザーへの最終確認ポップアップ
        answer = messagebox.askyesno("確認", "この商品を受領したことで確定しますか？")
        
        if answer:
                self.product_controller.receive_product(self.product)
                
                messagebox.showinfo("完了", "受領確認を記録しました。")
                self.controller.show_initial_page()

    def _on_back_clicked(self):
        # 1. まず画面上の部品を【完全に】すべて消し去る
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 2. 確定しているファイル名（seach_page）から直接インポート！
        from app.views.seach_page import SerchPage

        # 3. 検索画面を生成（受領画面にいる＝未ログイン状態なので False を渡す）
        SerchPage(self.root, self.controller, is_logged_in=False)