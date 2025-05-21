import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class DentalOfficeApp:
    def __init__(self, root):

        # Create notebook for multiple tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create frames for each tab
        self.login_frame = tk.Frame(self.notebook)
        self.calendar_frame = tk.Frame(self.notebook)
        self.patients_frame = tk.Frame(self.notebook)
        self.documentation_frame = tk.Frame(self.notebook)
        self.payments_frame = tk.Frame(self.notebook)
        self.dashboard_frame = tk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.login_frame, text='Logowanie')
        self.notebook.add(self.dashboard_frame, text='Pulpit')
        self.notebook.add(self.calendar_frame, text='Kalendarz wizyt')
        self.notebook.add(self.patients_frame, text='Pacjenci')
        self.notebook.add(self.documentation_frame, text='Dokumentacja')
        self.notebook.add(self.payments_frame, text='Płatności')
        
        # Initially hide all tabs except login
        self.notebook.hide(1)
        self.notebook.hide(2)
        self.notebook.hide(3)
        self.notebook.hide(4)
        self.notebook.hide(5)
                # Sample data 
        self.patients = [
            {"last_name": "Kowalski", "first_name": "Konrad", "pesel": "12345678912", "birth_date": "12-02-2004"},
            {"last_name": "Nowak", "first_name": "Jan", "pesel": "12345678913", "birth_date": "15-03-1985"},
            {"last_name": "Wiśniewski", "first_name": "Tomasz", "pesel": "12345678914", "birth_date": "22-07-1992"},
        ]

        self.appointments = [
            {"date": "06-05-2025", "time": "10:00", "patient": "Tomasz Kot", "procedure": "konsultacja"},
            {"date": "06-05-2025", "time": "12:00", "patient": "Dagmara Now.", "procedure": "wypełnienie"},
            {"date": "06-05-2025", "time": "13:00", "patient": "Zbigniew Pal.", "procedure": "wyrywanie:8"},
        ]

        self.payments = [
            {"date": "23-01-2025", "number": "1234", "amount": "258.00 zł", "status": "Opłacona"},
            {"date": "28-04-2025", "number": "6579", "amount": "459.30 zł", "status": "Opłacona"},
        ]

        self.documentation = [
            {"date": "23-01-2025", "doctor": "Dr. Majewski", "amount": "258.00 zł"},
            {"date": "28-04-2025", "doctor": "Dr. Bursztyn", "amount": "459.30 zł"},
        ]

        # Build all interfaces
        self.create_login_interface()
        self.create_dashboard_interface()
        self.create_calendar_interface()
        self.create_patients_interface()
        self.create_documentation_interface()
        self.create_payments_interface()
        

        
    
    def create_login_interface(self):
        # Login frame
        login_label = tk.Label(self.login_frame, text="DentiCare", font=('Arial', 24, 'bold'),bg="lightblue")
        login_label.pack(pady=20)
        
        # Email
        email_label = tk.Label(self.login_frame, text="Email", font=('Arial', 12))
        email_label.pack()
        self.email_entry = tk.Entry(self.login_frame, width=40)
        self.email_entry.pack(pady=5)
        
        # Password
        password_label = tk.Label(self.login_frame, text="Hasło", font=('Arial', 12))
        password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, width=40, show="*")
        self.password_entry.pack(pady=5)
        
        # Login button
        login_button = tk.Button(self.login_frame, text="Zaloguj się", command=self.login, width=20)
        login_button.pack(pady=20)
        
        # Forgot password
        forgot_button = tk.Button(self.login_frame, text="Zapomniałeś hasła?", command=self.forgot_password, borderwidth=0)
        forgot_button.pack()
    
    def create_dashboard_interface(self):
        # Dashboard frame
        dashboard_label = tk.Label(self.dashboard_frame, text="Pulpit", font=('Arial', 24, 'bold'))
        dashboard_label.pack(pady=20)
        
        # Today's appointments
        today_label = tk.Label(self.dashboard_frame, text=f"Dzisiaj: {len(self.appointments)} wizyt", font=('Arial', 14))
        today_label.pack(pady=10)
        
        nearest_label = tk.Label(self.dashboard_frame, text="Najbliższa: 10:00", font=('Arial', 12))
        nearest_label.pack()
        
        # Appointments table
        columns = ("patient", "procedure", "time")
        self.appointments_tree = ttk.Treeview(self.dashboard_frame, columns=columns, show="headings", height=5)
        
        self.appointments_tree.heading("patient", text="Pacjent")
        self.appointments_tree.heading("procedure", text="Zabieg")
        self.appointments_tree.heading("time", text="Godzina")
        
        self.appointments_tree.column("patient", width=200)
        self.appointments_tree.column("procedure", width=200)
        self.appointments_tree.column("time", width=100)
        
        for appointment in self.appointments:
            self.appointments_tree.insert("", "end", values=(appointment["patient"], appointment["procedure"], appointment["time"]))
        
        self.appointments_tree.pack(pady=20)
        
        # User info
        user_frame = tk.Frame(self.dashboard_frame)
        user_frame.pack(pady=20)
        
        user_label = tk.Label(user_frame, text="Marcin Kowalski\nmarcinkowalski@gmail.com", font=('Arial', 12))
        user_label.pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(self.dashboard_frame)
        nav_frame.pack()
        
        buttons = [
            ("Kalendarz wizyt", self.show_calendar),
            ("Pacjenci", self.show_patients),
            ("Nowy pacjent", self.show_new_patient),
            ("Ustawienia", self.show_settings),
            ("Wyloguj się", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(nav_frame, text=text, command=command, width=15)
            btn.pack(side='left', padx=5, pady=5)
    
    def create_calendar_interface(self):
        # Calendar frame
        calendar_label = tk.Label(self.calendar_frame, text="Kalendarz wizyt", font=('Arial', 24, 'bold'))
        calendar_label.pack(pady=20)
        
        # Week label
        week_label = tk.Label(self.calendar_frame, text="5-11 MAJ 2025", font=('Arial', 16))
        week_label.pack()
        
        # Calendar table
        days = ["PN", "WT", "ŚR", "CZW", "PT", "SOB", "NIEDZ"]
        times = ["10:00", "12:00", "13:00", "14:30", "16:30"]
        
        # Create a frame for the calendar grid
        calendar_grid = tk.Frame(self.calendar_frame)
        calendar_grid.pack(pady=20)
        
        # Create headers for days
        for i, day in enumerate(days):
            label = tk.Label(calendar_grid, text=day, width=15, relief='ridge', font=('Arial', 10, 'bold'))
            label.grid(row=0, column=i, sticky='nsew')
        
        # Create time slots
        for row, time in enumerate(times, start=1):
            time_label = tk.Label(calendar_grid, text=time, width=8, relief='ridge')
            time_label.grid(row=row, column=0, sticky='nsew')
            
            for col in range(1, len(days) + 1):
                entry = tk.Label(calendar_grid, text="", width=15, height=2, relief='ridge', bg='white')
                entry.grid(row=row, column=col, sticky='nsew')
        
        # Sample appointments
        appointments_data = {
            (1, 1): "T. Kat.",
            (1, 3): "T. Kat.",
            (2, 2): "D. Men.",
            (3, 4): "Z. Mat.",
            (4, 5): "W. Mt.",
            (5, 6): "Z. Kit.",
            (2, 1): "D. Now.",
            (2, 2): "T. Wat.",
            (2, 3): "Z. Nat.",
            (2, 4): "T. Mat.",
            (2, 5): "C. Men.",
            (2, 6): "T. Zbt.",
            (3, 1): "Z. Pat.",
            (3, 2): "K. Pap.",
            (3, 3): "Z. Mat.",
            (3, 4): "W. Zno.",
            (3, 5): "R. Zur.",
            (3, 6): "R. Dyn.",
            (4, 1): "A. Kot.",
            (4, 2): "A. Mit.",
            (4, 3): "A. Köb.",
            (4, 4): "B. Bab.",
            (4, 5): "W. Kat.",
            (5, 1): "M. Konr.",
            (5, 3): "M. Konr.",
            (5, 4): "W. Lanz.",
            (5, 5): "B. Kom.",
        }
        
        # Fill in appointments
        for (row, col), text in appointments_data.items():
            if row <= len(times) and col <= len(days):
                label = tk.Label(calendar_grid, text=text, width=15, height=2, relief='ridge', bg='lightblue')
                label.grid(row=row, column=col, sticky='nsew')
        
        # Add appointment button
        add_button = tk.Button(self.calendar_frame, text="DODAJ WIZYTĘ", command=self.add_appointment, width=20)
        add_button.pack(pady=20)
        
        # User info
        user_frame = tk.Frame(self.calendar_frame)
        user_frame.pack(pady=20)
        
        user_label = tk.Label(user_frame, text="Marcin Kowalski\nmarcinkowalski@gmail.com", font=('Arial', 12))
        user_label.pack()
    
    def create_patients_interface(self):
        # Patients frame
        patients_label = tk.Label(self.patients_frame, text="Lista pacjentów", font=('Arial', 24, 'bold'))
        patients_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.patients_frame)
        search_frame.pack(fill='x', padx=20, pady=10)
        
        search_label = tk.Label(search_frame, text="Wyszukaj:")
        search_label.pack(side='left')
        
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side='left', padx=10)
        
        search_button = tk.Button(search_frame, text="Szukaj", command=self.search_patient)
        search_button.pack(side='left')
        
        # Patients table
        columns = ("last_name", "first_name", "pesel", "actions")
        self.patients_tree = ttk.Treeview(self.patients_frame, columns=columns, show="headings", height=10)
        
        self.patients_tree.heading("last_name", text="Nazwisko")
        self.patients_tree.heading("first_name", text="Imię")
        self.patients_tree.heading("pesel", text="Pesel")
        self.patients_tree.heading("actions", text="Akcje")
        
        self.patients_tree.column("last_name", width=150)
        self.patients_tree.column("first_name", width=100)
        self.patients_tree.column("pesel", width=120)
        self.patients_tree.column("actions", width=300)
        
        for patient in self.patients:
            self.patients_tree.insert("", "end", values=(
                patient["last_name"],
                patient["first_name"],
                patient["pesel"],
                "Profil    Dokumentacja    Patronaż"
            ))
        
        self.patients_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Add patient button
        add_button = tk.Button(self.patients_frame, text="DODAJ PACJENTA", command=self.show_new_patient, width=20)
        add_button.pack(pady=20)
    
    def create_documentation_interface(self):
        # Documentation frame
        doc_label = tk.Label(self.documentation_frame, text="DOKUMENTACJA", font=('Arial', 24, 'bold'))
        doc_label.pack(pady=20)
        
        patient_label = tk.Label(self.documentation_frame, text="Konrad Kowalski", font=('Arial', 16))
        patient_label.pack()
        
        # Documentation table
        columns = ("date", "doctor", "amount", "actions")
        self.doc_tree = ttk.Treeview(self.documentation_frame, columns=columns, show="headings", height=5)
        
        self.doc_tree.heading("date", text="Data wizyty")
        self.doc_tree.heading("doctor", text="Lekarz")
        self.doc_tree.heading("amount", text="Kwota")
        self.doc_tree.heading("actions", text="Akcje")
        
        self.doc_tree.column("date", width=120)
        self.doc_tree.column("doctor", width=200)
        self.doc_tree.column("amount", width=100)
        self.doc_tree.column("actions", width=200)
        
        for doc in self.documentation:
            self.doc_tree.insert("", "end", values=(
                doc["date"],
                doc["doctor"],
                doc["amount"],
                "Szczegóły    Edytuj"
            ))
        
        self.doc_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Add documentation button
        add_button = tk.Button(self.documentation_frame, text="DODAJ", command=self.add_documentation, width=20)
        add_button.pack(pady=20)
        
        # User info
        user_frame = tk.Frame(self.documentation_frame)
        user_frame.pack(pady=20)
        
        user_label = tk.Label(user_frame, text="Marcin Kowalski\nmarcinkowalski@gmail.com", font=('Arial', 12))
        user_label.pack()
    
    def create_payments_interface(self):
        # Payments frame
        payments_label = tk.Label(self.payments_frame, text="PŁATNOŚCI", font=('Arial', 24, 'bold'))
        payments_label.pack(pady=20)
        
        patient_label = tk.Label(self.payments_frame, text="Konrad Kowalski", font=('Arial', 16))
        patient_label.pack()
        
        # Payments table
        columns = ("date", "number", "amount", "status", "actions")
        self.payments_tree = ttk.Treeview(self.payments_frame, columns=columns, show="headings", height=5)
        
        self.payments_tree.heading("date", text="Data wizyty")
        self.payments_tree.heading("number", text="Numer płatności")
        self.payments_tree.heading("amount", text="Kwota")
        self.payments_tree.heading("status", text="Status")
        self.payments_tree.heading("actions", text="Szczegóły")
        
        self.payments_tree.column("date", width=120)
        self.payments_tree.column("number", width=120)
        self.payments_tree.column("amount", width=100)
        self.payments_tree.column("status", width=100)
        self.payments_tree.column("actions", width=100)
        
        for payment in self.payments:
            self.payments_tree.insert("", "end", values=(
                payment["date"],
                payment["number"],
                payment["amount"],
                payment["status"],
                "Szczegóły"
            ))
        
        self.payments_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Add payment button
        add_button = tk.Button(self.payments_frame, text="DODAJ", command=self.add_payment, width=20)
        add_button.pack(pady=20)
        
        # User info
        user_frame = tk.Frame(self.payments_frame)
        user_frame.pack(pady=20)
        
        user_label = tk.Label(user_frame, text="Marcin Kowalski\nmarcinkowalski@gmail.com", font=('Arial', 12))
        user_label.pack()
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        # Simple validation
        if email and password:
            self.notebook.hide(0)  # Hide login tab
            self.notebook.add(self.dashboard_frame)  # Show dashboard
            self.notebook.add(self.calendar_frame)
            self.notebook.add(self.patients_frame)
            self.notebook.add(self.documentation_frame)
            self.notebook.add(self.payments_frame)
            self.notebook.select(1)  # Select dashboard tab
        else:
            messagebox.showerror("Błąd", "Proszę wprowadzić email i hasło")
    
    def logout(self):
        self.notebook.hide(1)
        self.notebook.hide(2)
        self.notebook.hide(3)
        self.notebook.hide(4)
        self.notebook.hide(5)
        self.notebook.select(0)
    
    def forgot_password(self):
        messagebox.showinfo("Przypomnienie hasła", "Link do resetowania hasła został wysłany na podany adres email.")
    
    def show_calendar(self):
        self.notebook.select(2)
    
    def show_patients(self):
        self.notebook.select(3)
    
    def show_new_patient(self):
        # Create a new window for adding a patient
        new_window = tk.Toplevel(self.root)
        new_window.title("Dodaj nowego pacjenta")
        new_window.geometry("500x500")
        
        # Form fields
        tk.Label(new_window, text="DODAJ PACJENTA", font=('Arial', 16, 'bold')).pack(pady=10)
        
        fields = [
            ("Nazwisko i imię", "Michelel Bogdan"),
            ("Pesel", "12345678912"),
            ("Data ur.", "12-02-2004"),
            ("Państwo", "Polska"),
            ("Miasto", "Gabrilów"),
            ("Kod poczt.", "72-100"),
            ("Ulica", "Kon. 3 imija"),
            ("Nr miesz.", "3/5"),
        ]
        
        self.new_patient_entries = {}
        
        for label_text, default_value in fields:
            frame = tk.Frame(new_window)
            frame.pack(fill='x', padx=20, pady=5)
            
            label = tk.Label(frame, text=label_text, width=15, anchor='w')
            label.pack(side='left')
            
            entry = tk.Entry(frame)
            entry.insert(0, default_value)
            entry.pack(side='left', fill='x', expand=True)
            
            self.new_patient_entries[label_text] = entry
        
        # Buttons
        button_frame = tk.Frame(new_window)
        button_frame.pack(pady=20)
        
        cancel_button = tk.Button(button_frame, text="ANULUJ", command=new_window.destroy)
        cancel_button.pack(side='left', padx=10)
        
        add_button = tk.Button(button_frame, text="DODAJ", command=lambda: self.save_new_patient(new_window))
        add_button.pack(side='left', padx=10)
    
    def save_new_patient(self, window):
        # Here you would save the new patient to your database
        messagebox.showinfo("Sukces", "Nowy pacjent został dodany")
        window.destroy()
    
    def search_patient(self):
        search_term = self.search_entry.get()
        # Here you would implement search functionality
        messagebox.showinfo("Wyszukiwanie", f"Wyszukiwanie pacjenta: {search_term}")
    
    def add_appointment(self):
        messagebox.showinfo("Dodaj wizytę", "Formularz dodawania nowej wizyty")
    
    def add_documentation(self):
        messagebox.showinfo("Dodaj dokumentację", "Formularz dodawania nowej dokumentacji")
    
    def add_payment(self):
        messagebox.showinfo("Dodaj płatność", "Formularz dodawania nowej płatności")
    
    def show_settings(self):
        messagebox.showinfo("Ustawienia", "Panel ustawień systemu")


if __name__ == "__main__":
    root = tk.Tk()
    app = DentalOfficeApp(root)
    root.mainloop()
