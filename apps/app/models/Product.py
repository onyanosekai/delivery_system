# product.py
import datetime
from typing import Lists

class Product:
    def __init__(self, product_id, product_name, customer_name, delivery_date, deadline, driver_id):
        self.product_id = product_id
        self.product_name = product_name
        self.customer_name = customer_name
        self.delivery_date = delivery_date
        self.deadline = deadline
        self.driver_id = driver_id

        self.status = "未受取"  # 初期状態は未受取
        
    def is_delivered(self):
        return self.status == "受取り済み"
    
    @classmethod
    def from_dict(cls, data: dict):
        """JSON（辞書型）からProductインスタンスを生成する"""
        return cls(
            product_id=data["product_id"],
            product_name=data["product_name"],
            customer_name=data["customer_name"],
            delivery_date=datetime.date.fromisoformat(data["delivery_date"]),
            deadline=datetime.date.fromisoformat(data["deadline"]),
            driver_id=int(data["driver_id"]),
            status=data.get("status", "未受取")
        )

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "customer_name": self.customer_name,
            "delivery_date": self.delivery_date.isoformat(),
            "deadline": self.deadline.isoformat(),
            "driver_id": self.driver_id,
            "status": self.status  
        }