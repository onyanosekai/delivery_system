import tkinter as tk
from tkinter import messagebox

class InfoRegistrationPage:
    def __init__(self, root, controller):
        """
        初期化メソッド
        :param root: Tkinterのメインウィンドウ
        :param controller: productController のインスタンス
        """
        self.root = root
        self.controller = controller
        
        # 画面の基本設定
        self.root.title("情報登録画面")
        self.root.geometry("450x300")
        
        # タイトルラベル
        self.label_title = tk.Label(root, text="情報登録", font=("Arial", 14, "bold"))
        self.label_title.pack(pady=15)
        
        # 入力説明のラベル
        self.label_hint = tk.Label(root, text="登録する情報を入力してください：", font=("Arial", 10))
        self.label_hint.pack(anchor="w", padx=30, pady=5)
        
        # 情報入力欄（複数行入力できるように Text ウィジェットを使用）
        self.text_info = tk.Text(root, height=6, width=50, font=("Arial", 10))
        self.text_info.pack(padx=30, pady=5)
        
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

    def submit(self, info: str) -> None:
        """
        クラス図にある submit メソッド
        入力された情報をコントローラーの register 処理へ引き渡す
        """
        # クラス図の「register」の矢印に相当する処理
        # productController に info（文字列）を渡して処理を依頼する
        # ※実際のコントローラー側のメソッド名に合わせて呼び出し
        if hasattr(self.controller, 'register'):
            self.controller.register(info)
        else:
            # まだコントローラー側に実装がない場合の仮ログ
            print(f"[Debug] productController.register('{info}') が要求されました。")
            
        messagebox.showinfo("成功", "情報を送信しました。")
        self.root.destroy()  # 登録が終わったら画面を閉じる

    def _on_submit_clicked(self):
        """
        「登録する」ボタンが押された時の内部処理
        """
        # 入力欄からテキストを取得（前後の余白を削除）
        input_data = self.text_info.get("1.0", "end-1c").strip()
        
        # バリデーション：未入力チェック
        if not input_data:
            messagebox.showwarning("入力エラー", "情報が入力されていません。")
            return
            
        # クラス図の指定通り、submit メソッドに入力データを渡して実行
        self.submit(input_data)
        
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