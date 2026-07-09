import datetime
import json
import os
from tkinter import messagebox
from typing import List, Optional
from app.models.Product import Product


class ProductController:
    PRODUCT_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Product.json")
    DELETED_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Deleted_product.json")

    def __init__(self):
        # コントローラーがデータリストを保持するようにする
        self.products: List[Product] = []

    #=================================登録=========================================
    def validate_product(self, product_id, product_name, customer_name, delivery_date, deadline, driver_id):

        if len(product_id) != 11:
            messagebox.showerror("エラー", "商品番号は11桁である必要があります。")
            return False
        
        if len(product_name) > 80:
            messagebox.showerror("エラー", "商品名は80文字以内である必要があります。")
            return False
    
        if len(customer_name) > 80:
            messagebox.showerror("エラー", "顧客名は80文字以内である必要があります。")
            return False

        if delivery_date < datetime.date.today():
            messagebox.showerror("エラー", "本日の日付を入力してください。")
            return False
        if delivery_date > datetime.date.today():
            messagebox.showerror("エラー", "本日の日付を入力してください。")
            return False
        


        return True
    
    
    #==============================商品検索=========================================
    def search_items(self,product_id: str,customer_name: str):
        for product in self.products:
            if product.product_id == product_id and product.customer_name == customer_name:
                return product
            else:
                return None
    

    #==============================削除処理=========================================
    def confirm_delete(self, target_product: Product) -> bool:
        if target_product in self.products:
            self.products.remove(target_product)
            messagebox.showinfo("成功", f"商品名「{target_product.product_name}」のデータを削除しました。")
            return True
        else:
            messagebox.showerror("エラー", "削除対象の商品が見つかりません。")
            return False
        
    #==============================受取処理=========================================
    def receive_product(self, product: Product) -> None:
        product.status = "受取り済み"

    def register_product(self, product_id, product_name, customer_name, delivery_date, deadline, driver_id):
        if not self.validate_product(product_id, product_name, customer_name, delivery_date, deadline, driver_id):
            return False
        product = Product(product_id, product_name, customer_name, delivery_date, deadline, driver_id)
        self.products.append(product)
        self.save_products_to_json()  # 登録後にJSONに保存
        return True

    #=============================商品のProduct.jsonへの保存========================================
    def save_products_to_json(self):
        data = [product.to_dict() for product in self.products]
        with open(self.PRODUCT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
