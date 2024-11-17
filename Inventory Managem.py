# This code is for the Inventory Management System
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Inventory Management System")

# Create the login frame
login_frame = tk.Frame(root)
login_frame.pack()

# Create the username and password labels and entry fields
username_label = tk.Label(login_frame, text="Username")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Password")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

# Create the login button
login_button = tk.Button(login_frame, text="Login", command=lambda: login())
login_button.grid(row=2, column=0, columnspan=2)

# Create the inventory frame
inventory_frame = tk.Frame(root)
inventory_frame.pack()

# Create the add product frame
add_product_frame = tk.Frame(inventory_frame)
add_product_frame.pack()

# Create the add product labels and entry fields
name_label = tk.Label(add_product_frame, text="Name")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(add_product_frame)
name_entry.grid(row=0, column=1)

quantity_label = tk.Label(add_product_frame, text="Quantity")
quantity_label.grid(row=1, column=0)
quantity_entry = tk.Entry(add_product_frame)
quantity_entry.grid(row=1, column=1)

price_label = tk.Label(add_product_frame, text="Price")
price_label.grid(row=2, column=0)
price_entry = tk.Entry(add_product_frame)
price_entry.grid(row=2, column=1)

category_label = tk.Label(add_product_frame, text="Category")
category_label.grid(row=3, column=0)
category_entry = tk.Entry(add_product_frame)
category_entry.grid(row=3, column=1)

# Create the add product button
add_product_button = tk.Button(add_product_frame, text="Add Product", command=lambda: add_product())
add_product_button.grid(row=4, column=0, columnspan=2)

# Create the delete product frame
delete_product_frame = tk.Frame(inventory_frame)
delete_product_frame.pack()

# Create the delete product label and entry field
product_id_label = tk.Label(delete_product_frame, text="Product ID to delete")
product_id_label.grid(row=0, column=0)
product_id_entry = tk.Entry(delete_product_frame)
product_id_entry.grid(row=0, column=1)

# Create the delete product button
delete_product_button = tk.Button(delete_product_frame, text="Delete Product", command=lambda: delete_product())
delete_product_button.grid(row=1, column=0, columnspan=2)

# Create the search product frame
search_product_frame = tk.Frame(inventory_frame)
search_product_frame.pack()

# Create the search product label and entry field
product_name_label = tk.Label(search_product_frame, text="Product Name")
product_name_label.grid(row=0, column=0)
product_name_entry = tk.Entry(search_product_frame)
product_name_entry.grid(row=0, column=1)

# Create the search product button
search_product_button = tk.Button(search_product_frame, text="Search", command=lambda: search_product())
search_product_button.grid(row=1, column=0, columnspan=2)

# Create the sales and reporting frame
sales_and_reporting_frame = tk.Frame(root)
sales_and_reporting_frame.pack()

# Create the daily sales report button
daily_sales_report_button = tk.Button(sales_and_reporting_frame, text="Daily Sales Report", command=lambda: daily_sales_report())
daily_sales_report_button.grid(row=0, column=0, columnspan=2)

# Create the top selling products button
top_selling_products_button = tk.Button(sales_and_reporting_frame, text="Top Selling Products", command=lambda: top_selling_products())
top_selling_products_button.grid(row=1, column=0, columnspan=2)

# Create the revenue analysis button
revenue_analysis_button = tk.Button(sales_and_reporting_frame, text="Revenue Analysis", command=lambda: revenue_analysis())
revenue_analysis_button.grid(row=2, column=0, columnspan=2)

# Create the purchase frame
purchase_frame = tk.Frame(root)
purchase_frame.pack()

# Create the purchase labels and entry fields
product_id_label = tk.Label(purchase_frame, text="Product ID")
product_id_label.grid(row=0, column=0)
product_id_entry = tk.Entry(purchase_frame)
product_id_entry.grid(row=0, column=1)

quantity_purchased_label = tk.Label(purchase_frame, text="Quantity Purchased")
quantity_purchased_label.grid(row=1, column=0)
quantity_purchased_entry = tk.Entry(purchase_frame)
quantity_purchased_entry.grid(row=1, column=1)

# Create the record purchase button
record_purchase_button = tk.Button(purchase_frame, text="Record Purchase", command=lambda: record_purchase())
record_purchase_button.grid(row=2, column=0, columnspan=2)

# Create the product list
product_list = []

# Create the login function
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "username" and password == "password":
        login_frame.pack_forget()
        inventory_frame.pack()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Create the add product function
def add_product():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    category = category_entry.get()
    if name == "" or quantity == "" or price == "" or category == "":
        messagebox.showerror("Error", "Please fill in all fields")
    else:
        product_list.append({"id": len(product_list) + 1, "name": name, "quantity": quantity, "price": price, "category": category})
        messagebox.showinfo("Success", "Product added successfully")
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)

# Create the delete product function
def delete_product():
    product_id = product_id_entry.get()
    if product_id == "":
        messagebox.showerror("Error", "Please enter a product ID")
    else:
        try:
            product_id = int(product_id)
            if product_id <= len(product_list) and product_id > 0:
                product_list.pop(product_id - 1)
                messagebox.showinfo("Success", "Product deleted successfully")
            else:
                messagebox.showerror("Error", "Invalid product ID")
        except ValueError:
            messagebox.showerror("Error", "Invalid product ID")
        product_id_entry.delete(0, tk.END)

# Create the search product function
def search_product():
    product_name = product_name_entry.get()
    if product_name == "":
        messagebox.showerror("Error", "Please enter a product name")
    else:
        found = False
        for product in product_list:
            if product["name"] == product_name:
                found = True
                messagebox.showinfo("Search Results", f"ID: {product['id']}\nName: {product['name']}\nQuantity: {product['quantity']}\nPrice: {product['price']}\nCategory: {product['category']}")
                break
        if not found:
            messagebox.showerror("Error", "Product not found")
        product_name_entry.delete(0, tk.END)

# Create the daily sales report function
def daily_sales_report():
    # Display the daily sales report
    print("Daily Sales Report")

# Create the top selling products function
def top_selling_products():
    # Display the top selling products
    print("Top Selling Products")

# Create the revenue analysis function
def revenue_analysis():
    # Display the revenue analysis
    print("Revenue Analysis")

# Create the record purchase function
def record_purchase():
    product_id = product_id_entry.get()
    quantity_purchased = quantity_purchased_entry.get()
    if product_id == "" or quantity_purchased == "":
        messagebox.showerror("Error", "Please fill in all fields")
    else:
        try:
            product_id = int(product_id)
            quantity_purchased = int(quantity_purchased)
            if product_id <= len(product_list) and product_id > 0:
                product_list[product_id - 1]["quantity"] = str(int(product_list[product_id - 1]["quantity"]) - quantity_purchased)
                messagebox.showinfo("Success", "Purchase recorded successfully")
            else:
                messagebox.showerror("Error", "Invalid product ID")
        except ValueError:
            messagebox.showerror("Error", "Invalid product ID or quantity")
        product_id_entry.delete(0, tk.END)
        quantity_purchased_entry.delete(0, tk.END)

# Run the main loop
root.mainloop()