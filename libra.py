import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
import random


def generate_captcha():
    operands = [str(random.randint(1, 10)) for _ in range(2)]
    operator = random.choice(['+', '-', '*'])
    expression = f'{operands[0]} {operator} {operands[1]}'
    result = eval(expression)
    return expression, result


# Function to show CAPTCHA and validate user input
def show_captcha():
    expression, expected_result = generate_captcha()
    user_result = simpledialog.askinteger("CAPTCHA", f"Solve the CAPTCHA: {expression}")

    if user_result is not None and user_result == expected_result:
        return True
    else:
        messagebox.showerror("Error", "CAPTCHA failed. Access denied.")
        return False


# Initial CAPTCHA verification window
root_captcha = tk.Tk()
root_captcha.title('CAPTCHA Verification')

if show_captcha():
    root_captcha.destroy()  # Close the CAPTCHA verification window

    # Create the main application window
    root = tk.Tk()
    root.title('Library')

# Создаем базу данных и таблицу книг
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)')
cursor.execute(
    'CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, client_id INTEGER, book_id INTEGER, order_date DATE DEFAULT CURRENT_DATE, FOREIGN KEY (client_id) REFERENCES clients(id), FOREIGN KEY (book_id) REFERENCES books(id))')


# Функция для добавления книг в базу данных
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()
    update_books_list()


# Функция для удаления книг из базы данных
def remove_book():
    selected_book = books_list.get(books_list.curselection())
    title, author, year = selected_book.split(' (', 1)[0], selected_book.split(', ')[0].split(' (', 1)[1], \
        selected_book.split(', ')[1].rstrip(')')
    cursor.execute('DELETE FROM books WHERE title = ? AND author = ? AND year = ?', (title, author, year))
    conn.commit()
    update_books_list()


# Функция для обновления списка книг
def update_books_list():
    books_list.delete(0, tk.END)
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    for book in books:
        books_list.insert(tk.END, f'{book[1]} ({book[2]}, {book[3]})')


# Функция для поиска книг в базе данных
def search_books():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()

    query = "SELECT * FROM books WHERE "
    if title:
        query += f"title LIKE '%{title}%' AND "
    if author:
        query += f"author LIKE '%{author}%' AND "
    if year:
        query += f"year = {year} AND "
    query = query.rstrip("AND ")

    books_list.delete(0, tk.END)
    cursor.execute(query)
    books = cursor.fetchall()
    for book in books:
        books_list.insert(tk.END, f'{book[1]} ({book[2]}, {book[3]})')


def edit_book():
    selected_book = books_list.get(books_list.curselection())
    if selected_book:
        title, author, year = selected_book.split(' (', 1)[0], selected_book.split(', ')[0].split(' (', 1)[1], \
            selected_book.split(', ')[1].rstrip(')')
        new_title = simpledialog.askstring("Редактировать книгу", f"Изменить название книги ({title}):",
                                           initialvalue=title)
        new_author = simpledialog.askstring("Редактировать книгу", f"Изменить автора ({author}):", initialvalue=author)
        new_year = simpledialog.askstring("Редактировать книгу", f"Изменить год издания ({year}):", initialvalue=year)
        if new_title and new_author and new_year:
            cursor.execute(
                'UPDATE books SET title = ?, author = ?, year = ? WHERE title = ? AND author = ? AND year = ?',
                (new_title, new_author, new_year, title, author, year))
            conn.commit()
            update_books_list()


# Функция для добавления клиентов в базу данных
def add_client():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    cursor.execute('INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
    conn.commit()
    update_clients_list()


# Функция для удаления клиентов из базы данных
def remove_client():
    selected_client = clients_list.get(clients_list.curselection())
    if selected_client:
        name, email, phone = selected_client.split(' (', 1)[0], selected_client.split(', ')[0].split(' (', 1)[1], \
            selected_client.split(', ')[1].rstrip(')')
        cursor.execute('DELETE FROM clients WHERE name = ? AND email = ? AND phone = ?', (name, email, phone))
        conn.commit()
        update_clients_list()


# Функция для обновления списка клиентов
def update_clients_list():
    clients_list.delete(0, tk.END)
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    for client in clients:
        clients_list.insert(tk.END, f'{client[1]} ({client[3]}, {client[2]})')


# Функция для поиска клиентов в базе данных
def search_clients():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    query = "SELECT * FROM clients WHERE "
    if name:
        query += f"name LIKE '%{name}%' AND "
    if email:
        query += f"email LIKE '%{email}%' AND "
    if phone:
        query += f"phone = {phone} AND "
    query = query.rstrip("AND ")

    clients_list.delete(0, tk.END)
    cursor.execute(query)
    clients = cursor.fetchall()
    for client in clients:
        clients_list.insert(tk.END, f'{client[1]} ({client[3]}, {client[2]})')


def edit_client():
    selected_client = clients_list.get(clients_list.curselection())
    if selected_client:
        name, email, phone = selected_client.split(' (', 1)[0], selected_client.split(', ')[0].split(' (', 1)[1], \
            selected_client.split(', ')[1].rstrip(')')
        new_name = simpledialog.askstring("Редактировать клиента", f"Изменить имя клиента ({name}):", initialvalue=name)
        new_email = simpledialog.askstring("Редактировать клиента", f"Изменить email клиента ({email}):",
                                           initialvalue=email)
        new_phone = simpledialog.askstring("Редактировать клиента", f"Изменить телефон клиента ({phone}):",
                                           initialvalue=phone)
        if new_name and new_email and new_phone:
            cursor.execute(
                'UPDATE clients SET name = ?, email = ?, phone = ? WHERE name = ? AND email = ? AND phone = ?',
                (new_name, new_email, new_phone, name, email, phone))
            conn.commit()
            update_clients_list()


def place_order():
    client_name = client_entry.get()
    book_title = book_entry.get()

    # Получаем ID клиента
    cursor.execute('SELECT id FROM clients WHERE name = ?', (client_name,))
    client_id = cursor.fetchone()

    # Получаем ID книги
    cursor.execute('SELECT id FROM books WHERE title = ?', (book_title,))
    book_id = cursor.fetchone()

    # Проверяем наличие клиента и книги в базе данных
    if client_id is not None and book_id is not None:
        # Выполняем заказ
        cursor.execute('INSERT INTO orders (client_id, book_id) VALUES (?, ?)', (client_id[0], book_id[0]))
        conn.commit()
        update_orders_list()


def update_orders_list():
    orders_list.delete(0, tk.END)
    cursor.execute(
        'SELECT orders.id, clients.name, books.title FROM orders JOIN clients ON orders.client_id = clients.id JOIN books ON orders.book_id = books.id')
    orders = cursor.fetchall()
    for order in orders:
        orders_list.insert(tk.END, f'{order[0]} - {order[1]} ({order[2]})')


icon = tk.PhotoImage(file="book-stack-icon--icon-search-engine-16.png")
root.iconphoto(False, icon)

# Создаем поля для ввода информации о книге
title_label = tk.Label(root, text="Название книги")
title_label.grid(row=0, column=0, sticky="w")

title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1, sticky="w")

author_label = tk.Label(root, text="Автор")
author_label.grid(row=1, column=0, sticky="w")

author_entry = tk.Entry(root)
author_entry.grid(row=1, column=1, sticky="w")

year_label = tk.Label(root, text="Год издания")
year_label.grid(row=2, column=0, sticky="w")

year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1, sticky="w")

add_button = tk.Button(root, text="Добавить книгу", command=add_book)
add_button.grid(row=3, column=0, sticky="w")

remove_button = tk.Button(root, text="Удалить книгу", command=remove_book)
remove_button.grid(row=3, column=1, sticky="w")

search_button = tk.Button(root, text="Найти книгу", command=search_books)
search_button.grid(row=3, column=2, sticky="w")

edit_book_button = tk.Button(root, text="Редактировать книгу", command=edit_book)
edit_book_button.grid(row=3, column=3, sticky="w")

# Создаем кнопку для редакции клиента


books_list = tk.Listbox(root, width=50)
books_list.grid(row=4, column=0, columnspan=3, sticky="w")

name_label = tk.Label(root, text="Имя клиента")
name_label.grid(row=5, column=0, sticky="w")

name_entry = tk.Entry(root)
name_entry.grid(row=5, column=1, sticky="w")

email_label = tk.Label(root, text="Email")
email_label.grid(row=6, column=0, sticky="w")

email_entry = tk.Entry(root)
email_entry.grid(row=6, column=1, sticky="w")

phone_label = tk.Label(root, text="Телефон")
phone_label.grid(row=7, column=0, sticky="w")

phone_entry = tk.Entry(root)
phone_entry.grid(row=7, column=1, sticky="w")

add_client_button = tk.Button(root, text="Добавить клиента", command=add_client)
add_client_button.grid(row=8, column=0, sticky="w")

remove_client_button = tk.Button(root, text="Удалить клиента", command=remove_client)
remove_client_button.grid(row=8, column=1, sticky="w")

search_client_button = tk.Button(root, text="Найти клиента", command=search_clients)
search_client_button.grid(row=8, column=2, sticky="w")

edit_client_button = tk.Button(root, text="Редактировать клиента", command=edit_client)
edit_client_button.grid(row=8, column=3, sticky="w")
clients_list = tk.Listbox(root, width=50)
clients_list.grid(row=9, column=0, columnspan=2, sticky="w")

client_label = tk.Label(root, text="Клиент")
client_label.grid(row=10, column=0, sticky="w")

client_entry = tk.Entry(root)
client_entry.grid(row=10, column=1, sticky="w")

book_label = tk.Label(root, text="Книга")
book_label.grid(row=11, column=0, sticky="w")

book_entry = tk.Entry(root)
book_entry.grid(row=11, column=1, sticky="w")

order_button = tk.Button(root, text="Заказать книгу", command=place_order)
order_button.grid(row=12, column=0, sticky="w")

orders_list = tk.Listbox(root, width=50)
orders_list.grid(row=13, column=0, columnspan=2, sticky="w")

update_orders_list()

update_clients_list()

# Запускаем основной цикл программы
root.mainloop()

# Закрываем соединение с базой данных
cursor.close()
conn.close()
