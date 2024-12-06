import sqlite3

# Połączenie z bazą danych SQLite
conn = sqlite3.connect('production.db')
cursor = conn.cursor()

# Tworzenie tabel
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_image TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    id TEXT PRIMARY KEY,
    access_code TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projects (
    id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    access_code TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    target_quantity INTEGER NOT NULL,
    completed_quantity INTEGER DEFAULT 0,
    manager_id TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES Products (id),
    FOREIGN KEY (manager_id) REFERENCES Employees (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    time_logged DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES Employees (id),
    FOREIGN KEY (project_id) REFERENCES Projects (id)
)
''')

# Dodawanie danych do tabeli Employees
employees = [
    ('PROD001', '12345', 'employee'),
    ('PROD002', '67890', 'employee'),
    ('MANA001', '54321', 'manager')
]

cursor.executemany('''
INSERT INTO Employees (id, access_code, role)
VALUES (?, ?, ?)
''', employees)

# Dodawanie danych do tabeli Products
products = [
    ('Graphic Card Model X', None),
    ('Graphic Card Model Y', None)
]

cursor.executemany('''
INSERT INTO Products (product_name, product_image)
VALUES (?, ?)
''', products)

# Dodawanie danych do tabeli Projects
projects = [
    ('PROJ001', 'PRODUCTION Graphic Card Model X', '98765', 1, 150, 'MANA001', 0)
]

cursor.executemany('''
INSERT INTO Projects (id, project_name, access_code, product_id, target_quantity, manager_id, completed)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', projects)

# Zatwierdzenie zmian w bazie danych
conn.commit()

# Zamknięcie połączenia
conn.close()
