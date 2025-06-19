import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from inventory import create_inventory, delete_inventory, read_inventory, update_inventory

def open_stock_management(parent_window):
    stock_window = ttk.Toplevel(parent_window)
    stock_window.title("MedPay Medical Store App")
    stock_window.minsize(1330, 300)

    welcome_label = ttk.Label(stock_window, text="Manage Stock - MedPay Medical Store", font=("Arial", 18))
    welcome_label.pack(pady=10)

    def add_medicine():
        medicine_code = medicine_code_entry.get()
        product_name = medicine_name_entry.get()
        quantity = quantity_entry.get()
        med_category_value = med_category_entry.get()
        expiry_date = expiry_date_entry.get()
        price_value = price_entry.get()
        manufacture_date_value = manufacture_date_entry.get()
        prescription_required = rack_number_entry.get()

        create_inventory((
            medicine_code, product_name, med_category_value, quantity, price_value,
            int(quantity) * float(price_value), manufacture_date_value,
            expiry_date, prescription_required
        ))
        update_inventory_table()
        clear_input_fields()

    def update_inventory_table():
        results = read_inventory()
        for row in inventory_table.get_children():
            inventory_table.delete(row)
        for result in results:
            inventory_table.insert("", "end", values=result[0:] + (f"Edit {result[0]}", f"Delete {result[0]}"))

    def edit_inventory_item():
        selected_item = inventory_table.selection()[0]
        selected_item_values = inventory_table.item(selected_item, "values")
        dialog = ttk.Toplevel(stock_window)
        dialog.title(f"EDIT {selected_item_values[2]}")

        entries = {}
        labels = ["Medicine Code", "Medicine Name", "Medicine Category", "Quantity",
                  "Price", "Expiry Date", "Manufacture Date", "Rack Number"]
        defaults = [selected_item_values[1], selected_item_values[2], selected_item_values[3],
                    selected_item_values[4], selected_item_values[5], selected_item_values[8],
                    selected_item_values[7], selected_item_values[9]]

        for i, (label_text, default_val) in enumerate(zip(labels, defaults)):
            label = ttk.Label(dialog, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5)
            if label_text == "Medicine Category":
                entry = ttk.Combobox(dialog, values=('tablet', 'Syrup', 'bandage', 'ointment', 'misc'))
                entry.set(default_val)
            else:
                entry = ttk.Entry(dialog)
                entry.insert(0, default_val)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label_text] = entry

        def save_changes():
            update_inventory(selected_item_values[0], (
                entries["Medicine Code"].get(),
                entries["Medicine Name"].get(),
                entries["Medicine Category"].get(),
                entries["Quantity"].get(),
                entries["Price"].get(),
                int(entries["Quantity"].get()) * float(entries["Price"].get()),
                entries["Manufacture Date"].get(),
                entries["Expiry Date"].get(),
                entries["Rack Number"].get(),
                "SYSTEMUSER"
            ))
            dialog.destroy()
            update_inventory_table()

        save_btn = ttk.Button(dialog, text="Save Changes", bootstyle=SUCCESS, command=save_changes)
        save_btn.grid(row=len(labels), columnspan=2, pady=10)

    def delete_inventory_item(id):
        delete_inventory(id)
        update_inventory_table()

    def clear_input_fields():
        for entry in [medicine_code_entry, medicine_name_entry, quantity_entry,
                      price_entry, manufacture_date_entry, expiry_date_entry, rack_number_entry]:
            entry.delete(0, "end")
        med_category_entry.set('')

    def on_inventory_item_click(event):
        try:
            item = inventory_table.selection()[0]
            column = inventory_table.identify_column(event.x)
            if column == "#11":
                edit_inventory_item()
            elif column == "#12":
                delete_inventory_item(int(inventory_table.item(item, "values")[0]))
        except IndexError:
            pass

    add_medicine_frame = ttk.LabelFrame(stock_window, text="Add Medicines")
    add_medicine_frame.pack(padx=10, pady=10, fill="x")

    # Input fields
    medicine_code_entry = ttk.Entry(add_medicine_frame)
    medicine_name_entry = ttk.Entry(add_medicine_frame)
    med_category_entry = ttk.Combobox(add_medicine_frame, values=('tablet', 'Syrup', 'bandage', 'ointment', 'misc'))
    quantity_entry = ttk.Entry(add_medicine_frame)
    price_entry = ttk.Entry(add_medicine_frame)
    manufacture_date_entry = ttk.Entry(add_medicine_frame)
    expiry_date_entry = ttk.Entry(add_medicine_frame)
    rack_number_entry = ttk.Entry(add_medicine_frame)

    labels = ["Medicine Code", "Medicine Name", "Medicine Category", "Quantity", "Price",
              "Manufacture Date (YYYY-MM-DD)", "Expiry Date (YYYY-MM-DD)", "Rack Number"]
    entries = [medicine_code_entry, medicine_name_entry, med_category_entry,
               quantity_entry, price_entry, manufacture_date_entry,
               expiry_date_entry, rack_number_entry]

    for i, (label_text, entry) in enumerate(zip(labels, entries)):
        label = ttk.Label(add_medicine_frame, text=label_text)
        label.grid(row=i//4, column=(i%4)*2, padx=5, pady=5, sticky='w')
        entry.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5)

    create_button = ttk.Button(add_medicine_frame, text="Add Inventory Item",
                               bootstyle=SUCCESS, width=30, command=add_medicine)
    create_button.grid(row=2, column=6, columnspan=2, padx=5, pady=5)

    inventory_table = ttk.Treeview(stock_window, columns=(
        "id", "Medicine Code", "Medicine Name", "Medicine Category", "Quantity",
        "Price", "Amount", "Manufacture Date", "Expiry Date", "Rack Number", "Edit", "Delete"
    ), show="headings")

    headings = ["Id", "Medicine Code", "Medicine Name", "Medicine Category", "Quantity",
                "Price", "Amount", "Manufacture Date", "Expiry Date", "Rack Number", "Edit", "Delete"]

    for i, heading in enumerate(headings, 1):
        inventory_table.heading(f"#{i}", text=heading)
        inventory_table.column(f"#{i}", anchor="center")

    inventory_table.pack(fill="both", expand=True, padx=10, pady=10)
    inventory_table.bind("<Button-1>", on_inventory_item_click)

    update_inventory_table()
    stock_window.mainloop()
