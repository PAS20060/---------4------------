import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаем и подключаемся к базе данных SQLite
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Создаем таблицу сотрудников, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()

# Функция для добавления сотрудника в базу данных
def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    
    cursor.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)', (name, phone, email, salary))
    conn.commit()
    
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    
    display_employees()

# Функция для обновления информации о сотруднике
def update_employee():
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()
        new_salary = salary_entry.get()
        
        cursor.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?',
                       (new_name, new_phone, new_email, new_salary, tree.item(selected_item, 'values')[0]))
        conn.commit()
        display_employees()
        
# Функция для удаления сотрудника
def delete_employee():
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]
        employee_id = tree.item(selected_item, 'values')[0]
        
        cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
        conn.commit()
        display_employees()

# Функция для поиска сотрудника по ФИО
def search_employee():
    search_name = search_entry.get()
    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + search_name + '%',))
    display_employees(result=cursor.fetchall())

# Функция для отображения списка сотрудников в виджете Treeview
def display_employees(result=None):
    for row in tree.get_children():
        tree.delete(row)
    
    if result is None:
        cursor.execute('SELECT * FROM employees')
        result = cursor.fetchall()
    
    for row in result:
        tree.insert('', 'end', values=row)

# Создаем главное окно
root = tk.Tk()
root.title("Список сотрудников компании")

# Создаем и размещаем элементы управления на главном окне
name_label = tk.Label(root, text="ФИО:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

phone_label = tk.Label(root, text="Телефон:")
phone_label.pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

email_label = tk.Label(root, text="Email:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

salary_label = tk.Label(root, text="Заработная плата:")
salary_label.pack()
salary_entry = tk.Entry(root)
salary_entry.pack()

add_button = tk.Button(root, text="Добавить сотрудника", command=add_employee)
add_button.pack()

update_button = tk.Button(root, text="Обновить информацию", command=update_employee)
update_button.pack()

delete_button = tk.Button(root, text="Удалить сотрудника", command=delete_employee)
delete_button.pack()

search_label = tk.Label(root, text="Поиск по ФИО:")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()
search_button = tk.Button(root, text="Искать", command=search_employee)
search_button.pack()

tree = ttk.Treeview(root, columns=('ID', 'ФИО', 'Телефон', 'Email', 'Заработная плата'))
tree.heading('ID', text='ID')
tree.heading('ФИО', text='ФИО')
tree.heading('Телефон', text='Телефон')
tree.heading('Email', text='Email')
tree.heading('Заработная плата', text='Заработная плата')
tree.pack()

display_employees()

root.mainloop()

# Закрытие соединения с базой данных при выходе из программы
conn.close()
