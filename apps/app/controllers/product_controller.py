import datetime


class ProductController:

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
    
    def check_deadline(self,deadline):
        if datetime.date.today() > deadline:
            print("error: 受け取り期限が過ぎています。")
            return False
        return True

    def search_items(self,products,product_id,customer_name):
        for product in products:
            if product.product_id == product_id and product.customer_name == customer_name:
                return product
        return None

    def confirm_delete(self,product): 
        
        pass