import tkinter as tk
from tkinter import messagebox
from app.controllers.product_controller import ProductController
from app.views.receive_page import ReceivePage
# ★ 削除画面のインポートを追加
from app.views.delete_page import DeletePage 

class SerchPage:
    # ★ 引数に is_logged_in=False を追加
    def __init__(self, root, controller, is_logged_in):
        
        self.root = root
        self.controller = controller  # クラス図で繋がっている productController を保持
        self.product_controller = ProductController()  # ProductController のインスタンスを作成
        self.is_logged_in = is_logged_in  # ★ ログイン状態を保持

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

        # 戻るボタン
        self.btn_back = tk.Button(
            self.root,
            text="戻る",
            bg="gray",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_back_clicked 
        )
        self.btn_back.pack(pady=5)

    def _on_search_clicked(self):
        customer_name = self.entry_customer.get().strip()
        item_number = self.entry_item_num.get().strip()
        
        if not customer_name or not item_number:
            messagebox.showwarning("入力エラー", "顧客名と商品番号の両方を入力してください。")
            return
            
        self.inputProductInfo(customer_name, item_number)
        
    def _on_back_clicked(self):
        """「戻る」ボタンが押された時に初期画面に戻る"""
        if hasattr(self.controller, 'show_initial_page'):
            self.controller.show_initial_page()
    
    def inputProductInfo(self, customer_name: str, item_number: str) -> None:
        product = self.product_controller.search_items(item_number, customer_name)
        
        if not product:
            messagebox.showerror("検索エラー", "該当する商品が見つかりませんでした。")
        else:
            for widget in self.root.winfo_children():
                widget.destroy()  # 現在のウィジェットをすべて削除
            
            # ★★★ ログイン状態で遷移先を分岐させる ★★★
            if self.is_logged_in:
                # 🔒 ログイン済：削除画面（DeletePage）を開き、データを渡す
                current_page = DeletePage(self.root, self.controller, self.product_controller, product)
                current_page.target_product = product
                current_page.display(
                    product.product_name, 
                    product.product_id, 
                    product.deadline
                )
            else:
                # 🔓 未ログイン：受領画面（ReceivePage）を開く
                ReceivePage(self.root, self.controller, self.product_controller, product)