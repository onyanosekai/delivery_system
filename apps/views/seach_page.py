import tkinter as tk
from tkinter import messagebox

class SerchPage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている productController を保持
        
        # 画面の基本設定
        self.root.title("商品検索画面")
        self.root.geometry("450x350")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="商品検索・受領要求", font=("Arial", 14, "bold"))
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
        
        # 受領要求ボタン（requestReceive を実行）
        self.btn_receive = tk.Button(
            self.btn_frame, 
            text="受領要求を送信", 
            bg="darkgreen", 
            fg="white", 
            font=("Arial", 10, "bold"),
            width=15,
            command=self.requestReceive
        )
        self.btn_receive.pack(side="left", padx=10)

    def inputProductInfo(self, customer_name: str, item_number: str) -> None:
        """
        クラス図にある inputProductInfo メソッド
        入力された検索条件を productController の seach 処理へ引き渡す
        """
        # クラス図の「seach」の点線矢印に相当する処理
        if hasattr(self.controller, 'seachItems'): # コントローラー側の検索メソッド（図内はseachitems）
            self.controller.seachItems(item_number, customer_name)
        else:
            print(f"[Debug] productControllerへ検索要求: 顧客名={customer_name}, 商品番号={item_number}")
            
        messagebox.showinfo("検索", "検索要求を送信しました。")

    def requestReceive(self) -> None:
        """
        クラス図にある requestReceive メソッド
        受領要求アクションを productController へ通知する
        """
        # クラス図の「confirmReceive」の点線矢印（左側）に相当する処理
        if hasattr(self.controller, 'confirmReceive'):
            self.controller.confirmReceive()
        else:
            print("[Debug] productController.confirmReceive() へ受領要求を通知しました。")
            
        messagebox.showinfo("受領要求", "受領要求をコントローラーへ通知しました。")

    def _on_search_clicked(self):
        """
        「商品を検索」ボタンが押された時の内部処理
        """
        customer_name = self.entry_customer.get().strip()
        item_number = self.entry_item_num.get().strip()
        
        if not customer_name or not item_number:
            messagebox.showwarning("入力エラー", "顧客名と商品番号の両方を入力してください。")
            return
            
        # クラス図の指定通り、メソッドに入力データを渡して実行
        self.inputProductInfo(customer_name, item_number)

    def display(self):
        """画面を表示するための補助メソッド"""
        self.root.mainloop()