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

if __name__ == "__main__":
    main()