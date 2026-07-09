import tkinter as tk
from tkinter import messagebox
from app.controllers.product_controller import ProductController

class ReceivePage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        """
        self.root = root
        self.controller = controller  # クラス図で繋がっている productController を保持
        self.product_controller = ProductController()  # ProductController のインスタンスも保持

        # 画面の基本設定
        self.root.title("商品の受領確認画面")
        self.root.geometry("400x400")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="以下の商品を受領（確認）します", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # 商品情報を表示するためのラベル群（初期値は空文字）
        self.label_item_name = tk.Label(root, text="", font=("Arial", 12))
        self.label_item_name.pack(pady=5)
        
        self.label_item_number = tk.Label(root, text="", font=("Arial", 12))
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

    def displayItem(self, item_name: str, item_number: str) -> None:
        """
        クラス図にある displayItem メソッド
        コントローラーから呼び出され、引数で受け取った商品情報を画面に表示する
        """
        # クラス図に指定されている2つの引数を画面のラベルにセット
        self.label_item_name.config(text=f"商品名: {item_name}")
        self.label_item_number.config(text=f"商品番号: {item_number}")
        
        # 画面を表示
        self.root.mainloop()

    def _on_confirm_clicked(self):
        """
        「受領を確定する」ボタンが押された時の内部処理
        """
        # ユーザーへの最終確認ポップアップ
        answer = messagebox.askyesno("確認", "この商品を受領したことで確定しますか？")
        
        if answer:
            # クラス図の「confirmReceive」の点線矢印に相当する処理
            # productController 側の confirmReceive メソッドを呼び出して通知
            if hasattr(self.controller, 'confirmReceive'):
                # 本来はどの商品を処理するか、引数で商品オブジェクトなどを渡す
                self.controller.confirmReceive()
            else:
                # まだコントローラー側に実装がない場合の仮ログ
                print("[Debug] productController.confirmReceive() が呼び出されました。")
                
            messagebox.showinfo("完了", "受領確認を記録しました。")
            self.root.destroy()  # 処理が終わったら画面を閉じる