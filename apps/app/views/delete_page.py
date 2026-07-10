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

        self.btn_back = tk.Button(
            self,
            text="戻る",
            bg="gray",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self._on_back_clicked,  # ボタンが押されたら下のメソッドを呼ぶ
        )
        self.btn_back.pack(pady=5)

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
        answer = messagebox.askyesno("最終確認", "本当に削除してもよろしいですか？")
        if answer:
            # product_controller.py に実装されている confirm_delete を呼び出す
            p_ctrl = self.controller.product_controller
            
            # 保持しておいた商品オブジェクトをそのまま渡して削除を実行！
            if p_ctrl.confirm_delete(self.target_product):
                # 削除が成功したら自動でポップアップが出るので、そのまま初期画面に戻る
                self._on_back_clicked()

    def _on_back_clicked(self):
        """現在の削除画面を破棄し、ログイン状態の初期メニュー画面を開き直す"""
        # 1. 自身の Frame を画面から消し去る
        self.destroy()

        # 2. 循環インポートを防ぐために、この関数内で InitialPage をインポートする
        from app.views.initial_page import InitialPage

        # 3. ログイン状態を引き継いで（is_logged_in=True）初期メニュー画面を表示する
        # （すでに削除画面にいる＝ログインに成功している状態なので True で固定します）
        app = InitialPage(self.root, self.controller, is_logged_in=True)

        # 4. controller側が持っているメニューの参照も最新に更新しておく
        self.controller.initial_page = app