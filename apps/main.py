from app.controllers.product_controller import ProductController
from app.controllers.User_controller import UserController
from app.models.Product import Product
from app.models.Administrator import Administrator
from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk


class DeliveryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("配送管理システム")
        self.root.geometry("500x400")

        # コントローラーとデータの初期化
        self.product_controller = ProductController()
        self.user_controller = UserController()
        self.products = []
        self.deleted_products = []

        # 画面の初期化（最初は登録・ログイン画面）
        self.create_auth_screen()

    # --- 画面1: 登録・ログイン画面 ---
    def create_auth_screen(self):
        self.auth_frame = tk.Frame(self.root)
        self.auth_frame.pack(pady=20)

        # ユーザー登録部分
        tk.Label(self.auth_frame, text="【ユーザー登録】", font=("", 12, "bold")).grid(
            row=0, column=0, columnspan=2, pady=5
        )
        tk.Label(self.auth_frame, text="登録ID:").grid(row=1, column=0)
        self.reg_id_entry = tk.Entry(self.auth_frame)
        self.reg_id_entry.grid(row=1, column=1)

        tk.Label(self.auth_frame, text="名前:").grid(row=2, column=0)
        self.reg_name_entry = tk.Entry(self.auth_frame)
        self.reg_name_entry.grid(row=2, column=1)

        tk.Label(self.auth_frame, text="パスワード:").grid(row=3, column=0)
        self.reg_pass_entry = tk.Entry(self.auth_frame, show="*")
        self.reg_pass_entry.grid(row=3, column=1)

        tk.Button(self.auth_frame, text="登録", command=self.handle_register).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # ログイン部分
        tk.Label(self.auth_frame, text="【ログイン】", font=("", 12, "bold")).grid(
            row=5, column=0, columnspan=2, pady=5
        )
        tk.Label(self.auth_frame, text="ログインID:").grid(row=6, column=0)
        self.login_id_entry = tk.Entry(self.auth_frame)
        self.login_id_entry.grid(row=6, column=1)

        tk.Label(self.auth_frame, text="パスワード:").grid(row=7, column=0)
        self.login_pass_entry = tk.Entry(self.auth_frame, show="*")
        self.login_pass_entry.grid(row=7, column=1)

        tk.Button(self.auth_frame, text="ログイン", command=self.handle_login).grid(
            row=8, column=0, columnspan=2, pady=10
        )

    def handle_register(self):
        admin_id = self.reg_id_entry.get()
        name = self.reg_name_entry.get()
        password = self.reg_pass_entry.get()

        if admin_id and name and password:
            self.user_controller.create_admin(admin_id, name, password)
            messagebox.showinfo("成功", "ユーザー登録が完了しました。")
        else:
            messagebox.showwarning("エラー", "全ての項目を入力してください。")

    def handle_login(self):
        try:
            admin_id = int(self.login_id_entry.get())
            password = self.login_pass_entry.get()
        except ValueError:
            messagebox.showerror("エラー", "IDは数値で入力してください。")
            return

        if self.user_controller.login(admin_id, password):
            messagebox.showinfo("成功", "ログイン成功！")
            self.auth_frame.destroy()  # ログイン画面を消す
            self.create_main_screen()  # メインメニュー画面を作る
        else:
            messagebox.showerror("失敗", "ログイン失敗。IDまたはパスワードが違います。")

    # --- 画面2: メインメニュー画面（タブ切り替え） ---
    def create_main_screen(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 各機能のタブ（フレーム）を作成
        self.tab_register = tk.Frame(self.notebook)
        self.tab_search = tk.Frame(self.notebook)
        self.tab_delete = tk.Frame(self.notebook)
        self.tab_list = tk.Frame(self.notebook)

        self.notebook.add(self.tab_register, text="商品登録")
        self.notebook.add(self.tab_search, text="検索・受取")
        self.notebook.add(self.tab_delete, text="商品削除")
        self.notebook.add(self.tab_list, text="削除済一覧")

        # 各タブの中身を組み立てる
        self.setup_register_tab()
        self.setup_search_tab()
        self.setup_delete_tab()
        self.setup_list_tab()

    # ===== ① 商品登録タブ =====
    def setup_register_tab(self):
        tk.Label(self.tab_register, text="商品番号:").grid(row=0, column=0, pady=5)
        self.p_id_entry = tk.Entry(self.tab_register)
        self.p_id_entry.grid(row=0, column=1)

        tk.Label(self.tab_register, text="商品名:").grid(row=1, column=0, pady=5)
        self.p_name_entry = tk.Entry(self.tab_register)
        self.p_name_entry.grid(row=1, column=1)

        tk.Label(self.tab_register, text="顧客名:").grid(row=2, column=0, pady=5)
        self.p_cust_entry = tk.Entry(self.tab_register)
        self.p_cust_entry.grid(row=2, column=1)

        tk.Button(
            self.tab_register, text="登録", command=self.handle_product_register
        ).grid(row=3, column=0, columnspan=2, pady=10)

    def handle_product_register(self):
        pid = self.p_id_entry.get()
        name = self.p_name_entry.get()
        customer = self.p_cust_entry.get()
        driver_id = 1
        today = date.today()

        if self.product_controller.validate_product(
            pid, name, customer, today, today, driver_id
        ):
            product = Product(pid, name, customer, today, today, driver_id)
            self.products.append(product)
            messagebox.showinfo("成功", f"商品「{name}」を登録しました。")
            # 入力欄をクリア
            self.p_id_entry.delete(0, tk.END)
            self.p_name_entry.delete(0, tk.END)
            self.p_cust_entry.delete(0, tk.END)
            self.refresh_deleted_list()

    # ===== ② 検索・受取タブ =====
    def setup_search_tab(self):
        tk.Label(self.tab_search, text="商品番号:").grid(row=0, column=0, pady=5)
        self.s_id_entry = tk.Entry(self.tab_search)
        self.s_id_entry.grid(row=0, column=1)

        tk.Label(self.tab_search, text="顧客名:").grid(row=1, column=0, pady=5)
        self.s_cust_entry = tk.Entry(self.tab_search)
        self.s_cust_entry.grid(row=1, column=1)

        tk.Button(self.tab_search, text="検索", command=self.handle_search).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def handle_search(self):
        pid = self.s_id_entry.get()
        customer = self.s_cust_entry.get()

        product = self.product_controller.search_items(self.products, pid, customer)

        if product is None:
            messagebox.showerror("エラー", "商品が見つかりません。")
            return

        if not self.product_controller.check_deadline(product.deadline):
            messagebox.showwarning("期限切れ", "期限が切れています。")
            return

        confirm = messagebox.askyesno(
            "受け取り確認", f"商品名: {product.product_name}\n受け取りますか？"
        )
        if confirm:
            self.product_controller.receive_product(product)
            messagebox.showinfo("完了", "受け取りが完了しました。")

    # ===== ③ 削除タブ =====
    def setup_delete_tab(self):
        tk.Label(self.tab_delete, text="削除する商品番号:").grid(row=0, column=0, pady=5)
        self.d_id_entry = tk.Entry(self.tab_delete)
        self.d_id_entry.grid(row=0, column=1)

        tk.Button(self.tab_delete, text="削除", command=self.handle_delete).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    def handle_delete(self):
        pid = self.d_id_entry.get()
        target = None

        for p in self.products:
            if p.product_id == pid:
                target = p
                break

        if target is None:
            messagebox.showerror("エラー", "商品が見つかりません。")
            return

        if not self.product_controller.check_deadline(target.deadline):
            messagebox.showwarning("エラー", "期限切れのため削除できません。")
            return

        self.products.remove(target)
        self.deleted_products.append(target)
        messagebox.showinfo("完了", f"商品「{target.product_name}」を削除しました。")
        self.d_id_entry.delete(0, tk.END)
        self.refresh_deleted_list()

    # ===== ④ 削除済一覧タブ =====
    def setup_list_tab(self):
        self.deleted_listbox = tk.Listbox(self.tab_list, width=40, height=15)
        self.deleted_listbox.pack(padx=10, pady=10)

    def refresh_deleted_list(self):
        # リストボックスの中身を最新にする
        self.deleted_listbox.delete(0, tk.END)
        for p in self.deleted_products:
            self.deleted_listbox.insert(tk.END, p.product_name)


def main():
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()