import tkinter as tk
import os
import datetime
from tkinter import messagebox
from app.controllers.product_controller import ProductController

'''
class Controller:
    def __init__(self, root):
        self.root = root
        self.product_controller = ProductController()
'''
        
class InfoRegistrationPage:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.product_controller = ProductController()

        
        # 画面の基本設定
        self.root.title("情報登録画面")
        self.root.geometry("450x600")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="情報登録", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # 入力説明のラベル
        self.label_hint = tk.Label(root, text="登録する情報を入力してください：", font=("Arial", 10))
        self.label_hint.pack(anchor="w", padx=30, pady=5)
        
        # --- 入力項目の配置 ---
        
        # 1. 商品名 (productName)
        self.label_product = tk.Label(root, text="商品名:")
        self.label_product.pack(anchor="w", padx=50, pady=2)
        self.entry_product = tk.Entry(root, width=35)
        self.entry_product.pack(padx=50, pady=5)
        
        # 2. 商品番号 (itemNumber)
        self.label_item_num = tk.Label(root, text="商品番号:")
        self.label_item_num.pack(anchor="w", padx=50, pady=2)
        self.entry_item_num = tk.Entry(root, width=35)
        self.entry_item_num.pack(padx=50, pady=5)

        # 3. 顧客名 (customerName)
        self.label_customer = tk.Label(root, text="顧客名:")
        self.label_customer.pack(anchor="w", padx=50, pady=2)
        self.entry_customer = tk.Entry(root, width=35)
        self.entry_customer.pack(padx=50, pady=5)

        # 4. 配達日 (deliveryDate)
        self.label_delivery = tk.Label(root, text="配達日 (YYYY-MM-DD):")
        self.label_delivery.pack(anchor="w", padx=50, pady=2)
        self.entry_delivery = tk.Entry(root, width=35)
        self.entry_delivery.pack(padx=50, pady=5)

        # 5. 受け取り期限 (deadline)
        self.label_deadline = tk.Label(root, text="受け取り期限 (YYYY-MM-DD):")
        self.label_deadline.pack(anchor="w", padx=50, pady=2)
        self.entry_deadline = tk.Entry(root, width=35)
        self.entry_deadline.pack(padx=50, pady=5)

        # 6. 配達員ID (driverId)
        self.label_driver = tk.Label(root, text="配達員ID:")
        self.label_driver.pack(anchor="w", padx=50, pady=2)
        self.entry_driver = tk.Entry(root, width=35)
        self.entry_driver.pack(padx=50, pady=5)
        
        # 登録ボタン（クリックで submit メソッドを呼び出す）
        self.btn_submit = tk.Button(
            root, 
            text="登録する", 
            bg="blue", 
            fg="white", 
            font=("Arial", 11, "bold"),
            command=self._on_submit_clicked
        )
        self.btn_submit.pack(pady=20)

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

    def _on_submit_clicked(self):
        product_name = self.entry_product.get().strip()
        product_id = self.entry_item_num.get().strip()
        customer = self.entry_customer.get().strip()
        delivery = self.entry_delivery.get().strip()
        deadline = self.entry_deadline.get().strip()
        driver = self.entry_driver.get().strip()
        
        # 画面側でサッとチェックしてからコントローラーへ投げる
        if not (product_name and product_id and customer and delivery and deadline and driver):
            messagebox.showwarning("入力エラー", "全ての項目を入力してください。")
            return
         # 文字列の日付を datetime 型に変換（Controllerへ渡す前に変換しておくのが安全です）
        try:
            deliv_date = datetime.datetime.strptime(delivery, "%Y-%m-%d").date()
            dead_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("エラー", "日付は YYYY-MM-DD 形式で入力してください。")
            return

            
        # submitメソッドへ渡す
        self.submit(product_id, product_name, customer, deliv_date, dead_date, driver)

    def submit(self, p_id, p_name, c_name, deliv_date, dead_date, d_id):
        # コントローラーの validate_product を呼び出し
        if self.product_controller.register_product(p_id, p_name, c_name, deliv_date, dead_date, d_id):
            messagebox.showinfo("成功", "登録が完了しました。")
            self.controller.show_initial_page()

        else:
            messagebox.showerror("エラー", "登録内容に不備があります。コンソールを確認してください。")

    def _on_back_clicked(self):
        """「戻る」ボタンが押された時に初期画面に戻る"""
        # ログイン画面の時と完全に同じ処理です！
        if hasattr(self.controller, 'show_initial_page'):
            self.controller.show_initial_page()

    def display(self):
        """
        画面を表示するための補助メソッド
        """
        self.root.mainloop()