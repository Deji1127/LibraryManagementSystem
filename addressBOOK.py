import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime


def fetch_books_from_database():
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Title FROM BOOK;')
    books = cursor.fetchall()
    connection.close()
    book_titles = [book[0] for book in books]
    return book_titles


def fetch_publisher_from_database():
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Publisher_Name FROM PUBLISHER;')
    pNames = cursor.fetchall()
    connection.close()
    publisher_name = [p[0] for p in pNames]
    return publisher_name


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

    elif v.get() == "3":
        if hasattr(on_checkout_clicked, 'frame') and on_checkout_clicked.frame.winfo_exists():
            # Destroy existing frame content
            on_checkout_clicked.frame.destroy()

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=5, anchor="center")

        book = tk.Entry(frame, width=27, name='book_title')
        book.grid(row=0, column=1)

        publisher_names = fetch_publisher_from_database()
        publisher_combobox = ttk.Combobox(
            frame, width=26, values=publisher_names, name='publisher_name')
        publisher_combobox.grid(row=1, column=1)

        author = tk.Entry(frame, width=27, name='book_author')
        author.grid(row=2, column=1)

        book_label = tk.Label(frame, text='Enter Title: ')
        book_label.grid(row=0, column=0)

        pName_label = tk.Label(frame, text='Select Publisher Name: ')
        pName_label.grid(row=1, column=0)

        author_label = tk.Label(
            frame, text='Enter Book Author: ')
        author_label.grid(row=2, column=0)

        submit_btn = tk.Button(frame, text='Submit',
                               command=lambda: submit_new_book(book, publisher_combobox, author, frame))
        submit_btn.grid(row=10, column=0, columnspan=2,
                        pady=10, padx=10, ipadx=140)

        # Store components for later destruction
        on_checkout_clicked.general = book
        on_checkout_clicked.general = publisher_combobox
        on_checkout_clicked.general = author
        on_checkout_clicked.general = frame

    elif v.get() == "5":
        if hasattr(on_checkout_clicked, 'frame') and on_checkout_clicked.frame.winfo_exists():
            # Destroy existing frame content
            on_checkout_clicked.frame.destroy()

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=5, anchor="center")

        # Create Entry widgets for due date range
        from_date_entry = tk.Entry(frame, width=27, name='from_date')
        from_date_entry.grid(row=0, column=1)

        to_date_entry = tk.Entry(frame, width=27, name='to_date')
        to_date_entry.grid(row=1, column=1)

        # Create labels
        from_date_label = tk.Label(
            frame, text='Enter From Date (YYYY-MM-DD): ')
        from_date_label.grid(row=0, column=0)

        to_date_label = tk.Label(frame, text='Enter To Date (YYYY-MM-DD): ')
        to_date_label.grid(row=1, column=0)

        # Create Submit button
        submit_btn = tk.Button(frame, text='Submit',
                               command=lambda: analyze_late_returns(from_date_entry.get(), to_date_entry.get(), result_frame))
        submit_btn.grid(row=2, column=0, columnspan=2,
                        pady=10, padx=10, ipadx=140)

        # Create a frame for displaying late book returns
        result_frame = tk.Frame(master)
        result_frame.pack(padx=10, pady=5, anchor="center")

        # Store components for later destruction
        on_checkout_clicked.from_date_entry = from_date_entry
        on_checkout_clicked.to_date_entry = to_date_entry
        on_checkout_clicked.frame = frame

    else:
        # Handle other cases or cleanup if needed
        destroy_combobox_and_label()


def analyze_late_returns(from_date, to_date, result_frame):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    try:
        # Remove previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Select book loans that were returned late and within the specified date range
        cursor.execute("SELECT * FROM BOOK_LOANS WHERE Returned_Date IS NOT NULL AND Late = 1 AND Date_Out BETWEEN ? AND ?",
                       (from_date, to_date))
        late_returns = cursor.fetchall()

        # Display the late book return information
        if late_returns:
            result_label = tk.Label(result_frame, text="Late Book Returns:")
            result_label.grid(row=0, column=0, columnspan=2, pady=10)

            for row in late_returns:
                due_date = datetime.strptime(row[4], '%Y-%m-%d')
                returned_date = datetime.strptime(row[5], '%Y-%m-%d')
                days_late = (returned_date - due_date).days

                book_info_label = tk.Label(
                    result_frame, text=f"Book Id: {row[0]}, Branch Id: {row[1]}, Card No: {row[2]}, Days Late: {days_late}")
                book_info_label.grid(row=late_returns.index(
                    row) + 1, column=0, columnspan=2, pady=5)

        else:
            result_label = tk.Label(
                result_frame, text="No late book returns within the specified date range.")
            result_label.grid(row=0, column=0, columnspan=2, pady=10)

    except sqlite3.Error as e:
        error_label = tk.Label(
            result_frame, text=f"Error: Failed to analyze late returns: {e}", fg="red")
        error_label.grid(row=0, column=0, columnspan=2, pady=10)

    connection.close()

    # Store the result_frame in the on_checkout_clicked class for later destruction
    on_checkout_clicked.result_frame = result_frame


def submit_new_book(title, publisher_combobox, author, frame):
    connection = sqlite3.connect('lmsproj.db')
    cursor = connection.cursor()

    try:
        # Get the last Book_Id and increment it by 1
        cursor.execute("SELECT MAX(Book_Id) FROM BOOK")
        last_book_id = cursor.fetchone()[0]
        new_book_id = last_book_id + 1 if last_book_id is not None else 1

        # Insert the new entry with the incremented Book_Id into BOOK table
        cursor.execute("INSERT INTO BOOK (Book_Id, Title, Publisher_Name) VALUES(:bid, :t, :pn)",
                       {
                           'bid': new_book_id,
                           't': title.get(),
                           'pn': publisher_combobox.get()
                       })

        # Update the BOOK_COPIES table by adding 5 copies to each branch
        for branch_id in range(1, 6):
            cursor.execute("INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies) VALUES(:bid, :branch_id, 5)",
                           {'bid': new_book_id, 'branch_id': branch_id})

        # Insert the new author's name into BOOK_AUTHORS table
        cursor.execute("INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name) VALUES(:bid, :an)",
                       {'bid': new_book_id, 'an': author.get()})

    except sqlite3.Error as e:
        tk.messagebox.showerror("Error", f"Failed to add new book: {e}")
    else:
        # Display the new Book_Id
        result1_label = tk.Label(
            frame, text="NEW BOOK Successfully Added!")
        result1_label.grid(row=11, column=0, columnspan=2, pady=20)

        book_info_label = tk.Label(
            frame, text=f"Book Id: {new_book_id}\nBook Title: {title.get()}\nPublisher Name: {publisher_combobox.get()}\nAuthor Name: {author.get()}")
        book_info_label.grid(row=12, column=0, columnspan=2, pady=20)

    connection.commit()
    connection.close()


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

    if hasattr(on_checkout_clicked, 'general'):
        on_checkout_clicked.general.destroy()
        del on_checkout_clicked.general

    if hasattr(on_checkout_clicked, 'result_frame'):
        on_checkout_clicked.result_frame.destroy()
        del on_checkout_clicked.result_frame


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
