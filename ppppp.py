from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("CORE ATHLETICS")
root.geometry('800x650')
root.resizable(0, 0)
root.configure(bg="#333333")  # background color

# Sample equipment data (can be replaced with your actual equipment data)
equipment_data = [
    {"name": "Dumbbells", "price": 25.99},
    {"name": "Yoga Mat", "price": 19.99},
    {"name": "Resistance Bands", "price": 12.99},
    {"name": "Jump Rope", "price": 9.99},
    {"name": "Foam Roller", "price": 14.99}
]

# Cart to store selected items
cart = []

def initialize_database():
    connection = sqlite3.connect("core_athletics.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

initialize_database()

def create_login_page():
    header_label = Label(root, text="CORE ATHLETICS", font=("Arial", 36, "bold"), fg="#FFFFFF", bg="#333333")
    header_label.pack(side=TOP, pady=20)

    image = Image.open("o.jpg") 
    image = image.resize((400, 500))
    filename = ImageTk.PhotoImage(image)

    bg_label = Label(root, image=filename)
    bg_label.image = filename  
    bg_label.pack(expand=1, side=LEFT)

    login_frame = Frame(root, bg="#333333")
    login_frame.pack(pady=80)

    username_label = Label(login_frame, text="Username:", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#333333")
    username_label.grid(row=0, column=0, sticky=W, padx=20, pady=5)
    username_entry = Entry(login_frame, font=("Arial", 12), bg="#FFFFFF", fg="#333333")
    username_entry.grid(row=1, column=0, padx=20)

    password_label = Label(login_frame, text="Password:", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#333333")
    password_label.grid(row=2, column=0, sticky=W, padx=20, pady=5)
    password_entry = Entry(login_frame, show="*", font=("Arial", 12), bg="#FFFFFF", fg="#333333")
    password_entry.grid(row=3, column=0, padx=20)

    login_button = Button(login_frame, text="Login", command=lambda: login(username_entry, password_entry),
                          font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#FF0000", padx=10, pady=5, relief=FLAT)
    login_button.grid(row=4, column=0, pady=10)

    additional_text = Label(login_frame, text="Don't have an account?", font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    additional_text.grid(row=6, column=0, pady=5)

    register_button = Button(login_frame, text="Register Now", command=create_registration_page,
                             font=("Arial", 12, "bold"), fg="#FF0000", bg="#FFFFFF", padx=10, pady=5, bd=0)
    register_button.grid(row=7, column=0)

    equipment_button = Button(login_frame, text="Equipment", command=create_equipment_page,
                              font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#FF0000", padx=10, pady=5, relief=FLAT)
    equipment_button.grid(row=8, column=0, pady=10)

def create_registration_page():
    registration_window = Toplevel(root)
    registration_window.title("CORE ATHLETICS - Registration")
    registration_window.geometry('800x650')
    registration_window.resizable(0, 0)
    registration_window.configure(bg="#333333")

    header_label = Label(registration_window, text="REGISTRATION", font=("Arial", 36, "bold"), fg="#FFFFFF", bg="#333333")
    header_label.pack(side=TOP, pady=20)

    registration_frame = Frame(registration_window, bg="#333333")
    registration_frame.pack(pady=80)

    fullname_label = Label(registration_frame, text="Full Name:", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#333333")
    fullname_label.grid(row=0, column=0, sticky=W, padx=20, pady=5)
    fullname_entry = Entry(registration_frame, font=("Arial", 12), bg="#FFFFFF", fg="#333333")
    fullname_entry.grid(row=1, column=0, padx=20)

    email_label = Label(registration_frame, text="Email:", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#333333")
    email_label.grid(row=2, column=0, sticky=W, padx=20, pady=5)
    email_entry = Entry(registration_frame, font=("Arial", 12), bg="#FFFFFF", fg="#333333")
    email_entry.grid(row=3, column=0, padx=20)

    password_label = Label(registration_frame, text="Password:", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#333333")
    password_label.grid(row=4, column=0, sticky=W, padx=20, pady=5)
    password_entry = Entry(registration_frame, show="*", font=("Arial", 12), bg="#FFFFFF", fg="#333333")
    password_entry.grid(row=5, column=0, padx=20)

    register_button = Button(registration_frame, text="Register", command=lambda: register(fullname_entry, email_entry, password_entry),
                             font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#FF0000", padx=10, pady=5, relief=FLAT)
    register_button.grid(row=6, column=0, pady=10)

    return_label = Label(registration_frame, text="Already have an account?",
                         font=("Arial", 12), fg="#FFFFFF", bg="#333333")
    return_label.grid(row=8, column=0, pady=5)

    return_button = Button(registration_frame, text="Return to Login", command=registration_window.destroy,
                           font=("Arial", 12, "bold"), fg="#FF0000", bg="#FFFFFF", padx=10, pady=5, bd=0)
    return_button.grid(row=9, column=0)

def login(username_entry, password_entry):
    global logged_in
    username = username_entry.get()
    password = password_entry.get()

    try:
        connection = sqlite3.connect("core_athletics.db")
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()

        connection.close()

        if user_data:
            messagebox.showinfo("Login", "Login successful!")
            logged_in = True
            root.withdraw()
            create_equipment_page()
        else:
            messagebox.showerror("Login", "Invalid username or password.")
    except sqlite3.Error:
        messagebox.showerror("Error", "An error occurred while logging in.")


def register(fullname_entry, email_entry, password_entry):
    fullname = fullname_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if fullname and email and password:
        try:
            connection = sqlite3.connect("core_athletics.db")
            cursor = connection.cursor()

            cursor.execute('INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)', (fullname, email, password))
            
            connection.commit()
            connection.close()

            messagebox.showinfo("Registration", "Registration successful!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration", "Email address already registered.")
    else:
        messagebox.showerror("Registration", "Please fill in all the fields.")


def create_equipment_page():
    if not logged_in:  # Check if the user is logged in
        messagebox.showerror("Unauthorized", "Please log in first.")
        return

    equipment_window = Toplevel(root)
    equipment_window.title("CORE ATHLETICS - Equipment")
    equipment_window.geometry('800x650')
    equipment_window.resizable(0, 0)
    equipment_window.configure(bg="#333333")

    header_label = Label(equipment_window, text="EQUIPMENT", font=("Arial", 36, "bold"), fg="#FFFFFF", bg="#333333")
    header_label.pack(side=TOP, pady=20)

    equipment_frame = Frame(equipment_window, bg="#333333")
    equipment_frame.pack(pady=80)

    for index, item in enumerate(equipment_data):
        item_label = Label(equipment_frame, text=f"{item['name']} - ${item['price']:.2f}", font=("Arial", 14), fg="#FFFFFF", bg="#333333")
        item_label.grid(row=index, column=0, sticky=W, padx=20, pady=5)

        add_to_cart_button = Button(equipment_frame, text="Add to Cart", command=lambda idx=index: add_to_cart(idx),
                                    font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#FF0000", padx=10, pady=5, relief=FLAT)
        add_to_cart_button.grid(row=index, column=1, padx=20)

    cart_button = Button(equipment_frame, text="View Cart", command=view_cart,
                         font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#FF0000", padx=10, pady=5, relief=FLAT)
    cart_button.grid(row=len(equipment_data), column=0, columnspan=2, pady=10)

def add_to_cart(index):
    item = equipment_data[index]
    cart.append(item['name'])
    messagebox.showinfo("Added to Cart", f"{item['name']} added to cart!")

def view_cart():
    cart_window = Toplevel(root)
    cart_window.title("CORE ATHLETICS - Cart")
    cart_window.geometry('400x400')
    cart_window.resizable(0, 0)
    cart_window.configure(bg="#333333")

    header_label = Label(cart_window, text="YOUR CART", font=("Arial", 20, "bold"), fg="#FFFFFF", bg="#333333")
    header_label.pack(side=TOP, pady=20)

    cart_frame = Frame(cart_window, bg="#333333")
    cart_frame.pack(pady=20)

    total_price = 0  # To calculate the total value of items in the cart

    for index, item in enumerate(cart):
        cart_item_label = Label(cart_frame, text=f"{item} - ${equipment_data[index]['price']:.2f}", font=("Arial", 14), fg="#FFFFFF", bg="#333333")
        cart_item_label.grid(row=index, column=0, sticky=W, padx=20, pady=5)

        # Calculate the total price
        total_price += equipment_data[index]['price']

    # Display the total price
    total_label = Label(cart_frame, text=f"Total: ${total_price:.2f}", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#333333")
    total_label.grid(row=len(cart), column=0, sticky=W, padx=20, pady=10)

    # Checkout button
    checkout_button = Button(cart_frame, text="Checkout", command=lambda: checkout(total_price),
                             font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#FF0000", padx=10, pady=5, relief=FLAT)
    checkout_button.grid(row=len(cart) + 1, column=0, columnspan=2, pady=10)

def checkout(total_price):
    # Display a message box with the total value of the items
    messagebox.showinfo("Checkout", f"Total Price: ${total_price:.2f}")

create_login_page()
root.mainloop()
