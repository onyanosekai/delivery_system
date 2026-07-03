import tkinter as tk
from tkinter import messagebox

class SerchPage:
    def __init__(self, root, controller):
        
        self.root = root
        self.controller = controller  # クラス図で繋がっている productController を保持
        
        # 画面の基本設定
        self.root.title("商品検索画面")
        self.root.geometry("450x350")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="商品検索", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # --- 入力項目の配置 ---
        
        # 1. 顧客名 (customerName)
        self.label_customer = tk.Label(root, text="顧客名:")
        self.label_customer.pack(anchor="w", padx=50, pady=2)
        self.entry_customer = tk.Entry(root, width=35)
        self.entry_customer.pack(padx=50, pady=5)
        
        # 2. 商品番号 (itemNumber)
        self.label_item_num = tk.Label(root, text="商品番号:")
        self.label_item_num.pack(anchor="w", padx=50, pady=2)
        self.entry_item_num = tk.Entry(root, width=35)
        self.entry_item_num.pack(padx=50, pady=5)
        
        # --- ボタン配置エリア ---
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=25)
        
        # 検索ボタン（inputProductInfo を実行）
        self.btn_search = tk.Button(
            self.btn_frame, 
            text="商品を検索", 
            bg="blue", 
            fg="white", 
            font=("Arial", 10, "bold"),
            width=15,
            command=self._on_search_clicked
        )
        self.btn_search.pack(side="left", padx=10)

    def _on_search_clicked(self):
        customer_name = self.entry_customer.get().strip()
        item_number = self.entry_item_num.get().strip()
        
        if not customer_name or not item_number:
            messagebox.showwarning("入力エラー", "顧客名と商品番号の両方を入力してください。")
            return
            
        self.inputProductInfo(customer_name, item_number)

    def inputProductInfo(self, customer_name: str, item_number: str) -> None:
        from app.controllers.product_controller import ProductController
        product = self.controller.search_items(item_number, customer_name)
        
        # 2. 結果による分岐
        if product is not None:
            # 見つかった場合：現在のフレームを破棄して次の画面へ
            self.frame.destroy()
            from app.views.receive_page import ReceivePage
            ReceivePage(self.root, self.controller, product)
            
        else:
            messagebox.showerror("検索エラー", "該当する商品が見つかりませんでした。")
