
import sqlite3

def create_db():
    conn = sqlite3.connect('dental_office.db')
    c = conn.cursor()
   
    #c.execute("DELETE FROM payments")  # usuwa wszystkie płatności
    # Tworzenie tabel
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            pesel TEXT UNIQUE NOT NULL,
            birth_date TEXT,
            country TEXT,
            city TEXT,
            postal_code TEXT,
            street TEXT,
            apartment_number TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            patient_id INTEGER,
            procedure TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            number TEXT UNIQUE,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            UNIQUE(patient_id, date, amount)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS documentation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            doctor TEXT,
            amount TEXT,
            patient_id INTEGER,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    ''')

    # Dodanie przykładowych użytkowników
    users = [
        ("marcinkowalski@gmail.com", "1234"),
        ("admin@dentist.pl", "haslo123"),
        ("lekarka@clinic.pl", "abcd"),
        ("test", "1")
    ]
    c.executemany("INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)", users)

    # Dodanie przykładowych pacjentów
    patients = [
        ("Kowalski", "Konrad", "12345678912", "2004-02-12", "Polska", "Gabrilów", "72-100", "Kon. 3 imija", "3/5"),
        ("Nowak", "Jan", "12345678913", "1985-03-15", "Polska", "Warszawa", "00-001", "Marszałkowska", "10"),
        ("Wiśniewski", "Tomasz", "12345678914", "1992-07-22", "Polska", "Kraków", "30-001", "Krakowska", "5A")
    ]
    c.executemany('''
        INSERT OR IGNORE INTO patients 
        (last_name, first_name, pesel, birth_date, country, city, postal_code, street, apartment_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', patients)

    # Dodanie przykładowych wizyt (zakładając id pacjentów 1,2,3)

    appointments = [
        ("2025-05-05", "10:00", 1, "konsultacja"),
        ("2025-05-05", "12:00", 2, "wypełnienie"),
        ("2025-05-05", "13:00", 3, "wyrywanie:8"),
        ("2026-05-05", "11:00", 1, "wybielanie")
    ]
    c.executemany('''
        INSERT OR IGNORE INTO appointments (date, time, patient_id, procedure) VALUES (?, ?, ?, ?)
    ''', appointments)
    #c.execute("ALTER TABLE payments ADD COLUMN patient_id INTEGER")
    # Dodanie przykładowych płatności
    payments = [
        # Format: (patient_id, date, number, amount, status)
        (1, "2025-01-23", "1234", 258.00, "Opłacona"),
        (1, "2025-04-28", "6579", 459.30, "Opłacona"),
        (2, "2025-05-10", "8888", 120.50, "Do zapłaty")
    ]
    #c.executemany('''
    #    INSERT OR IGNORE INTO payments (patient_id, date, number, amount, status)
    #    VALUES (?, ?, ?, ?, ?)
    #''', payments)
    for payment in payments:
        try:
            c.execute('''
                INSERT INTO payments (patient_id, date, number, amount, status)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(number) DO NOTHING
            ''', payment)
        except sqlite3.Error as e:
            print(f"Błąd przy wstawianiu płatności: {e}")
    # Dodanie przykładowej dokumentacji
    documentation = [
        ("2025-01-23", "Dr. Majewski", "258.00 zł", 1),
        ("2025-04-28", "Dr. Bursztyn", "459.30 zł", 1)
    ]
    c.executemany('''
        INSERT OR IGNORE INTO documentation (date, doctor, amount, patient_id) VALUES (?, ?, ?, ?)
    ''', documentation)
    #c.execute("DELETE FROM appointments")
    

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()