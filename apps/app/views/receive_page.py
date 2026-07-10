import tkinter as tk
from tkinter import messagebox
from app.controllers.product_controller import ProductController
from app.models.Product import Product

class ReceivePage:
    def __init__(self, root, controller, product):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        :param product: 受領する商品の情報
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている productController を保持
        self.product_controller = ProductController()  # ProductController のインスタンスも保持
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