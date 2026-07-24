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
        
        self.products: List[Product] = []
        self.load_products_from_json()

    #=============================Product.jsonからの読み込み========================================
    def load_products_from_json(self):
        if not os.path.exists(self.PRODUCT_JSON_PATH):
            return

        with open(self.PRODUCT_JSON_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.products = [
                    Product.from_dict(item)
                    for item in data
                ]
            except json.JSONDecodeError:
                self.products = []


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
            messagebox.showerror("エラー", "納品日は本日の日付以降である必要があります。")
            return False
        
        if deadline < delivery_date:
            messagebox.showerror("エラー", "受け取り期限は納品日以降である必要があります。")
            return False

        if not driver_id.isdigit():
            messagebox.showerror("エラー", "配達員IDは数字のみ入力してください。")
            return False


        return True
    
    #=============================削除した商品をDeleted_product.jsonに保存=========================================
    def save_deleted_product(self, product: Product):

        if os.path.exists(self.DELETED_JSON_PATH):
            with open(self.DELETED_JSON_PATH, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(product.to_dict())

        with open(self.DELETED_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    #==============================商品検索=========================================
    def search_items(self,product_id: str,customer_name: str):
        for product in self.products:
            if product.product_id == product_id and product.customer_name == customer_name:
                return product
        return None

    #==============================削除処理=========================================
    def confirm_delete(self, target_product: Product) -> bool:
        if target_product in self.products:
            self.save_deleted_product(target_product)
            self.products.remove(target_product)
            self.save_products_to_json()
            self.save_products_to_json()  # 削除後にJSONに保存
            messagebox.showinfo("成功", f"商品名「{target_product.product_name}」のデータを削除しました。")
            return True
        else:
            messagebox.showerror("エラー", "削除対象の商品が見つかりません。")
            return False
        
    #=============================受け取り期限切れの表示=========================================
    def get_expired_products(self) -> List[Product]:
        today = datetime.date.today()
        if self.puroduct.deadline < today:
            messagebox.showwarning("期限切れ", f"商品名「{self.product.product_name}」の受け取り期限が過ぎています。")

    #==============================受取処理=========================================
    def receive_product(self, product: Product) -> None:
        #print("変更前のステータス:", product.status)  # デバッグ用
        product.status = "受取り済み"
        #print("変更後のステータス:", product.status)  # デバッグ用
        self.save_products_to_json()

    #=============================商品登録=========================================
    def register_product(self, product_id, product_name, customer_name, delivery_date, deadline, driver_id):
        if not self.validate_product(product_id, product_name, customer_name, delivery_date, deadline, driver_id):
            return False
        product = Product(product_id, product_name, customer_name, delivery_date, deadline, driver_id)
        self.products.append(product)
        self.save_products_to_json()  
        return True

    #=============================商品のProduct.jsonへの保存========================================
    def save_products_to_json(self):
        data = [product.to_dict() for product in self.products]

        print(data) 

        with open(self.PRODUCT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
