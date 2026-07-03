import tkinter as tk
from app.views.initial_page import InitialPage
from app.controllers.product_controller import ProductController

def main():
    # 1. ルートウィンドウの作成
    root = tk.Tk()
    root.title("配送管理システム")
    root.geometry("500x400")

    # 2. 初期画面（InitialPage）の呼び出し
    # 各画面の遷移制御やコントローラーの初期化は、InitialPageや各View/Controllerで行います
    controller = ProductController()
    app = InitialPage(root, controller)

    # 3. メインループの実行
    root.mainloop()

if __name__ == "__main__":
    main()