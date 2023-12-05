import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta

# card_var = 0
# branch_var = 0
Name = ''
Address = ''
Phone = ''
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


def fetch_copies_loaned(Title):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT Branch_Name, COUNT(*) AS Number_of_Loans
        FROM BOOK_LOANS 
        NATURAL JOIN LIBRARY_BRANCH
        NATURAL JOIN BOOK
        WHERE Title = ? 
        GROUP BY Branch_Id
    ''', (Title,),)
    result = cursor.fetchall()
    # count = result[0] if result is not None else 0
    
    connection.close()
    return result

def fetch_card_info(book_id, branch_id, card_no):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    # Check if the provided card_no is correct
    cursor.execute('''
        SELECT Card_No 
        FROM BORROWER
        WHERE Card_No = ?;
    ''', (card_no,))

    result = cursor.fetchone()

    if not result:
        connection.close()
        return None  # Invalid card_no

    # Insert a new record into BOOK_LOANS table
    Date_out = datetime.now().strftime('%Y-%m-%d')
    Due_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO BOOK_LOANS
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', (book_id, branch_id, card_no, Date_out, Due_date, "None", "None"),)
    connection.commit()
    connection.close()

    return {'Date_out': Date_out, 'Due_date': Due_date}

def fetch_borrower(Name, Address, Phone):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    # Check if the provided card_no is correct
    cursor.execute('''
        INSERT INTO BORROWER 
        VALUES (?, ?, ?, ?);
    ''', (Name, Address, Phone, "None"),)

    cursor.execute('''
        SELECT Card_no 
        FROM BORROWER
        WHERE Name = ?
    ''', (Name, Address, Phone),);

    result = cursor.fetchone()

    connection.commit()
    connection.close()

    return result
def on_submit_clicked():
    book_title = book_var.get()
    # branch_id = branch_var
    # card_no = card_var
    branch_id = int(branch_var.get())
    card_no = int(card_var.get())
    New_name = Name
    New_address = Address
    New_phone = Phone
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    # Get Book_Id based on the selected title
    cursor.execute('SELECT Book_Id FROM BOOK WHERE Title = ?', (book_title,))
    result = cursor.fetchone()

    if result:
        book_id = result[0]

        if v.get() in ["1"]:
            card_info = fetch_card_info(book_id, branch_id, card_no)

            if not card_info:
                on_checkout_clicked.result_label.config(text="Invalid card number.")
        if v.get() in ["2"]:
            new_card_info = fetch_borrower(New_name, New_address, New_phone)
            on_checkout_clicked.result_label.config(text=f'Your new Card Number is: {new_card_info}')   
        if v.get() in ["4"]:
            # Calculate the number of copies loaned out for the selected book and branch
            copies_loaned = fetch_copies_loaned(book_title)
            # Display the result
            for branch_name, number_of_loans in copies_loaned:
                on_checkout_clicked.result_label.config(text=f'Branch: {branch_name} \t Number of Loans: {number_of_loans}')     
    else:
        on_checkout_clicked.result_label.config(text="Book not found.")

    connection.close()


def on_checkout_clicked():
    # Destroy existing combobox and labels
    destroy_combobox_and_label()

    # Initialize result_label
    on_checkout_clicked.result_label = tk.Label(master, text="")

    if v.get() in ["4"]:
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

        # Add a Submit button
        on_checkout_clicked.submit_button = tk.Button(
            master, text="Submit", command=on_submit_clicked)
        on_checkout_clicked.submit_button.pack(pady=10)

        # Add a label to display the result
        on_checkout_clicked.result_label.pack()
    elif v.get() in ["1"]:
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
        global branch_var
        branch_var = tk.StringVar()
        branch_choosen = ttk.Combobox(branch_frame, width=27, textvariable=branch_var)
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
    elif v.get() in ["2"]:
        # Name
        Name_frame = tk.Frame(master)
        Name_frame.pack(padx=10, pady=5, anchor="center")

        ttk.Label(Name_frame, text="Enter your Name:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        global Name
        Name = tk.StringVar()
        Name_entry = tk.Entry(Name_frame, textvariable=Name, width=27)
        Name_entry.pack(side="left", padx=(0, 5))

        on_checkout_clicked.Name_entry = Name_entry
        on_checkout_clicked.Name_label = Name_frame

        # Address
        Address_frame = tk.Frame(master)
        Address_frame.pack(padx=10, pady=5, anchor="center")

        ttk.Label(Address_frame, text="Enter you Address:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        global Address
        Address = tk.StringVar()
        Address_entry = tk.Entry(Address_frame, textvariable=Address, width=27)
        Address_entry.pack(side="left", padx=(0, 5))

        on_checkout_clicked.Address_entry = Address_entry
        on_checkout_clicked.Address_label = Address_frame

        # Phone
        Phone_frame = tk.Frame(master)
        Phone_frame.pack(padx=10, pady=5, anchor="center")

        ttk.Label(Phone_frame, text="Enter your Phone Number:", font=(
            "Times New Roman", 10)).pack(side="left", padx=(0, 5))

        global Phone
        Phone = tk.StringVar()
        Phone_entry = tk.Entry(Phone_frame, textvariable=Phone, width=27)
        Phone_entry.pack(side="left", padx=(0, 5))

        on_checkout_clicked.Phone_entry = Phone_entry
        on_checkout_clicked.Phone_label = Phone_frame

        # Add Submit button
        on_checkout_clicked.submit_button = tk.Button(
            master, text="Submit", command=on_submit_clicked)
        on_checkout_clicked.submit_button.pack(pady=10)

        # Add a label to display the result
        on_checkout_clicked.result_label.pack()
    else:
        destroy_combobox_and_label()


# Rest of the code remains unchanged


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
    if hasattr(on_checkout_clicked, 'card_label'):
        on_checkout_clicked.card_label.destroy()
        del on_checkout_clicked.card_label
    if hasattr(on_checkout_clicked, 'Name_label'):
        on_checkout_clicked.Name_label.destroy()
        del on_checkout_clicked.Name_label
    if hasattr(on_checkout_clicked, 'Address_label'):
        on_checkout_clicked.Address_label.destroy()
        del on_checkout_clicked.Address_label
    if hasattr(on_checkout_clicked, 'Phone_label'):
        on_checkout_clicked.Phone_label.destroy()
        del on_checkout_clicked.Phone_label


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
