import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Window, Style
import mysql.connector

# Database connection setup
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # use your MySQL password
        database="users"
    )

# Admin Login Verification
def verify_admin(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# Customer Login Verification (optional)
def verify_customer(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# Admin Login Window
def open_admin_login(app, on_success):
    login_win = tk.Toplevel(app)
    login_win.title("Admin Login")

    tk.Label(login_win, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.grid(row=0, column=1)

    tk.Label(login_win, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.grid(row=1, column=1)

    def attempt_login():
        if verify_admin(username_entry.get(), password_entry.get()):
            messagebox.showinfo("Login", "Admin login successful")
            login_win.destroy()
            on_success("admin")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login_win, text="Login", command=attempt_login).grid(row=2, columnspan=2, pady=10)

# Customer Access (skip login)
def proceed_as_customer(app, on_success):
    messagebox.showinfo("Welcome", "Proceeding as Customer")
    on_success("customer")

# Initial Role Selection Window
def start_login(app, on_success):
    selection_window = tk.Toplevel(app)
    selection_window.title("Welcome to MedPay")

    tk.Label(selection_window, text="Choose Role:", font=("Arial", 14)).pack(pady=10)

    tk.Button(selection_window, text="Login as Admin", width=30,
              command=lambda: [selection_window.destroy(), open_admin_login(app, on_success)]).pack(pady=5)

    tk.Button(selection_window, text="Continue as Customer", width=30,
              command=lambda: [selection_window.destroy(), proceed_as_customer(app, on_success)]).pack(pady=5)
