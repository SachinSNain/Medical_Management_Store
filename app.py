import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Window
from billing import create_billing, create_store_billing_table, generate_bill_number
from billinggui import billing_transaction
from inventory import create_inventory, create_store_inventory_table, delete_inventory, read_inventory, update_inventory
from inventorygui import open_stock_management
from reportgui import open_report_section
from login import start_login  # 👈 Login system added

# Step 1: Create required tables
create_store_inventory_table()
create_store_billing_table()

# Step 2: Create main app window using ttkbootstrap
app = Window(themename="flatly")
app.title("MedPay Medical Store App")
app.minsize(500, 400)
app.resizable(True, True)  # Allow window to be resizable

# Step 3: Define function to launch the main dashboard after login
def launch_dashboard(role):
    for widget in app.winfo_children():
        widget.destroy()  # Clear existing widgets

    # Welcome Labels
    welcome_label = ttk.Label(app, text=f"Welcome {role.title()} to the MedPay Medical Store", font=("Arial", 18))
    welcome_label.pack(pady=10)

    subtext = "You have full access to the system" if role == "admin" else "You have limited access as a customer"
    welcome_label2 = ttk.Label(app, text=subtext, font=("Arial", 13), foreground="gray")
    welcome_label2.pack(pady=5)

    # Create menu bar
    menu_bar = tk.Menu(app)
    menu_main = tk.Menu(menu_bar, tearoff=0)

    # Add available menu options
    menu_main.add_command(label="Billing", command=lambda: billing_transaction(app))
    if role == "admin":
        menu_main.add_command(label="Stock Management", command=lambda: open_stock_management(app))
        menu_main.add_command(label="Report Section", command=lambda: open_report_section(app))

    menu_bar.add_cascade(label="Menu", menu=menu_main)
    app.config(menu=menu_bar)

# Step 4: Start login interface (Admin or Customer)
start_login(app, launch_dashboard)

# Step 5: Run the app
app.mainloop()
