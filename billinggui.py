import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Toplevel
from tkinter import messagebox
import mysql.connector
from db import with_cursor

rows = []
medicine_list = []

def billing_transaction(app):
    medicine_data = []

    def add_medicine():
        price = 0
        patient_name = patient_name_entry.get()
        patient_mobile = patient_mobile_entry.get()
        doctor_name = doctor_name_entry.get()
        mode_of_pay = mode_of_pay_entry.get()
        med_name = name_combobox.get()
        quantity = quantity_entry.get()

        for row in rows:
            if row[2] == med_name:
                price = float(row[5])
                if int(quantity) > row[4]:
                    messagebox.showerror("Error", f"Qty exceeds stock: {row[4]}")
                    return
                break

        discount = discount_entry.get()
        try:
            amount = float(quantity) * float(price)
            amount -= (float(discount) / 100 * amount)
        except:
            amount = 0

        if all([patient_name, doctor_name, med_name, discount, quantity]):
            medicine_data.append((patient_name, patient_mobile, doctor_name, mode_of_pay, med_name, quantity, price, discount, amount))
            medicine_list.insert("", "end", values=(med_name, quantity, price, discount, amount))
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def reset_fields():
        global medicine_data
        patient_name_entry.delete(0, "end")
        patient_mobile_entry.delete(0, "end")
        doctor_name_entry.delete(0, "end")
        mode_of_pay_entry.delete(0, "end")
        name_combobox.set("")
        quantity_entry.delete(0, "end")
        discount_entry.delete(0, "end")
        medicine_data = []
        for item in medicine_list.get_children():
            medicine_list.delete(item)

    @with_cursor
    def save_data(conn, cursor):
        if not patient_name_entry.get():
            messagebox.showerror("Error", "No data to save")
            return
        try:
            for data in medicine_data:
                cursor.execute("INSERT INTO billing_tran (PatientName, MobileNum, PrescribedByDr, ModeOfPayment, MedicineName, Qty, Price, Discount, Amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
                cursor.execute("UPDATE medicine_m SET qty = qty - %s WHERE medicineName = %s", (data[5], data[4]))
            conn.commit()
            messagebox.showinfo("Success", "Data saved successfully!")
            reset_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))

    @with_cursor
    def fetch_medicine_names(conn, cur):
        global rows
        try:
            cur.execute("SELECT * FROM medicine_m")
            rows = cur.fetchall()
            for row in rows:
                medicine_name_values.append(row[2])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", str(err))

    biil_screen = Toplevel(app)
    biil_screen.title("MedPay Medical Store App")
    biil_screen.geometry("1050x530")

    ttk.Label(biil_screen, text="Add Sales", font=("Segoe UI", 20, "bold")).pack(pady=10)

    section1 = ttk.LabelFrame(biil_screen, text="Patient Details", padding=10)
    section1.pack(fill="x", padx=10, pady=5)

    patient_name_entry = ttk.Entry(section1)
    patient_mobile_entry = ttk.Entry(section1)
    doctor_name_entry = ttk.Entry(section1)
    mode_of_pay_entry = ttk.Entry(section1)

    ttk.Label(section1, text="Patient Name:").grid(row=0, column=0, padx=5, pady=5)
    patient_name_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(section1, text="Mobile No:").grid(row=0, column=2, padx=5, pady=5)
    patient_mobile_entry.grid(row=0, column=3, padx=5, pady=5)
    ttk.Label(section1, text="Doctor Name:").grid(row=1, column=0, padx=5, pady=5)
    doctor_name_entry.grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(section1, text="Payment Mode:").grid(row=1, column=2, padx=5, pady=5)
    mode_of_pay_entry.grid(row=1, column=3, padx=5, pady=5)

    section2 = ttk.LabelFrame(biil_screen, text="Medicine Details", padding=10)
    section2.pack(fill="both", expand=True, padx=10, pady=5)

    medicine_name_values = []
    fetch_medicine_names()

    name_combobox = ttk.Combobox(section2, values=medicine_name_values)
    name_combobox.set("Select Medicine")
    quantity_entry = ttk.Entry(section2)
    discount_entry = ttk.Entry(section2)

    ttk.Label(section2, text="Medicine Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    name_combobox.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(section2, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    quantity_entry.grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(section2, text="Discount (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    discount_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(section2, text="Add Medicine", bootstyle="primary", command=add_medicine).grid(row=3, column=0, columnspan=2, pady=10)

    columns = ("Medicine Name", "Quantity", "Price", "Discount", "Amount")
    medicine_list = ttk.Treeview(section2, columns=columns, show="headings")
    for col in columns:
        medicine_list.heading(col, text=col)
        medicine_list.column(col, anchor="center")
    medicine_list.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    control_frame = ttk.Frame(biil_screen)
    control_frame.pack(fill="x", pady=10, padx=10)
    ttk.Button(control_frame, text="Save", bootstyle="success", command=save_data).pack(side="right", padx=5)
    ttk.Button(control_frame, text="Close", bootstyle="warning", command=biil_screen.destroy).pack(side="right", padx=5)

    biil_screen.mainloop()
