import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class DeletePage(tk.Frame):
    def __init__(self, root, controller, product_controller,product):
        # 1. 親クラス（tk.Frame）の初期化
        super().__init__(root)

        self.root = root  # main.py の root を保持
        self.controller = controller
        self.product_controller = product_controller  # ProductController のインスタンスを保持
        self.target_product = product  # 削除対象のオブジェクト保持用
        
        # 画面の基本設定
        self.root.title("削除確認画面")
        self.root.geometry("400x300")  # ボタンが増えたので高さを少し広げました

        # --- 部品の配置（すべて root ではなく self の上に配置） ---
        self.label_title = tk.Label(self, text="以下の商品を削除しますか？", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)

        # 商品情報を表示するためのラベル群
        self.label_item_name = tk.Label(self, text="商品名: (未選択)", font=("Arial", 11))
        self.label_item_name.pack(pady=5)

        self.label_item_number = tk.Label(self, text="商品番号: (未選択)", font=("Arial", 11))
        self.label_item_number.pack(pady=5)

        self.label_deadline = tk.Label(self, text="期限: (未選択)", font=("Arial", 11))
        self.label_deadline.pack(pady=5)

        # 削除確定ボタン
        self.btn_delete = tk.Button(
            self,
            text="削除を確定する",
            bg="red",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_confirm_delete_clicked
        )
        self.btn_delete.pack(pady=15)

        # 「戻る」ボタン
        self.btn_back = tk.Button(
            self,
            text="メニューに戻る",
            bg="gray",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_back_clicked
        )
        self.btn_back.pack(pady=5)

        # ★★★【超重要】このFrame自体を画面いっぱいに配置する ★★★
        self.pack(fill="both", expand=True)

    def display(self, item_name: str, item_number: str, deadline) -> None:
        """データをラベルにセットするメソッド"""
        if isinstance(deadline, datetime):
            deadline_str = deadline.strftime("%Y-%m-%d")
        else:
            deadline_str = str(deadline)

        # ラベルの文字を書き換える
        self.label_item_name.config(text=f"商品名: {item_name}")
        self.label_item_number.config(text=f"商品番号: {item_number}")
        self.label_deadline.config(text=f"期限: {deadline_str}")

    def _on_confirm_delete_clicked(self):
        answer = messagebox.askyesno("最終確認", "本当に削除してもよろしいですか？")
        if answer:
            p_ctrl = self.controller.product_controller
            
            # ★すでに存在していた save_deleted_product を呼び出してJSONに保存
            if self.target_product and hasattr(p_ctrl, 'save_deleted_product'):
                p_ctrl.save_deleted_product(self.target_product)
            
            # 通常リストから削除する既存の処理（もしあればここに呼び出しを残す）
            # 例: p_ctrl.confirm_delete(self.target_product) などがあれば併記
            
            messagebox.showinfo("成功", "商品を削除し、消去済みリストに記録しました。")
            self._on_back_clicked()

    def _on_back_clicked(self):
        """現在の削除画面を破棄し、ログイン状態の初期メニュー画面を開き直す"""
        self.destroy()  # 削除画面を消し去る

        from app.views.initial_page import InitialPage
        # ログイン状態を維持したまま初期画面を生成
        app = InitialPage(self.root, self.controller, is_logged_in=True)
        self.controller.initial_page = app