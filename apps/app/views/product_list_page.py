import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.product_controller import ProductController

class ProductListPage:
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
        self.root.title("商品一覧画面")
        self.root.geometry("600x450")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="商品一覧（配送リスト）", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=10)
        
        # 一覧を表示するためのテーブル（Treeview）の作成
        # クラス図の Deliveryitem（またはProduct）の属性を想定して列を作成
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Customer", "Deadline", "Status"), show="headings")
        self.tree.heading("ID", text="商品ID")
        self.tree.heading("Name", text="商品名")
        self.tree.heading("Customer", text="顧客名")
        self.tree.heading("Deadline", text="期限")
        self.tree.heading("Status", text="ステータス")
        
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Name", width=130)
        self.tree.column("Customer", width=130)
        self.tree.column("Deadline", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)
        
        # 下部に配置するアクションボタンのエリア
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=15)
        
        # 1. ステータス編集画面を表示するボタン（showStatusEditPage に対応）
        self.btn_show_edit = tk.Button(
            self.btn_frame, 
            text="ステータス編集画面を開く", 
            command=self._on_show_status_edit_clicked,
            bg="lightblue"
        )
        self.btn_show_edit.pack(side="left", padx=10)
        
        # 2. 直近のステータスを変更するボタン（changeStatus に対応）
        self.btn_change_status = tk.Button(
            self.btn_frame, 
            text="簡易ステータス変更", 
            command=self._on_change_status_clicked,
            bg="lightgreen"
        )
        self.btn_change_status.pack(side="left", padx=10)

    def displayList(self, delivery_list: list) -> None:
        """
        クラス図にある displayList メソッド
        コントローラーから配送リスト（ArrayList）を受け取ってテーブルに表示する
        """
        # 既存のテーブル表示を一度クリア
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 受け取ったリスト（delivery_list）の中身をループで回してテーブルに追加
        for item in delivery_list:
            # item は辞書型、またはオブジェクトを想定
            self.tree.insert("", "end", values=(
                item.get("id", ""), 
                item.get("name", ""), 
                item.get("customer", ""), 
                item.get("deadline", ""), 
                item.get("status", "")
            ))
            
        # 画面を表示
        self.root.mainloop()

    def _on_show_status_edit_clicked(self):
        """
        「ステータス編集画面を開く」ボタンが押された時（クラス図の showStatusEditPage 矢印に相当）
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("注意", "商品を選択してください。")
            return
            
        item_values = self.tree.item(selected_item, "values")
        product_id = item_values[0]
        
        # 本来はここで StatusEditPage を呼び出す
        messagebox.showinfo("画面遷移", f"商品ID: {product_id} のステータス編集画面（StatusEditPage）を開きます。")

    def _on_change_status_clicked(self):
        """
        「簡易ステータス変更」ボタンが押された時（クラス図の changeStatus 矢印に相当）
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("注意", "商品を選択してください。")
            return
            
        item_values = self.tree.item(selected_item, "values")
        product_id = item_values[0]
        
        # 本来はコントローラー経由、もしくは直接 StatusEditPage に変更を通知
        messagebox.showinfo("ステータス変更", f"商品ID: {product_id} のステータス変更（changeStatus）を要求しました。")