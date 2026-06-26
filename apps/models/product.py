# product.py
class Product:
    def __init__(self, product_id, product_name, customer_name, delivery_date, deadline, driver_id):
        self.product_id = product_id
        self.product_name = product_name
        self.customer_name = customer_name
        self.delivery_date = delivery_date
        self.deadline = deadline
        self.driver_id = driver_id

    def is_delivered(self):
        return False