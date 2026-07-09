import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.product_controller import ProductController

class DeletedProductListPage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        """
        self.root = root
        self.controller = controller
        self.product_controller = ProductController()  # ProductController のインスタンスも保持
        # 画面の基本設定
        self.root.title("削除済み商品一覧画面")
        self.root.geometry("600x400")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="削除済み商品一覧", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=10)
        
        # 一覧を表示するためのテーブル（Treeview）の作成
        # クラス図の Deliveryitem の属性を想定して列を作成（商品ID、商品名、顧客名など）
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Customer", "Status"), show="headings")
        self.tree.heading("ID", text="商品ID")
        self.tree.heading("Name", text="商品名")
        self.tree.heading("Customer", text="顧客名")
        self.tree.heading("Status", text="ステータス")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Customer", width=150)
        self.tree.column("Status", width=100, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)
        
        # 下部に配置するボタンエリア
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=15)
        
        # ステータス編集画面を開くボタン
        self.btn_edit_status = tk.Button(
            self.btn_frame, 
            text="選択した商品のステータスを編集", 
            command=self.showStatusEditPage,
            bg="orange"
        )
        self.btn_edit_status.pack(side="left", padx=10)

    def displayList(self, deleted_list: list) -> None:
        """
        クラス図にある displayList メソッド
        コントローラーから削除済みリスト（ArrayList）を受け取って、テーブルに表示する
        """
        # まず既存のテーブル表示をクリア
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 受け取ったリスト（deleted_list）の中身をループで回してテーブルに追加
        # ※deleted_list の中は Deliveryitem オブジェクト、または辞書型を想定
        for item in deleted_list:
            # ここでは仮に item が辞書型、または特定の属性を持っているものとして処理
            # 例: item = {"id": 1, "name": "りんご", "customer": "大阪商店", "status": "削除済み"}
            self.tree.insert("", "end", values=(
                item.get("id", ""), 
                item.get("name", ""), 
                item.get("customer", ""), 
                item.get("status", "削除済み")
            ))
            
        # 画面を表示
        self.root.mainloop()

    def showStatusEditPage(self) -> None:
        """
        クラス図にある showStatusEditPage メソッド
        ステータス編集ボタンが押された時に、次の画面（StatusEditPage）を呼び出す
        """
        # テーブルで今どの行が選択されているかを取得
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("注意", "ステータスを編集する商品を選択してください。")
            return
            
        # 選択された行のデータを取得
        item_values = self.tree.item(selected_item, "values")
        product_id = item_values[0]
        
        # ここで次の画面（StatusEditPage）を生成して表示する
        # 本来はここで StatusEditPage のインスタンスを作って呼び出し
        # コントローラー経由で画面遷移をコントロール
        messagebox.showinfo("画面遷移", f"商品ID: {product_id} のステータス編集画面を開きます。")
        
        # TODO: StatusEditPage(self.root, self.controller).restoreItem() などの呼び出し