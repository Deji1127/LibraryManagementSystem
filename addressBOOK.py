import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


def fetch_books_from_database():
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Title FROM BOOK;')
    books = cursor.fetchall()
    connection.close()
    book_titles = [book[0] for book in books]
    return book_titles


def fetch_branch_ids_from_database():
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Branch_Id FROM LIBRARY_BRANCH;')
    branches = cursor.fetchall()
    connection.close()
    branch_ids = [branch[0] for branch in branches]
    return branch_ids


def fetch_copies_loaned(book_id, branch_id):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT No_Of_Copies 
        FROM BOOK_COPIES 
        WHERE Book_Id = ? AND Branch_Id = ? AND Returned_Date IS NULL
    ''', (book_id, branch_id))

    result = cursor.fetchone()
    count = result[0] if result is not None else 0

    connection.close()
    return count


def on_submit_clicked():
    book_title = book_var.get()
    branch_id = int(branch_var.get())

    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    # Get Book_Id based on the selected title
    cursor.execute('SELECT Book_Id FROM BOOK WHERE Title = ?', (book_title,))
    result = cursor.fetchone()

    if result:
        book_id = result[0]
        # Calculate the number of copies loaned out for the selected book and branch
        copies_loaned = fetch_copies_loaned(book_id, branch_id)
        # Display the result
        on_checkout_clicked.result_label.config(
            text=f'Number of Copies Loaned: {copies_loaned}')
    else:
        on_checkout_clicked.result_label.config(text="Book not found.")

    connection.close()


def on_checkout_clicked():
    # Destroy existing combobox and labels
    destroy_combobox_and_label()

    # Initialize result_label
    on_checkout_clicked.result_label = tk.Label(master, text="")

    if v.get() in "4":
        # Create a centered label and Combobox for selecting a book
        frame = tk.Frame(master)
        frame.pack(padx=10, pady=5, anchor="center")

        ttk.Label(frame, text="Select a Book:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        book_names = fetch_books_from_database()
        global book_var
        book_var = tk.StringVar()
        book_choosen = ttk.Combobox(frame, width=27, textvariable=book_var)
        book_choosen['values'] = tuple(book_names)
        book_choosen.pack(side="left", padx=(0, 5))
        book_choosen.current()

        on_checkout_clicked.book_choosen = book_choosen
        on_checkout_clicked.label = frame

        branch_frame = tk.Frame(master)
        branch_frame.pack(padx=10, pady=5, anchor="center")

        ttk.Label(branch_frame, text="Select Branch ID:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        branch_ids = fetch_branch_ids_from_database()
        global branch_var
        branch_var = tk.StringVar()
        branch_choosen = ttk.Combobox(
            branch_frame, width=27, textvariable=branch_var)
        branch_choosen['values'] = tuple(branch_ids)
        branch_choosen.pack(side="left", padx=(0, 5))
        branch_choosen.current()

        on_checkout_clicked.branch_choosen = branch_choosen
        on_checkout_clicked.branch_label = branch_frame

        # Add a Submit button
        on_checkout_clicked.submit_button = tk.Button(
            master, text="Submit", command=on_submit_clicked)
        on_checkout_clicked.submit_button.pack(pady=10)

        # Add a label to display the result
        on_checkout_clicked.result_label.pack()

    elif v.get() in "1":
        frame = tk.Frame(master)
        frame.pack(padx=10, pady=5, anchor="center")

        # start of book select label
        ttk.Label(frame, text="Select a Book:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        book_names = fetch_books_from_database()
        # book_var
        book_var = tk.StringVar()
        book_choosen = ttk.Combobox(frame, width=27, textvariable=book_var)
        book_choosen['values'] = tuple(book_names)
        book_choosen.pack(side="left", padx=(0, 5))
        book_choosen.current()

        on_checkout_clicked.book_choosen = book_choosen
        on_checkout_clicked.label = frame

        branch_frame = tk.Frame(master)
        branch_frame.pack(padx=10, pady=5, anchor="center")

        # start of branch select label
        ttk.Label(branch_frame, text="Select Branch ID:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        branch_ids = fetch_branch_ids_from_database()
        # global branch_var
        branch_var = tk.StringVar()
        branch_choosen = ttk.Combobox(
            branch_frame, width=27, textvariable=branch_var)
        branch_choosen['values'] = tuple(branch_ids)
        branch_choosen.pack(side="left", padx=(0, 5))
        branch_choosen.current()
        on_checkout_clicked.branch_choosen = branch_choosen
        on_checkout_clicked.branch_label = branch_frame

        # start of card_no label
        card_frame = tk.Frame(master)
        card_frame.pack(padx=10, pady=5, anchor="center")

        ttk.Label(card_frame, text="Enter your Card Number:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        # Text entry for card number
        global card_var
        card_var = tk.StringVar()
        card_entry = tk.Entry(card_frame, textvariable=card_var, width=27)
        card_entry.pack(side="left", padx=(0, 5))

        on_checkout_clicked.card_entry = card_entry
        on_checkout_clicked.card_label = card_frame

        # Add a Submit button
        on_checkout_clicked.submit_button = tk.Button(
            master, text="Submit", command=on_submit_clicked)
        on_checkout_clicked.submit_button.pack(pady=10)

        # Add a label to display the result
        on_checkout_clicked.result_label.pack()
    elif v.get() == "2":
        if hasattr(on_checkout_clicked, 'frame') and on_checkout_clicked.frame.winfo_exists():
            # Destroy existing frame content
            on_checkout_clicked.frame.destroy()

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=5, anchor="center")

        name = tk.Entry(frame, width=27, name='name')
        name.grid(row=0, column=1)

        address = tk.Entry(frame, width=27, name='address')
        address.grid(row=1, column=1)

        phone = tk.Entry(frame, width=27, name='phone')
        phone.grid(row=2, column=1)

        name_label = tk.Label(frame, text='Enter Name: ')
        name_label.grid(row=0, column=0)

        address_label = tk.Label(frame, text='Enter Address: ')
        address_label.grid(row=1, column=0)

        phoneNo_label = tk.Label(
            frame, text='Enter Phone (format: 000-000-0000): ')
        phoneNo_label.grid(row=2, column=0)

        submit_btn = tk.Button(frame, text='Submit',
                               command=lambda: submit_ab(name, address, phone, frame))
        submit_btn.grid(row=10, column=0, columnspan=2,
                        pady=10, padx=10, ipadx=140)

        # Store components for later destruction
        on_checkout_clicked.name_entry = name
        on_checkout_clicked.address_entry = address
        on_checkout_clicked.phone_entry = phone
        on_checkout_clicked.frame = frame

    else:
        # Handle other cases or cleanup if needed
        destroy_combobox_and_label()


def submit_ab(name, address, phone, frame):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    try:
        # Get the last Card_No and increment it by 1
        cursor.execute("SELECT MAX(Card_No) FROM BORROWER")
        last_card_no = cursor.fetchone()[0]
        new_card_no = last_card_no + 1 if last_card_no is not None else 1

        # Insert the new entry with the incremented Card_No
        cursor.execute("INSERT INTO BORROWER (Card_No, Name, Address, Phone) VALUES(:cn, :n, :ad, :p)",
                       {
                           'cn': new_card_no,
                           'n': name.get(),
                           'ad': address.get(),
                           'p': phone.get()
                       })
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to add new borrower: {e}")
    else:
        # Display the new Card_No
        result1_label = tk.Label(
            frame, text="NEW CARD NUMBER: " + str(new_card_no))
        result1_label.grid(row=11, column=0, columnspan=2, pady=20)

    connection.commit()
    connection.close()


def destroy_combobox_and_label():
    if hasattr(on_checkout_clicked, 'book_choosen'):
        on_checkout_clicked.book_choosen.destroy()
        del on_checkout_clicked.book_choosen
    if hasattr(on_checkout_clicked, 'label'):
        on_checkout_clicked.label.destroy()
        del on_checkout_clicked.label

    if hasattr(on_checkout_clicked, 'branch_choosen'):
        on_checkout_clicked.branch_choosen.destroy()
        del on_checkout_clicked.branch_choosen
    if hasattr(on_checkout_clicked, 'branch_label'):
        on_checkout_clicked.branch_label.destroy()
        del on_checkout_clicked.branch_label

    if hasattr(on_checkout_clicked, 'submit_button'):
        on_checkout_clicked.submit_button.destroy()
        del on_checkout_clicked.submit_button

    if hasattr(on_checkout_clicked, 'result_label'):
        on_checkout_clicked.result_label.destroy()
        del on_checkout_clicked.result_label

    if hasattr(on_checkout_clicked, 'card_entry'):
        on_checkout_clicked.card_entry.destroy()
        del on_checkout_clicked.card_entry

    if hasattr(on_checkout_clicked, 'card_label'):
        on_checkout_clicked.card_label.destroy()
        del on_checkout_clicked.card_label

    if hasattr(on_checkout_clicked, 'name_entry'):
        on_checkout_clicked.name_entry.destroy()
        del on_checkout_clicked.name_entry

    if hasattr(on_checkout_clicked, 'address_entry'):
        on_checkout_clicked.address_entry.destroy()
        del on_checkout_clicked.address_entry

    if hasattr(on_checkout_clicked, 'phone_entry'):
        on_checkout_clicked.phone_entry.destroy()
        del on_checkout_clicked.phone_entry

    if hasattr(on_checkout_clicked, 'frame'):
        on_checkout_clicked.frame.destroy()
        del on_checkout_clicked.frame


master = tk.Tk()

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

master.geometry(f"{screen_width}x{screen_height}")

v = tk.StringVar(master, "1")

values = {
    "Checkout Book": "1",
    "Add New Borrower": "2",
    "Add New Book": "3",
    "Number of Copies Loaned": "4",
    "Late Book Returns Analysis": "5",
    "Late Fee List": "6",
    "Book Information": "7"
}

button_width = 20

for (text, value) in values.items():
    button = tk.Radiobutton(master, text=text, variable=v, value=value, indicator=0, width=button_width,
                            command=on_checkout_clicked)
    button.pack(ipady=5, pady=10, anchor="center")

tk.Label(master, text="").pack()

master.mainloop()
