import tkinter as tk
from app.views.initial_page import InitialPage
from app.views.delete_page import DeletePage 
from app.controllers.User_controller import UserController
from app.controllers.product_controller import ProductController 

def main():
    root = tk.Tk()
    root.title("配送管理システム")
    root.geometry("500x400")

    controller = UserController()
    controller.product_controller = ProductController() 

    controller.root = root
    app = InitialPage(root, controller)
    controller.initial_page = app

    def show_delete_page(item_name, item_number, deadline, product_obj):
        """商品データを引き連れて削除画面へ遷移する"""
        
        if hasattr(controller, 'initial_page') and hasattr(controller.initial_page, 'frame'):
            controller.initial_page.frame.destroy()
            
        current_page = DeletePage(root, controller)
        current_page.pack(fill="both", expand=True)
        
        current_page.target_product = product_obj
        current_page.display(item_name, item_number, deadline)

    controller.show_delete_page = show_delete_page

    
    root.mainloop()

if __name__ == "__main__":
    main()