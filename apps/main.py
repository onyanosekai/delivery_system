import tkinter as tk
from app.views.initial_page import InitialPage
# ★ ProductController から UserController に変更します
from app.controllers.User_controller import UserController

def main():
    # 1. ルートウィンドウの作成
    root = tk.Tk()
    root.title("配送管理システム")
    root.geometry("500x400")

    # 2. 初期画面（InitialPage）の呼び出し
    # ★ ここで画面遷移の機能を持っている UserController を生成して渡します！
    controller = UserController()
    
    # UserControllerのインスタンスに root や initial_page の情報を持たせる
    controller.root = root
    app = InitialPage(root, controller)
    controller.initial_page = app

    # 3. メインループの実行
    root.mainloop()

def show_delete_page(self, item_name, item_number, deadline, product_obj):
        """商品データを引き連れて削除画面へ遷移する"""
        self.show_page(DeletePage)
        
        current_page = self.container.winfo_children()[-1]
        
        if isinstance(current_page, DeletePage):
            # 削除画面に商品情報と、オブジェクト自体を覚えさせる
            current_page.target_product = product_obj
            current_page.display(item_name, item_number, deadline)

if __name__ == "__main__":
    main()