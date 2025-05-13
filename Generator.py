import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import csv

users = {
    "alice": "password123",
    "bob": "mypassword",
    "jude": "jude123"
}

def open_invoice_window():
    invoice_window = tk.Toplevel()
    invoice_window.title("Invoice Generator")
    invoice_window.geometry("1000x700")
    invoice_window.configure(bg="lightblue")

    header_frame = tk.Frame(invoice_window, bg="lightblue")
    header_frame.grid(row=0, column=0, pady=10, sticky="ew")

    try:
        image = Image.open("InvoRator.png")
        image = image.resize((50, 50))
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(header_frame, image=logo, bg="lightblue")
        logo_label.image = logo
        logo_label.pack(side=tk.LEFT, padx=10)
    except Exception as e:
        print(f"Error loading image: {e}")

    tk.Label(header_frame, text="Welcome to the InvoRator", font=("Garamond", 14, "bold"), bg="lightblue").pack(side=tk.LEFT)

    time_label = tk.Label(header_frame, font=("Garamond", 25, "bold"), bg="lightblue", anchor="e")
    time_label.pack(side=tk.RIGHT, padx=10)

    def update_time():
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_label.config(text=current_time)
        time_label.after(1000, update_time)

    update_time()

    form_frame = tk.Frame(invoice_window, bg="lightblue")
    form_frame.grid(row=1, column=0, pady=5, sticky="nsew")

    tk.Label(form_frame, text="Your Name:", bg="lightblue", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky='w')
    customer_entry = tk.Entry(form_frame, width=40)
    customer_entry.grid(row=0, column=1)

    tk.Label(form_frame, text="Bill To - Name:", bg="lightblue", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky='w')
    client_name_entry = tk.Entry(form_frame, width=40)
    client_name_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="Bill To - Address:", bg="lightblue", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky='w')
    client_address_entry = tk.Entry(form_frame, width=40)
    client_address_entry.grid(row=2, column=1)

    tk.Label(form_frame, text="Bill To - Email:", bg="lightblue", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky='w')
    client_email_entry = tk.Entry(form_frame, width=40)
    client_email_entry.grid(row=3, column=1)

    tk.Label(invoice_window, text="Select Appliance to Add", font=("Helvetica", 12, "bold"), bg="lightblue").grid(row=2, column=0, pady=5)

    display_frame = tk.Frame(invoice_window, bg="lightblue")
    display_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
    invoice_window.grid_rowconfigure(3, weight=1)
    invoice_window.grid_columnconfigure(0, weight=1)

    button_container = tk.Frame(display_frame, bg="lightblue")
    button_container.pack(side=tk.LEFT, fill="both", expand=True)

    canvas_widget = tk.Canvas(button_container, bg="lightblue", height=250)
    scrollbar = tk.Scrollbar(button_container, orient="vertical", command=canvas_widget.yview)
    scrollable_frame = tk.Frame(canvas_widget, bg="lightblue")

    canvas_widget.configure(yscrollcommand=scrollbar.set)
    canvas_widget.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    scrollable_window = canvas_widget.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas_widget.configure(scrollregion=canvas_widget.bbox("all"))

    def on_canvas_configure(event):
        canvas_widget.itemconfig(scrollable_window, width=event.width)

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas_widget.bind("<Configure>", on_canvas_configure)

    def on_mousewheel(event):
        canvas_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas_widget.bind_all("<MouseWheel>", on_mousewheel)

    appliances = [
        ("Refrigerator (LG 6.0 cu.ft)", 13498),
        ("Washing Machine (Samsung 7kg)", 10995),
        ("Electric Fan (Asahi 16\")", 1599),
        ("Air Conditioner (Panasonic 1.0HP)", 18495),
        ("Rice Cooker (Hanabishi 1.0L)", 999),
        ("Microwave Oven (Sharp 20L)", 3999),
        ("Induction Cooker (Imarflex IDX-2000S)", 2195),
        ("Blender (Oster 10-speed)", 2495),
        ("Electric Kettle (Kyowa 1.7L)", 849),
        ("Flat Iron (Philips GC122)", 799),
        ("Television (TCL 32” Android)", 8995),
        ("Water Dispenser (Fujidenzo Table Top)", 3395),
        ("Chest Freezer (Haier 5.3 cu.ft)", 14495),
        ("Vacuum Cleaner (Electrolux Cyclonic)", 5995),
        ("Coffee Maker (Black+Decker 12-cup)", 2499),
        ("Air Fryer (Xiaomi 3.5L)", 3295),
        ("Toaster Oven (Hanabishi 23L)", 2295),
        ("Water Heater (Panasonic)", 6495),
        ("Electric Grill (Dowell Smokeless)", 1799),
        ("Stand Mixer (KitchenAid 4.5qt)", 21999)
    ]

    products = []
    total_var = tk.StringVar(value="₱0.00")

    def refresh_product_listbox():
        product_listbox.delete(0, tk.END)
        for i, (item, qty, price, total) in enumerate(products):
            product_listbox.insert(tk.END, f"{i+1}. {item:<35} Qty:{qty:<4} Price: ₱{price:<7.2f} \nTotal: ₱{total:<7.2f}")
        total_var.set(f"₱{sum(p[3] for p in products):.2f}")

    def add_appliance_to_invoice(name, price):
        for index, (item, qty, existing_price, total) in enumerate(products):
            if item == name:
                new_qty = qty + 1
                new_total = new_qty * price
                products[index] = (name, new_qty, price, new_total)
                break
        else:
            products.append((name, 1, price, price))
        refresh_product_listbox()

    for idx, (name, price) in enumerate(appliances):
        row = idx // 3
        column = idx % 3
        btn = tk.Button(scrollable_frame, text=f"{name}\n₱{price}", width=40, height=3,
                        command=lambda n=name, p=price: add_appliance_to_invoice(n, p), bg="white")
        btn.grid(row=row, column=column, padx=5, pady=5)

    product_listbox = tk.Listbox(display_frame, width=60, height=10, activestyle="none", font=("Helvetica", 10))
    product_listbox.pack(side=tk.RIGHT, fill="y", padx=10)

    def delete_selected():
        selected = product_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to delete.")
            return
        del products[selected[0]]
        refresh_product_listbox()

    def update_selected():
        selected = product_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an item to update.")
            return
        index = selected[0]
        item, qty, price, _ = products[index]
        update_window = tk.Toplevel(invoice_window)
        update_window.title("Update Item")
        update_window.geometry("300x200")

        tk.Label(update_window, text="Item:").pack()
        item_entry = tk.Entry(update_window)
        item_entry.insert(0, item)
        item_entry.pack()

        tk.Label(update_window, text="Quantity:").pack()
        qty_entry = tk.Entry(update_window)
        qty_entry.insert(0, str(qty))
        qty_entry.pack()

        tk.Label(update_window, text="Price:").pack()
        price_entry_update = tk.Entry(update_window)
        price_entry_update.insert(0, str(price))
        price_entry_update.pack()

        def save_update():
            try:
                new_item = item_entry.get().strip()
                new_qty = int(qty_entry.get().strip())
                new_price = float(price_entry_update.get().strip())
                new_total = new_qty * new_price
                products[index] = (new_item, new_qty, new_price, new_total)
                refresh_product_listbox()
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Ensure quantity is integer and price is numeric.")

        tk.Button(update_window, text="Save", command=save_update, bg="lightgreen").pack(pady=10)

    btn_frame = tk.Frame(invoice_window, bg="lightblue")
    btn_frame.grid(row=4, column=0, pady=5)

    tk.Button(btn_frame, text="Update Product", command=update_selected, bg="orange").pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Delete Product", command=delete_selected, bg="tomato").pack(side=tk.LEFT, padx=10)

    total_frame = tk.Frame(invoice_window, bg="lightblue")
    total_frame.grid(row=5, column=0, pady=5)
    tk.Label(total_frame, text="Total: ", bg="lightblue", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
    tk.Label(total_frame, textvariable=total_var, bg="lightblue", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)

    def generate_pdf():
        customer = customer_entry.get().strip()
        client_name = client_name_entry.get().strip()
        client_address = client_address_entry.get().strip()
        client_email = client_email_entry.get().strip()

        if not customer or not client_name or not client_address or not client_email:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        if not products:
            messagebox.showerror("Error", "Please add at least one product.")
            return

        current_datetime = datetime.now().strftime("%m/%d/%y %I:%M %p")
        filename = f"Invoice_{client_name.replace(' ', '_')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 50, "InvoRator")
        c.drawString(50, height - 70, f"Date: {current_datetime}")
        c.setFont("Helvetica-Bold", 12)
        c.line(50, height - 90, 550, height - 90)

        c.setFont("Helvetica", 10)
        y = height - 120
        c.drawString(50, y, f"Customer: {customer}")
        y -= 15
        c.drawString(50, y, f"Bill To: {client_name}")
        y -= 15
        c.drawString(50, y, f"Address: {client_address}")
        y -= 15
        c.drawString(50, y, f"Email: {client_email}")
        y -= 25

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Item Description")
        c.drawString(250, y, "Qty")
        c.drawString(330, y, "Unit Price")
        c.drawString(450, y, "Total")
        y -= 10
        c.line(50, y, 550, y)
        y -= 15

        c.setFont("Helvetica", 10)
        for item, qty, price, total in products:
            c.drawString(50, y, item)
            c.drawString(250, y, str(qty))
            c.drawString(330, y, f"₱{price:.2f}")
            c.drawString(450, y, f"₱{total:.2f}")
            y -= 15

        c.line(50, y, 550, y)
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"TOTAL: {total_var.get()}")

        y -= 30
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "-" * 100)
        y -= 10
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "THANK YOU FOR USING InvoRator")

        c.save()
        messagebox.showinfo("Success", f"Invoice saved as {filename}")

    def generate_csv():
        customer = customer_entry.get().strip()
        client_name = client_name_entry.get().strip()
        client_address = client_address_entry.get().strip()
        client_email = client_email_entry.get().strip()

        if not customer or not client_name or not client_address or not client_email:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        if not products:
            messagebox.showerror("Error", "Please add at least one product.")
            return

        filename = f"Invoice_{client_name.replace(' ', '_')}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Customer", customer])
            writer.writerow(["Client Name", client_name])
            writer.writerow(["Address", client_address])
            writer.writerow(["Email", client_email])
            writer.writerow([])
            writer.writerow(["Item", "Quantity", "Unit Price", "Total"])
            for item, qty, price, total in products:
                writer.writerow([item, qty, price, total])
            writer.writerow([])
            writer.writerow(["Total", "", "", total_var.get()])
        messagebox.showinfo("Success", f"CSV file saved as {filename}")

    tk.Button(invoice_window, text="Generate PDF", command=generate_pdf, bg="green", font=("Helvetica", 12)).grid(row=6, column=0, pady=10)
    tk.Button(invoice_window, text="Generate CSV", command=generate_csv, bg="blue", fg="white", font=("Helvetica", 12)).grid(row=7, column=0, pady=5)

def register_user():
    def save_user():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        users[username] = password
        messagebox.showinfo("Success", f"User '{username}' registered successfully!")
        reg_window.destroy()

    reg_window = tk.Toplevel()
    reg_window.title("Register")
    reg_window.geometry("400x300")
    reg_window.configure(bg="lightblue")

    tk.Label(reg_window, text="Username:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
    reg_username_entry = tk.Entry(reg_window, font=("Helvetica", 12))
    reg_username_entry.pack(pady=5)

    tk.Label(reg_window, text="Password:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
    reg_password_entry = tk.Entry(reg_window, font=("Helvetica", 12), show="*")
    reg_password_entry.pack(pady=5)

    tk.Button(reg_window, text="Register", font=("Helvetica", 12), command=save_user).pack(pady=20)

def show_register_window():
    root.withdraw()
    register_user()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username in users and users[username] == password:
        root.withdraw()
        open_invoice_window()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

root = tk.Tk()
root.title("Login Window")
root.geometry("400x300")
root.configure(bg="lightblue")

tk.Label(root, text="Username:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
username_entry = tk.Entry(root, font=("Helvetica", 12))
username_entry.pack(pady=5)

tk.Label(root, text="Password:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
password_entry = tk.Entry(root, font=("Helvetica", 12), show="*")
password_entry.pack(pady=5)

tk.Button(root, text="Login", font=("Helvetica", 12), command=login).pack(pady=20)
tk.Button(root, text="Register", font=("Helvetica", 12), command=show_register_window).pack(pady=20)

root.mainloop()
