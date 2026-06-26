from app.controllers.Product_controller import ProductController
from app.controllers.User_controller import UserController
from app.models.Product import Product
from app.models.Administrator import Administrator
from datetime import date


def main():
    product_controller = ProductController()
    user_controller = UserController()

    # 仮データ
    products = []
    deleted_products = []

    # 管理者（仮）
    admin = Administrator(1, "admin", "password")
    user_controller.create_admin(admin)

    # ===== ログイン =====
    print("=== ログイン ===")
    admin_id = int(input("ID: "))
    password = input("Password: ")

    if not user_controller.login(admin_id, password):
        print("ログイン失敗")
        return

    print("ログイン成功")

    # ===== メインループ =====
    while True:
        print("\n=== メニュー ===")
        print("1: 商品登録")
        print("2: 商品検索・受取")
        print("3: 商品削除")
        print("4: 削除済一覧")
        print("5: 終了")

        choice = input("選択: ")

        # ===== ① 商品登録 =====
        if choice == "1":
            print("\n=== 商品登録 ===")
            pid = input("商品番号: ")
            name = input("商品名: ")
            customer = input("顧客名: ")
            driver_id = 1  # 仮
            today = date.today()

            if product_controller.validate_product(
                pid, name, customer, today, today, driver_id
            ):
                product = Product(pid, name, customer, today, today, driver_id)
                products.append(product)
                print("登録成功")

        # ===== ② 検索＋受取 =====
        elif choice == "2":
            print("\n=== 商品検索 ===")
            pid = input("商品番号: ")
            customer = input("顧客名: ")

            product = product_controller.search_items(products, pid, customer)

            if product is None:
                print("エラー：商品が見つかりません")
                continue

            print("\n=== 受け取り画面 ===")
            print(f"商品名: {product.product_name}")

            if not product_controller.check_deadline(product.deadline):
                continue

            confirm = input("受け取りますか？(y/n): ")

            if confirm.lower() == "y":
                product_controller.receive_product(product)
                print("受け取り完了")

        # ===== ③ 削除 =====
        elif choice == "3":
            print("\n=== 商品削除 ===")

            pid = input("商品番号: ")

            target = None
            for p in products:
                if p.product_id == pid:
                    target = p
                    break

            if target is None:
                print("見つかりません")
                continue

            if not product_controller.check_deadline(target.deadline):
                continue

            products.remove(target)
            deleted_products.append(target)

            print("削除完了")

        # ===== ④ 削除済一覧 =====
        elif choice == "4":
            print("\n=== 削除済一覧 ===")
            for p in deleted_products:
                print(p.product_name)

        # ===== ⑤ 終了 =====
        elif choice == "5":
            print("終了します")
            break

        else:
            print("無効な入力")


if __name__ == "__main__":
    main()
