import datetime
import json
import os
from typing import List, Optional
from app.models.Product import Product


class ProductController:
    PRODUCT_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Product.json")
    DELETED_JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/Deleted_product.json")


    #=================================登録=========================================
    def validate_product(self, product_id, product_name, customer_name, delivery_date, deadline, driver_id):
        if not product_id or not product_name or not customer_name or not delivery_date or not deadline or not driver_id:
            print("error: 全ての項目を入力してください。")
            return False

        if len(product_id) != 11:
            print("error: 商品番号は11桁である必要があります。")
            return False
        
        if len(product_name) > 80:
            print("error: 商品名は80文字以内である必要があります。")
            return False
    
        if len(customer_name) > 80:
            print("error: 顧客名は80文字以内である必要があります。")
            return False

        if delivery_date < datetime.date.today():
            print("error: 過去の日付は登録できません。")
            return False

        return True
    
    #===============================期限チェック=========================================
    def check_deadline(self,deadline):
        if datetime.date.today() > deadline:
            print("error: 受け取り期限が過ぎています。")
            return False
        return True
    
    #==============================商品検索=========================================
    def search_items(self,products,product_id,customer_name):
        for product in products:
            if product.product_id == product_id and product.customer_name == customer_name:
                return product
        return None
    

    #==============================削除処理=========================================
    def confirm_delete(self, products: List[Product], target_product: Product) -> bool:
        if target_product in products:
            products.remove(target_product)
            print(f"success: 商品名「{target_product.product_name}」のデータを削除しました。")
            return True
        else:
            print("error: 削除対象の商品が見つかりません。")
            return False
        
    #==============================受取処理=========================================
    def receive_product(self, product: Product) -> None:
        product.status = "受取り済み"
        print(f"success: 商品名「{product.product_name}」の受取が完了しました。")