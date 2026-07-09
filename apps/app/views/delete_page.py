import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from app.controllers.product_controller import ProductController

class DeletePage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっているコントローラーを保持
        self.product_controller = ProductController()  # ProductController のインスタンスも保持

        # 画面の基本設定
        self.root.title("削除確認画面")
        self.root.geometry("400x250")
        
        # 画面上に配置する部品（ラベル）の準備
        self.label_title = tk.Label(root, text="以下の商品を削除しますか？", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=10)
        
        self.label_item_name = tk.Label(root, text="", font=("Arial", 11))
        self.label_item_name.pack(pady=5)
        
        self.label_item_number = tk.Label(root, text="", font=("Arial", 11))
        self.label_item_number.pack(pady=5)
        
        self.label_deadline = tk.Label(root, text="", font=("Arial", 11))
        self.label_deadline.pack(pady=5)
        
        # 削除確定ボタン（押したらコントローラーの confirmDelete を呼ぶ）
        self.btn_delete = tk.Button(
            root, 
            text="削除を確定する", 
            bg="red", 
            fg="white", 
            command=self._on_confirm_delete_clicked
        )
        self.btn_delete.pack(pady=15)

    def display(self, item_name: str, item_number: str, deadline: datetime) -> None:
        """
        クラス図にある display メソッド
        コントローラーから呼び出され、引数で受け取った商品情報を画面に表示する
        """
        # 日付を指定のフォーマット（例: 2026-06-26）の文字列に変換
        deadline_str = deadline.strftime("%Y-%m-%d") if isinstance(deadline, datetime) else str(deadline)
        
        # 画面のラベルに値をセット
        self.label_item_name.config(text=f"商品名: {item_name}")
        self.label_item_number.config(text=f"商品番号: {item_number}")
        self.label_deadline.config(text=f"期限: {deadline_str}")
        
        # 画面を表示
        self.root.mainloop()

    def _on_confirm_delete_clicked(self):
        """
        削除ボタンが押された時の内部処理
        """
        # ユーザーに最終確認のポップアップを出す
        answer = messagebox.askyesno("最終確認", "本当に削除してもよろしいですか？")
        
        if answer:
            # クラス図の「confirmDelete」の矢印に相当する処理
            # コントローラー側の confirmDelete メソッドを呼び出す
            # ※本来は削除対象のproductオブジェクトなどを渡します
            self.controller.confirmDelete()
            messagebox.showinfo("完了", "削除処理を要求しました。")
            self.root.destroy()  # 画面を閉じる