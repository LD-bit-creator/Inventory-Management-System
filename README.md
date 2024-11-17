import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from fpdf import FPDF
import datetime

# Initialize the SQLite database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create necessary tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL
)""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity_purchased INTEGER NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
)""")
conn.commit()

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")

        # Initialize UI setup
        self.setup_login_frame()
        self.setup_menu_frame()
        self.setup_add_product_frame()
        self.setup_delete_product_frame()
        self.setup_search_product_frame()
        self.setup_record_purchase_frame()
        self.setup_reporting_frame()

        # Initialize Treeview for product history in Add Product page
        self.product_tree = ttk.Treeview(self.add_product_frame, columns=("ID", "Name", "Quantity", "Price", "Category"), show="headings")
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Quantity", text="Quantity")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.pack(fill=tk.BOTH, expand=True, pady=20)

        # Initialize label for purchase history in Record Purchase page
        self.purchase_history_label = tk.Label(self.record_purchase_frame, text="")
        self.purchase_history_label.pack(pady=10)

    def setup_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        tk.Label(self.login_frame, text="Inventory Management System", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.login_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        tk.Label(self.login_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()
        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)
        self.login_frame.pack()

    def setup_menu_frame(self):
        self.menu_frame = tk.Frame(self.root)
        tk.Label(self.menu_frame, text="Main Menu", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Add Product", command=self.show_add_product_page).pack(pady=5)
        tk.Button(self.menu_frame, text="Delete Product", command=self.show_delete_product_page).pack(pady=5)
        tk.Button(self.menu_frame, text="Search Product", command=self.show_search_product_page).pack(pady=5)
        tk.Button(self.menu_frame, text="Record a Purchase", command=self.show_record_purchase_page).pack(pady=5)
        tk.Button(self.menu_frame, text="Sales and Reporting", command=self.show_reporting_page).pack(pady=5)

    def setup_add_product_frame(self):
        self.add_product_frame = tk.Frame(self.root)
        tk.Label(self.add_product_frame, text="Add Product", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.add_product_frame, text="Name").pack()
        self.name_entry = tk.Entry(self.add_product_frame)
        self.name_entry.pack()
        tk.Label(self.add_product_frame, text="Quantity").pack()
        self.quantity_entry = tk.Entry(self.add_product_frame)
        self.quantity_entry.pack()
        tk.Label(self.add_product_frame, text="Price").pack()
        self.price_entry = tk.Entry(self.add_product_frame)
        self.price_entry.pack()
        tk.Label(self.add_product_frame, text="Category").pack()
        self.category_entry = tk.Entry(self.add_product_frame)
        self.category_entry.pack()
        tk.Button(self.add_product_frame, text="Add Product", command=self.add_product).pack(pady=10)
        tk.Button(self.add_product_frame, text="Back to Menu", command=self.back_to_menu).pack()

    def setup_delete_product_frame(self):
        self.delete_product_frame = tk.Frame(self.root)
        tk.Label(self.delete_product_frame, text="Delete Product", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.delete_product_frame, text="Product ID").pack()
        self.delete_product_id_entry = tk.Entry(self.delete_product_frame)
        self.delete_product_id_entry.pack()
        tk.Button(self.delete_product_frame, text="Delete Product", command=self.delete_product).pack(pady=10)
        tk.Button(self.delete_product_frame, text="Back to Menu", command=self.back_to_menu).pack()

    def setup_search_product_frame(self):
        self.search_product_frame = tk.Frame(self.root)
        tk.Label(self.search_product_frame, text="Search Product", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.search_product_frame, text="Product Name").pack()
        self.search_entry = tk.Entry(self.search_product_frame)
        self.search_entry.pack()
        tk.Button(self.search_product_frame, text="Search", command=self.search_product).pack(pady=5)
        self.search_result_label = tk.Label(self.search_product_frame, text="")
        self.search_result_label.pack(pady=10)
        tk.Button(self.search_product_frame, text="Back to Menu", command=self.back_to_menu).pack()

    def setup_record_purchase_frame(self):
        self.record_purchase_frame = tk.Frame(self.root)
        tk.Label(self.record_purchase_frame, text="Record Purchase", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.record_purchase_frame, text="Product ID").pack()
        self.product_id_entry = tk.Entry(self.record_purchase_frame)
        self.product_id_entry.pack()
        tk.Label(self.record_purchase_frame, text="Quantity Purchased").pack()
        self.quantity_purchased_entry = tk.Entry(self.record_purchase_frame)
        self.quantity_purchased_entry.pack()
        tk.Button(self.record_purchase_frame, text="Record Purchase", command=self.record_purchase).pack(pady=10)
        tk.Button(self.record_purchase_frame, text="Back to Menu", command=self.back_to_menu).pack()

    def setup_reporting_frame(self):
        self.reporting_frame = tk.Frame(self.root)
        tk.Label(self.reporting_frame, text="Sales and Reporting", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.reporting_frame, text="Daily Sales Report", command=self.daily_sales_report).pack(pady=5)
        tk.Button(self.reporting_frame, text="Top Selling Products", command=self.top_selling_products).pack(pady=5)
        tk.Button(self.reporting_frame, text="Revenue Analysis", command=self.total_revenue).pack(pady=5)
        tk.Button(self.reporting_frame, text="Export Sales Report to PDF", command=self.export_sales_to_pdf).pack(pady=5)
        self.sales_report_label = tk.Label(self.reporting_frame, text="")
        self.sales_report_label.pack(pady=10)
        tk.Button(self.reporting_frame, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "password":
            self.show_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def add_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        category = self.category_entry.get()
        if name and quantity and price and category:
            cursor.execute("INSERT INTO products (name, quantity, price, category) VALUES (?, ?, ?, ?)",
                           (name, quantity, price, category))
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            self.refresh_product_history()
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def delete_product(self):
        product_id = self.delete_product_id_entry.get()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Product deleted successfully!")

    def search_product(self):
        search_name = self.search_entry.get()
        cursor.execute("SELECT * FROM products WHERE name=?", (search_name,))
        result = cursor.fetchone()
        if result:
            result_text = f'ID: {result[0]}, Name: {result[1]}, Quantity: {result[2]}, Price: {result[3]}, Category: {result[4]}'
            self.search_result_label.config(text=result_text)
        else:
            self.search_result_label.config(text="Product not found")

    def record_purchase(self):
        product_id = int(self.product_id_entry.get())
        quantity_purchased = int(self.quantity_purchased_entry.get())
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()
        if product and quantity_purchased <= product[2]:
            new_quantity = product[2] - quantity_purchased
            cursor.execute("UPDATE products SET quantity=? WHERE id=?", (new_quantity, product_id))
            cursor.execute("INSERT INTO sales (product_id, quantity_purchased) VALUES (?, ?)", (product_id, quantity_purchased))
            conn.commit()
            messagebox.showinfo("Success", "Purchase recorded successfully!")
            self.refresh_purchase_history()
        else:
            messagebox.showerror("Error", "Product not available or insufficient quantity")

    def daily_sales_report(self):
        today = datetime.date.today()
        cursor.execute("SELECT product_id, SUM(quantity_purchased) FROM sales WHERE DATE(sale_date) = ? GROUP BY product_id", (today,))
        sales = cursor.fetchall()
        report_text = "Daily Sales Report:\n"
        for sale in sales:
            cursor.execute("SELECT name FROM products WHERE id=?", (sale[0],))
            product_name = cursor.fetchone()[0]
            report_text += f"{product_name}: {sale[1]} units sold\n"
        self.sales_report_label.config(text=report_text)

    def top_selling_products(self):
        cursor.execute("SELECT product_id, SUM(quantity_purchased) AS total_sold FROM sales GROUP BY product_id ORDER BY total_sold DESC LIMIT 5")
        sales = cursor.fetchall()
        report_text = "Top Selling Products:\n"
        for sale in sales:
            cursor.execute("SELECT name FROM products WHERE id=?", (sale[0],))
            product_name = cursor.fetchone()[0]
            report_text += f"{product_name}: {sale[1]} units sold\n"
        self.sales_report_label.config(text=report_text)

    def total_revenue(self):
        cursor.execute("SELECT SUM(quantity_purchased * price) FROM sales JOIN products ON sales.product_id = products.id")
        total_revenue = cursor.fetchone()[0]
        self.sales_report_label.config(text=f"Total Revenue: ${total_revenue:.2f}")

    def export_sales_to_pdf(self):
        today = datetime.date.today()
        cursor.execute("SELECT product_id, SUM(quantity_purchased) FROM sales WHERE DATE(sale_date) = ? GROUP BY product_id", (today,))
        sales = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Daily Sales Report", ln=1, align="C")

        for sale in sales:
            cursor.execute("SELECT name FROM products WHERE id=?", (sale[0],))
            product_name = cursor.fetchone()[0]
            pdf.cell(200, 10, txt=f"{product_name}: {sale[1]} units sold", ln=1, align="L")

        pdf.output("daily_sales_report.pdf")
        messagebox.showinfo("Success", "Sales report exported to PDF")

    def refresh_product_history(self):
        for i in self.product_tree.get_children():
            self.product_tree.delete(i)
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            self.product_tree.insert("", "end", values=row)

    def refresh_purchase_history(self):
        cursor.execute("SELECT * FROM sales ORDER BY sale_date DESC LIMIT 5")
        sales = cursor.fetchall()
        history_text = "Recent Purchases:\n"
        for sale in sales:
            cursor.execute("SELECT name FROM products WHERE id=?", (sale[1],))
            product_name = cursor.fetchone()[0]
            history_text += f"Product: {product_name}, Quantity: {sale[2]}, Date: {sale[3]}\n"
        self.purchase_history_label.config(text=history_text)

    def show_menu(self):
        self.hide_all_frames()
        self.menu_frame.pack()

    def show_add_product_page(self):
        self.hide_all_frames()
        self.refresh_product_history()
        self.add_product_frame.pack()

    def show_delete_product_page(self):
        self.hide_all_frames()
        self.delete_product_frame.pack()

    def show_search_product_page(self):
        self.hide_all_frames()
        self.search_product_frame.pack()

    def show_record_purchase_page(self):
        self.hide_all_frames()
        self.refresh_purchase_history()
        self.record_purchase_frame.pack()

    def show_reporting_page(self):
        self.hide_all_frames()
        self.reporting_frame.pack()

    def back_to_menu(self):
        self.hide_all_frames()
        self.menu_frame.pack()

    def hide_all_frames(self):
        self.login_frame.pack_forget()
        self.menu_frame.pack_forget()
        self.add_product_frame.pack_forget()
        self.delete_product_frame.pack_forget()
        self.search_product_frame.pack_forget()
        self.record_purchase_frame.pack_forget()
        self.reporting_frame.pack_forget()

# Entry point for the application
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
