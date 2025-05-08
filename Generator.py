import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Predefined users
users = {
    "alice": "password123",
    "bob": "mypassword"
}

# Function to launch the invoice window
def open_invoice_window():
    invoice_window = tk.Toplevel()
    invoice_window.title("Invoice Generator")
    invoice_window.geometry("720x550")
    invoice_window.configure(bg="lightblue")

    # Header Frame
    header_frame = tk.Frame(invoice_window, bg="lightblue")
    header_frame.pack(pady=10)

    # Load and display logo
    try:
        image = Image.open("InvoRator.png")
        image = image.resize((50, 50))
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(header_frame, image=logo, bg="lightblue")
        logo_label.image = logo
        logo_label.pack(side=tk.LEFT, padx=10)
    except Exception as e:
        print(f"Error loading image: {e}")

    tk.Label(header_frame, text="Welcome to the InvoRator", font=("Garamondq", 14, "bold"), bg="lightblue").pack(side=tk.LEFT)

    # Form fields
    form_frame = tk.Frame(invoice_window, bg="lightblue")
    form_frame.pack(pady=5)

    # Customer (Sender)
    tk.Label(form_frame, text="Your Name:", bg="lightblue").grid(row=0, column=0, sticky='w')
    customer_entry = tk.Entry(form_frame, width=40)
    customer_entry.grid(row=0, column=1)

    # Bill To fields
    tk.Label(form_frame, text="Bill To - Name:", bg="lightblue").grid(row=1, column=0, sticky='w')
    client_name_entry = tk.Entry(form_frame, width=40)
    client_name_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="Bill To - Address:", bg="lightblue").grid(row=2, column=0, sticky='w')
    client_address_entry = tk.Entry(form_frame, width=40)
    client_address_entry.grid(row=2, column=1)

    tk.Label(form_frame, text="Bill To - Email:", bg="lightblue").grid(row=3, column=0, sticky='w')
    client_email_entry = tk.Entry(form_frame, width=40)
    client_email_entry.grid(row=3, column=1)

    # Item and Amount
    tk.Label(form_frame, text="Item Description:", bg="lightblue").grid(row=4, column=0, sticky='w')
    item_entry = tk.Entry(form_frame, width=40)
    item_entry.grid(row=4, column=1)

    tk.Label(form_frame, text="Amount:", bg="lightblue").grid(row=5, column=0, sticky='w')
    amount_entry = tk.Entry(form_frame, width=40)
    amount_entry.grid(row=5, column=1)

    # PDF generation
    def generate_pdf():
        customer = customer_entry.get().strip()
        client_name = client_name_entry.get().strip()
        client_address = client_address_entry.get().strip()
        client_email = client_email_entry.get().strip()
        item = item_entry.get().strip()
        amount = amount_entry.get().strip()

        if not customer or not client_name or not client_address or not client_email or not item or not amount:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        filename = f"Invoice_{client_name.replace(' ', '_')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "INVOICE")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 100, f"From: {customer}")
        c.drawString(50, height - 130, "Bill To:")
        c.drawString(70, height - 150, f"Name: {client_name}")
        c.drawString(70, height - 170, f"Address: {client_address}")
        c.drawString(70, height - 190, f"Email: {client_email}")

        c.drawString(50, height - 230, f"Item Description: {item}")
        c.drawString(50, height - 250, f"Amount: ${amount}")

        c.save()
        messagebox.showinfo("Success", f"Invoice saved as {filename}")

    # Generate button
    tk.Button(invoice_window, text="Generate Invoice", command=generate_pdf, bg="lightgreen").pack(pady=20)

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username in users and users[username] == password:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        root.withdraw()
        open_invoice_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Register function
def register():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    if username in users:
        messagebox.showerror("Error", "Username already exists.")
    else:
        users[username] = password
        messagebox.showinfo("Success", "User registered successfully!")

# Login window
root = tk.Tk()
root.title("User Login")
root.geometry("300x200")
root.configure(bg="lightblue")

tk.Label(root, text="Username:", bg="lightblue", width=20, anchor='w').pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password:", bg="lightblue", width=20, anchor='w').pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login, bg="lightgreen", width=10, height=1).place(x=60, y=110)
tk.Button(root, text="Register", command=register, bg="tomato", width=10, height=1).place(x=155, y=110)

root.mainloop()
