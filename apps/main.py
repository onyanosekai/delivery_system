import tkinter as tk
from app.views.initial_page import InitialPage
# ★ 追加：DeletePage をインポートする
from app.views.delete_page import DeletePage 
# ★ ProductController から UserController に変更します
from app.controllers.User_controller import UserController
from app.controllers.product_controller import ProductController # これも念のため必要です

def main():
    # # 1. ルートウィンドウの作成
    root = tk.Tk()
    root.title("配送管理システム")
    root.geometry("500x400")

    # # 2. 初期画面 (InitialPage) の呼び出し
    controller = UserController()
    # 削除ボタンの検索で使うため、product_controller も持たせておきます
    controller.product_controller = ProductController() 

    controller.root = root
    app = InitialPage(root, controller)
    controller.initial_page = app

    # ★ 修正：main() の中で呼び出せるように、ここに引っ越し（インデントを下げる）
    # 元々あった self は、この構成だと不要になるので削るか root などに置き換えます
    def show_delete_page(item_name, item_number, deadline, product_obj):
        """商品データを引き連れて削除画面へ遷移する"""
        
        # 現在の initial_page のフレーム（土台）を消す
        if hasattr(controller, 'initial_page') and hasattr(controller.initial_page, 'frame'):
            controller.initial_page.frame.destroy()
            
        # 新しい削除画面を生成する
        # ※現在の構成に合わせて、DeletePageにrootとcontrollerを渡して直接配置します
        current_page = DeletePage(root, controller)
        current_page.pack(fill="both", expand=True)
        
        # 削除画面にオブジェクトとデータをセットして表示
        current_page.target_product = product_obj
        current_page.display(item_name, item_number, deadline)

    # 他の画面からこの show_delete_page を呼べるように controller に覚えさせておく
    controller.show_delete_page = show_delete_page

    # # 3. メインループの実行
    root.mainloop()

if __name__ == "__main__":
    main()