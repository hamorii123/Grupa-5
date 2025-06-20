import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from baza import create_db
import sqlite3
import datetime
class DentalOfficeApp:
    def __init__(self, root):
        self.root = root #zmiana???
        # Inicjalizacja bazy danych
        self.conn = sqlite3.connect('dental_office.db')
        self.cursor = self.conn.cursor()
        self.load_data_from_db()
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
        self.new_patients_frame = tk.Frame(self.notebook)
        
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
        
        #        # Sample data 
        #self.patients = [
        #    {"last_name": "Kowalski", "first_name": "Konrad", "pesel": "12345678912", "birth_date": "12-02-2004"},
        #    {"last_name": "Nowak", "first_name": "Jan", "pesel": "12345678913", "birth_date": "15-03-1985"},
        #    {"last_name": "Wiśniewski", "first_name": "Tomasz", "pesel": "12345678914", "birth_date": "22-07-1992"},
        #]

        #self.appointments = [
        #    {"date": "06-05-2025", "time": "10:00", "patient": "Tomasz Kot", "procedure": "konsultacja"},
        #    {"date": "06-05-2025", "time": "12:00", "patient": "Dagmara Now.", "procedure": "wypełnienie"},
        #    {"date": "06-05-2025", "time": "13:00", "patient": "Zbigniew Pal.", "procedure": "wyrywanie:8"},
        #]

        #self.payments = [
        #    {"date": "23-01-2025", "number": "1234", "amount": "258.00 zł", "status": "Opłacona"},
        #    {"date": "28-04-2025", "number": "6579", "amount": "459.30 zł", "status": "Opłacona"},
        #]

        #self.documentation = [
        #    {"date": "23-01-2025", "doctor": "Dr. Majewski", "amount": "258.00 zł"},
        #    {"date": "28-04-2025", "doctor": "Dr. Bursztyn", "amount": "459.30 zł"},
        #]
        ## Lista użytkowników (email: hasło)
        #self.users = {
        #    "marcinkowalski@gmail.com": "1234",
        #    "admin@dentist.pl": "haslo123",
        #    "lekarka@clinic.pl": "abcd",
        #    "test": "1"
        #}

        # Build all interfaces
        self.create_login_interface()
        self.create_dashboard_interface()
        self.create_calendar_interface()
        self.create_patients_interface()
        self.create_documentation_interface()
        self.create_payments_interface()

       
        

        
    def create_login_interface(self):
        self.login_frame.configure(bg="#B6ECF8")
    
        # Biały prostokąt jako kontener na wszystko
        container_frame = tk.Frame(self.login_frame, bg="white", relief=tk.RIDGE)
        container_frame.pack(padx=300, pady=100, fill='both', expand=False)
    
        # Czarny napis nad logo
        title_label = tk.Label(container_frame, text="DentiCare", font=('Arial', 28, 'bold'), fg="black", bg="white")
        title_label.pack(pady=(15, 10))
    
        # Logo pod napisem
        try:
            pil_image = Image.open("logo.png")
            pil_image = pil_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(pil_image)
            logo_label = tk.Label(container_frame, image=self.logo_image, bg="white")
            logo_label.pack(pady=(0, 20))
        except Exception as e:
            print("Błąd ładowania obrazu logo:", e)
            fallback_label = tk.Label(container_frame, text="DentiCare", font=('Arial', 24, 'bold'), bg="white", fg="black")
            fallback_label.pack(pady=(0, 20))
    
        # Email i hasło też do container_frame, żeby były w białym prostokącie
        # Email
        email_frame = tk.Frame(container_frame, bg="white")
        email_frame.pack(pady=5, fill='x', padx=20)
        email_label = tk.Label(email_frame, text="Email", font=('Arial', 12), bg="white")
        email_label.pack(anchor="w")
        self.email_entry = tk.Entry(email_frame, width=40, font=('Arial', 10))
        self.email_entry.pack(pady=(0, 10), ipady=3, fill='x')
    
        # Hasło
        password_frame = tk.Frame(container_frame, bg="white")
        password_frame.pack(pady=5, fill='x', padx=20)
        password_label = tk.Label(password_frame, text="Hasło", font=('Arial', 12), bg="white")
        password_label.pack(anchor="w")
        self.password_entry = tk.Entry(password_frame, width=40, show="*", font=('Arial', 10))
        self.password_entry.pack(pady=(0, 10), ipady=3, fill='x')
    
        # Przycisk logowania
        login_button = tk.Button(container_frame, text="Zaloguj się", 
                                 command=self.login, width=20,
                                 bg="black", fg="white",
                                 font=('Arial', 10, 'bold'),
                                 relief=tk.RAISED, borderwidth=2)
        login_button.pack(pady=(20, 10), ipady=5)
    
        # Przycisk zapomniałem hasła
        forgot_button = tk.Button(container_frame, text="Zapomniałeś hasła?", 
                                  command=self.forgot_password, borderwidth=0,
                                  bg="white", fg="black", activebackground="white", activeforeground="darkblue",
                                  font=('Arial', 9))
        forgot_button.pack(pady=(0, 20))

    def create_dashboard_interface(self):

        self.dashboard_frame.configure(bg="#B6ECF8")

        # FILTRUJ TYLKO WIZYTY NA 2025-05-05
        target_date = "2025-05-05"
        todays_appointments = [a for a in self.appointments if a["date"] == target_date]

        # NAVIGATION BAR (cała wysokość po lewej stronie)
        nav_frame = tk.Frame(self.dashboard_frame, bg="#3585AD", width=200)
        nav_frame.pack(side="left", fill="y")

        #centrowanie przycisków pionowo
        button_container = tk.Frame(nav_frame, bg="#3585AD")
        button_container.pack(expand=True)

        buttons = [
            ("Kalendarz wizyt", self.show_calendar),
            ("Pacjenci", self.show_patients),
            ("Nowy pacjent", self.show_new_patient),
            ("Ustawienia", self.show_settings),
            ("Wyloguj się", self.logout)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_container, text=text, command=command, width=20,
                bg="#3585AD", fg="white", relief="flat",
                font=("Arial", 12, "bold"), anchor="center", padx=10
            )
            btn.pack(fill="x", pady=5)

        # CONTENT OBOK PANELU
        content_frame = tk.Frame(self.dashboard_frame, bg="#B6ECF8")
        content_frame.pack(side="left", fill="both", expand=True)

        # Nagłówek
        dashboard_label = tk.Label(content_frame, text="Witaj", font=('Arial', 24, 'bold'), fg="black", bg="white", width=30, anchor="center")
        dashboard_label.pack(pady=20)

        # Kontener dla obu etykiet
        info_frame = tk.Frame(content_frame, bg="#B6ECF8")
        info_frame.pack(pady=10)

        # Pierwsza etykieta
        today_label = tk.Label(info_frame,text=f"Dzisiaj: {len(todays_appointments)} wizyt",font=('Arial', 14),bg="white",padx=10,pady=5)
        today_label.pack(side="left", padx=(0, 10))  # Margines prawy 10px

        # Druga etykieta
        nearest_time = todays_appointments[0]["time"] if todays_appointments else "brak"
        nearest_label = tk.Label(info_frame,text=f"Najbliższa: {nearest_time}",font=('Arial', 14),bg="white",padx=10,pady=5)
        nearest_label.pack(side="left")

        # Tabela wizyt
        columns = ("patient", "procedure", "time")
        self.appointments_tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=9)

        self.appointments_tree.heading("patient", text="Pacjent")
        self.appointments_tree.heading("procedure", text="Zabieg")
        self.appointments_tree.heading("time", text="Godzina")

        self.appointments_tree.column("patient", width=200)
        self.appointments_tree.column("procedure", width=200)
        self.appointments_tree.column("time", width=100)

        for appointment in todays_appointments:
            self.appointments_tree.insert("", "end", values=(appointment["patient"], appointment["procedure"], appointment["time"]))

        self.appointments_tree.pack(pady=10)

        # User info
        user_frame = tk.Frame(content_frame)
        user_frame.pack(pady=20)





    
    def create_calendar_interface(self):
            self.calendar_frame.configure(bg="#B6ECF8")
            # Calendar frame
            calendar_label = tk.Label(self.calendar_frame, text="Kalendarz wizyt", font=('Arial', 24, 'bold'), bg="white")
            calendar_label.pack(pady=20)

            # Ustawienie stałej daty na Poniedziałek 5 maja 2025
            self.current_start_of_week = datetime.date(2025, 5, 5) 
            self.current_end_of_week = self.current_start_of_week + datetime.timedelta(days=6)
        
            # Week label
            self.week_label = tk.Label(self.calendar_frame, 
                                       text=f"{self.current_start_of_week.day}-{self.current_end_of_week.day} {self.current_start_of_week.strftime('%B').upper()} {self.current_start_of_week.year}", 
                                       font=('Arial', 16), bg="white")
            self.week_label.pack()

            # Calendar table
            days = ["PN", "WT", "ŚR", "CZW", "PT", "SOB", "NIEDZ"]
            times = ["10:00", "12:00", "13:00", "14:30", "16:30"]
        
            self.day_to_col = {
                (self.current_start_of_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d'): i + 1
                for i in range(len(days))
            }
            self.time_to_row = {time: i + 1 for i, time in enumerate(times)}

            # Create a frame for the calendar grid
            self.calendar_grid = tk.Frame(self.calendar_frame, bg="white")
            self.calendar_grid.pack(pady=20)

            # Create headers for days
            for i, day in enumerate(days):
                label = tk.Label(self.calendar_grid, text=day, width=15, relief='ridge', font=('Arial', 10, 'bold'))
                label.grid(row=0, column=i + 1, sticky='nsew')

            # Create time slots and empty labels for appointments
            self.calendar_cells = {}
            for row, time in enumerate(times, start=1):
                time_label = tk.Label(self.calendar_grid, text=time, width=8, relief='ridge')
                time_label.grid(row=row, column=0, sticky='nsew')
            
                for col in range(1, len(days) + 1):
                    entry = tk.Label(self.calendar_grid, text="", width=15, height=2, relief='ridge', bg='white')
                    entry.grid(row=row, column=col, sticky='nsew')
                    self.calendar_cells[(row, col)] = entry

            self.fill_calendar_with_appointments(self.current_start_of_week, self.current_end_of_week)

            # --- Nowa ramka dla przycisków ---
            button_frame = tk.Frame(self.calendar_frame, bg="#B6ECF8")
            button_frame.pack(pady=20)

            # Add appointment button
            add_button = tk.Button(button_frame, text="DODAJ WIZYTĘ", command=self.add_appointment, width=20)
            add_button.pack(side=tk.LEFT, padx=10) # Używamy side=tk.LEFT i padx

            # Edit appointment button
            edit_button = tk.Button(button_frame, text="EDYTUJ WIZYTĘ", command=self.edit_appointment, width=20)
            edit_button.pack(side=tk.LEFT, padx=10) # Umieszczamy obok

            # User info
            user_frame = tk.Frame(self.calendar_frame)
            user_frame.pack(pady=20)

    # --- NOWA FUNKCJA DO WYPEŁNIANIA KALENDARZA ---
    def fill_calendar_with_appointments(self, start_date, end_date):
            # Wyczyść istniejące wpisy w kalendarzu przed ponownym wypełnieniem
            for (row, col), label in self.calendar_cells.items():
                label.config(text="", bg="white")

            # Upewnij się, że self.appointments jest załadowane
            if not hasattr(self, 'appointments') or not self.appointments:
                self.load_data_from_db() # Upewnij się, że dane są załadowane

            # Iteruj po załadowanych wizytach
            for apt in self.appointments:
                # Użyj kluczy słownika do pobierania danych
                apt_date_str = apt["date"] 
                apt_time_str = apt["time"]
                patient_name = apt["patient"] # To jest złączenie last_name i first_name pacjenta

                # Sprawdź, czy wizyta mieści się w bieżącym zakresie tygodnia
                apt_date = datetime.datetime.strptime(apt_date_str, '%Y-%m-%d').date()
                if start_date <= apt_date <= end_date:
                    col_index = self.day_to_col.get(apt_date_str)
                    row_index = self.time_to_row.get(apt_time_str)

                    if col_index is not None and row_index is not None:
                        current_text = self.calendar_cells[(row_index, col_index)].cget("text")
                        new_text = f"{current_text}\n{patient_name}" if current_text else patient_name
                    
                        self.calendar_cells[(row_index, col_index)].config(text=new_text.strip(), bg='lightblue')


    def add_appointment(self):
            """Otwiera okno dialogowe do dodawania nowej wizyty."""
            # Utwórz nowe okno Toplevel
            add_apt_window = tk.Toplevel(self.root)
            add_apt_window.title("Dodaj nową wizytę")
            add_apt_window.geometry("400x300")
            add_apt_window.transient(self.root) # Okno dialogowe będzie na wierzchu głównego okna
            add_apt_window.grab_set() # Zablokuj interakcję z głównym oknem

            # Tworzenie etykiet i pól wejściowych
            tk.Label(add_apt_window, text="Wybierz pacjenta:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
            # ComboBox do wyboru pacjenta
            self.patient_var = tk.StringVar()
        
            # Przygotuj listę pacjentów w formacie "Nazwisko Imię (PESEL)"
            patient_options = [
                f"{p['last_name']} {p['first_name']} ({p['pesel']})" 
                for p in self.patients # Zakłada, że self.patients jest załadowane z load_data_from_db
            ]
            # Tworzymy słownik do mapowania stringów z ComboBoxa na ID pacjenta
            self.patient_name_to_id = {
                f"{p['last_name']} {p['first_name']} ({p['pesel']})": p['id']
                for p in self.patients
            }

            self.patient_dropdown = ttk.Combobox(add_apt_window, textvariable=self.patient_var, 
                                                 values=patient_options, state="readonly")
            self.patient_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            self.patient_dropdown.set("Wybierz pacjenta...") # Domyślny tekst

            tk.Label(add_apt_window, text="Data (RRRR-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.date_entry = tk.Entry(add_apt_window)
            self.date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d")) # Domyślna dzisiejsza data

            tk.Label(add_apt_window, text="Godzina (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.time_entry = tk.Entry(add_apt_window)
            self.time_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
            self.time_entry.insert(0, "10:00") # Domyślna godzina

            tk.Label(add_apt_window, text="Procedura:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.procedure_entry = tk.Entry(add_apt_window)
            self.procedure_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

            # Przycisk "Dodaj"
            add_button = tk.Button(add_apt_window, text="Dodaj wizytę", 
                                   command=lambda: self.save_appointment(add_apt_window))
            add_button.grid(row=4, column=0, columnspan=2, pady=10)

            # Skonfiguruj rozciąganie kolumn
            add_apt_window.grid_columnconfigure(1, weight=1)

    def save_appointment(self, window):
            """Zapisuje nową wizytę do bazy danych."""
            selected_patient_name = self.patient_var.get()
            patient_id = self.patient_name_to_id.get(selected_patient_name) # Pobierz ID pacjenta

            apt_date = self.date_entry.get()
            apt_time = self.time_entry.get()
            procedure = self.procedure_entry.get()

            # Walidacja danych
            if not patient_id:
                messagebox.showerror("Błąd", "Proszę wybrać pacjenta.")
                return
            if not apt_date or not apt_time or not procedure:
                messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
                return
        
            # Podstawowa walidacja formatu daty i godziny (można rozszerzyć)
            try:
                datetime.datetime.strptime(apt_date, '%Y-%m-%d')
                datetime.datetime.strptime(apt_time, '%H:%M')
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowy format daty (RRRR-MM-DD) lub godziny (HH:MM).")
                return

            try:
                self.cursor.execute('''
                    INSERT INTO appointments (patient_id, date, time, procedure)
                    VALUES (?, ?, ?, ?)
                ''', (patient_id, apt_date, apt_time, procedure))
                self.conn.commit()
                messagebox.showinfo("Sukces", "Wizyta dodana pomyślnie!")
            
                # Odśwież dane i widok kalendarza
                self.load_data_from_db() # Ponownie załaduj dane z bazy
                #current_start_of_week ustawione?
                # Jeśli nie masz, możesz tymczasowo użyć daty z kalendarza
                current_start_of_week = datetime.date(2025, 5, 5) # Zastąp to zmienną, którą śledzisz
                current_end_of_week = current_start_of_week + datetime.timedelta(days=6)
                self.fill_calendar_with_appointments(current_start_of_week, current_end_of_week)
                window.destroy() # Zamknij okno dialogowe po dodaniu wizyty

            except sqlite3.Error as e:
                messagebox.showerror("Błąd bazy danych", f"Wystąpił błąd podczas dodawania wizyty: {e}")

        
    def edit_appointment(self):
        """Otwiera okno dialogowe do edycji istniejącej wizyty."""
        # Upewnij się, że dane wizyt i pacjentów są załadowane
        if not hasattr(self, 'appointments') or not self.appointments:
            self.load_data_from_db()
        if not hasattr(self, 'patients') or not self.patients:
            self.load_data_from_db()

        edit_apt_window = tk.Toplevel(self.root)
        edit_apt_window.title("Edytuj wizytę")
        edit_apt_window.geometry("500x400")
        edit_apt_window.transient(self.root)
        edit_apt_window.grab_set()

        tk.Label(edit_apt_window, text="Wybierz wizytę do edycji:").pack(pady=10)

        # Lista wizyt do wyboru
        self.selected_appointment_var = tk.StringVar()
        
        # Przygotuj listę wizyt w formacie "Data - Godzina - Pacjent - Procedura"
        appointment_options = []
        for apt in self.appointments:
            display_text = f"{apt['date']} - {apt['time']} - {apt['patient']} - {apt['procedure']}"
            appointment_options.append(display_text)
        
        self.appointment_display_to_data = {
            f"{apt['date']} - {apt['time']} - {apt['patient']} - {apt['procedure']}": apt
            for apt in self.appointments
        }

        self.appointment_dropdown = ttk.Combobox(edit_apt_window, textvariable=self.selected_appointment_var,
                                                 values=appointment_options, state="readonly", width=60)
        self.appointment_dropdown.pack(pady=5)
        self.appointment_dropdown.set("Wybierz wizytę...")

        # Pola do edycji danych
        form_frame = tk.Frame(edit_apt_window)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Pacjent:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.edit_patient_var = tk.StringVar()
        patient_options = [f"{p['last_name']} {p['first_name']} ({p['pesel']})" for p in self.patients]
        self.edit_patient_dropdown = ttk.Combobox(form_frame, textvariable=self.edit_patient_var,
                                                  values=patient_options, state="readonly", width=30)
        self.edit_patient_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Data (RRRR-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.edit_date_entry = tk.Entry(form_frame, width=30)
        self.edit_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Godzina (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.edit_time_entry = tk.Entry(form_frame, width=30)
        self.edit_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Procedura:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.edit_procedure_entry = tk.Entry(form_frame, width=30)
        self.edit_procedure_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Funkcja do wypełniania pól po wybraniu wizyty
        def load_selected_appointment_data(*args):
            selected_display_text = self.selected_appointment_var.get()
            if selected_display_text and selected_display_text in self.appointment_display_to_data:
                selected_apt = self.appointment_display_to_data[selected_display_text]
                
                # Ustawiamy wartości w polach edycji
                self.edit_date_entry.delete(0, tk.END)
                self.edit_date_entry.insert(0, selected_apt['date'])
                
                self.edit_time_entry.delete(0, tk.END)
                self.edit_time_entry.insert(0, selected_apt['time'])
                
                self.edit_procedure_entry.delete(0, tk.END)
                self.edit_procedure_entry.insert(0, selected_apt['procedure'])

                # Wybierz pacjenta w ComboBoxie
                current_patient_display = f"{selected_apt['patient_id']}" # To wymaga ID pacjenta w appointments
                # Musimy znaleźć wyświetlaną nazwę pacjenta po jego ID
                found_patient_name = ""
                for p_id, p_display_name in self.patient_name_to_id.items(): # Odwróćmy słownik
                    if p_display_name == selected_apt['patient_id']: # Porównujemy ID
                         found_patient_name = p_id
                         break
                
                # Przygotuj listę patient_options z oryginalnego formatu z ID, aby znaleźć odpowiedni string
                patient_display_name_from_id = ""
                for p in self.patients:
                    if p['id'] == selected_apt['patient_id']:
                        patient_display_name_from_id = f"{p['last_name']} {p['first_name']} ({p['pesel']})"
                        break
                
                if patient_display_name_from_id:
                    self.edit_patient_var.set(patient_display_name_from_id)
                else:
                    self.edit_patient_var.set("Wybierz pacjenta...") # Domyślna wartość, jeśli nie znaleziono

        self.selected_appointment_var.trace("w", load_selected_appointment_data)

        # Przycisk "Zapisz zmiany"
        save_button = tk.Button(edit_apt_window, text="Zapisz zmiany",
                                command=lambda: self.save_edited_appointment(edit_apt_window))
        save_button.pack(pady=10)

        edit_apt_window.grid_columnconfigure(1, weight=1)
    def save_edited_appointment(self, window):
        """Zapisuje zmiany w istniejącej wizycie do bazy danych."""
        selected_display_text = self.selected_appointment_var.get()
        if not selected_display_text:
            messagebox.showerror("Błąd", "Proszę wybrać wizytę do edycji.")
            return

        selected_apt_data = self.appointment_display_to_data.get(selected_display_text)
        if not selected_apt_data:
            messagebox.showerror("Błąd", "Nie znaleziono danych wybranej wizyty.")
            return

        apt_id = selected_apt_data['id'] # Pobieramy ID wizyty do edycji

        selected_patient_name_for_edit = self.edit_patient_var.get()
        new_patient_id = self.patient_name_to_id.get(selected_patient_name_for_edit)

        new_apt_date = self.edit_date_entry.get()
        new_apt_time = self.edit_time_entry.get()
        new_procedure = self.edit_procedure_entry.get()

        # Walidacja danych
        if not new_patient_id:
            messagebox.showerror("Błąd", "Proszę wybrać pacjenta.")
            return
        if not new_apt_date or not new_apt_time or not new_procedure:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
            return
        
        try:
            datetime.datetime.strptime(new_apt_date, '%Y-%m-%d')
            datetime.datetime.strptime(new_apt_time, '%H:%M')
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty (RRRR-MM-DD) lub godziny (HH:MM).")
            return

        try:
            self.cursor.execute('''
                UPDATE appointments
                SET patient_id = ?, date = ?, time = ?, procedure = ?
                WHERE id = ?
            ''', (new_patient_id, new_apt_date, new_apt_time, new_procedure, apt_id))
            self.conn.commit()
            messagebox.showinfo("Sukces", "Wizyta zaktualizowana pomyślnie!")
            
            # Odśwież dane i widok kalendarza
            self.load_data_from_db()
            self.fill_calendar_with_appointments(self.current_start_of_week, self.current_end_of_week)
            window.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Błąd bazy danych", f"Wystąpił błąd podczas aktualizacji wizyty: {e}")
    def create_patients_interface(self):
        self.patients_frame.configure(bg="#B6ECF8")
        # Patients frame
        patients_label = tk.Label(self.patients_frame, text="Lista pacjentów", font=('Arial', 24, 'bold'),bg="white")
        patients_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.patients_frame,bg="white")
        search_frame.pack(fill='x', padx=20, pady=10)
        
        search_label = tk.Label(search_frame, text="Wyszukaj:", bg="white")
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
                "Profil    Dokumentacja    Płatności"
            ))
        
        self.patients_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Add patient button
        add_button = tk.Button(self.patients_frame, text="DODAJ PACJENTA", command=self.show_new_patient, width=20)
        add_button.pack(pady=20)
    
    def create_documentation_interface(self):
        self.documentation_frame.configure(bg="#B6ECF8")
        # Documentation frame
        doc_label = tk.Label(self.documentation_frame, text="DOKUMENTACJA", font=('Arial', 24, 'bold'), bg="white")
        doc_label.pack(pady=20)
    
        # Search frame
        search_frame = tk.Frame(self.documentation_frame, bg="white")
        search_frame.pack(pady=10)
    
        search_label = tk.Label(search_frame, text="Wyszukaj pacjenta:", font=('Arial', 12), bg="white")
        search_label.pack(side=tk.LEFT, padx=5)
    
        self.patient_search = tk.Entry(search_frame, width=30, bg="white")
        self.patient_search.pack(side=tk.LEFT, padx=5)
    
        search_button = tk.Button(search_frame, text="Szukaj", command=self.search_patient_documentation, bg="white")
        search_button.pack(side=tk.LEFT, padx=5)
    
        # Patient info label
        self.current_patient_label = tk.Label(self.documentation_frame, text="", font=('Arial', 16), bg="white")
        self.current_patient_label.pack(pady=10)
    
        # Documentation table
        columns = ("date", "doctor", "amount", "actions")
        self.doc_tree = ttk.Treeview(self.documentation_frame, columns=columns, show="headings", height=10)
    
        self.doc_tree.heading("date", text="Data wizyty")
        self.doc_tree.heading("doctor", text="Lekarz")
        self.doc_tree.heading("amount", text="Kwota")
        self.doc_tree.heading("actions", text="Akcje")
    
        self.doc_tree.column("date", width=120)
        self.doc_tree.column("doctor", width=200)
        self.doc_tree.column("amount", width=100)
        self.doc_tree.column("actions", width=200)
    
        self.doc_tree.pack(fill='both', expand=True, padx=20, pady=10)
    
        # Add documentation button
        add_button = tk.Button(self.documentation_frame, text="DODAJ DOKUMENTACJĘ", 
                              command=self.add_documentation, width=20)
        add_button.pack(pady=20)

    def search_patient_documentation(self):
        search_term = self.patient_search.get().strip()
        if not search_term:
            messagebox.showwarning("Uwaga", "Wprowadź dane do wyszukiwania")
            return
    
        try:
            self.cursor.execute('''
                SELECT id, last_name, first_name, pesel 
                FROM patients 
                WHERE last_name LIKE ? OR first_name LIKE ? OR pesel LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
            patients = self.cursor.fetchall()
        
            if not patients:
                messagebox.showinfo("Info", "Nie znaleziono pacjentów")
                return
        
            if len(patients) > 1:
                # Jeśli wielu pacjentów, pokaż listę do wyboru
                self.show_patient_selection(patients)
            else:
                # Jeśli tylko jeden, pokaż jego dokumentację
                self.show_patient_documentation(patients[0][0], 
                                              f"{patients[0][1]} {patients[0][2]}")
            
        except sqlite3.Error as e:
            messagebox.showerror("Błąd", f"Błąd bazy danych: {e}")

    def show_patient_selection(self, patients):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Wybierz pacjenta")
    
        tree = ttk.Treeview(selection_window, columns=("last_name", "first_name", "pesel"), show="headings")
        tree.heading("last_name", text="Nazwisko")
        tree.heading("first_name", text="Imię")
        tree.heading("pesel", text="PESEL")
    
        for patient in patients:
            tree.insert("", "end", values=(patient[1], patient[2], patient[3]), iid=patient[0])
    
        tree.pack(fill='both', expand=True, padx=10, pady=10)
    
        def on_select():
            selected_item = tree.focus()
            if selected_item:
                patient_id = int(selected_item)
                patient_data = tree.item(selected_item)['values']
                patient_name = f"{patient_data[0]} {patient_data[1]}"
                selection_window.destroy()
                self.show_patient_documentation(patient_id, patient_name)
    
        select_button = tk.Button(selection_window, text="Wybierz", command=on_select)
        select_button.pack(pady=10)

    def show_patient_documentation(self, patient_id, patient_name):
        self.current_patient_label.config(text=patient_name)
        self.current_patient_id = patient_id

        # Wyczyść poprzednie dane
        for item in self.doc_tree.get_children():
            self.doc_tree.delete(item)

        try:
            self.cursor.execute('''
                SELECT date, doctor, amount, id 
                FROM documentation 
                WHERE patient_id = ?
                ORDER BY date DESC
            ''', (patient_id,))
    
            for row in self.cursor.fetchall():
                doc_id = row[3]
                amount_value = "N/A" # Default value
                try:
                    # Attempt to convert to float
                    amount_value = f"{float(row[2]):.2f} zł"
                except (ValueError, TypeError):
                    # Handle cases where row[2] is not a valid number string
                    amount_value = f"{row[2]} zł (invalid)" # Or just "N/A"

                self.doc_tree.insert("", "end", values=(
                    row[0],
                    row[1],
                    amount_value,
                    "Szczegóły    Edytuj"
                ), iid=doc_id)
        
        except sqlite3.Error as e:
            messagebox.showerror("Błąd", f"Błąd przy ładowaniu dokumentacji: {e}")

    def add_documentation(self):
        if not hasattr(self, 'current_patient_id') or not self.current_patient_id:
            messagebox.showwarning("Uwaga", "Najpierw wybierz pacjenta")
            return
    
        add_window = tk.Toplevel(self.root)
        add_window.title("Dodaj dokumentację")
    
        # Formularz dodawania dokumentacji (bez notes)
        tk.Label(add_window, text="Data wizyty (RRRR-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
    
        tk.Label(add_window, text="Lekarz:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        doctor_entry = tk.Entry(add_window)
        doctor_entry.grid(row=1, column=1, padx=5, pady=5)
    
        tk.Label(add_window, text="Kwota:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        amount_entry = tk.Entry(add_window)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
    
        def save_documentation():
            try:
                # Walidacja danych
                if not date_entry.get() or not doctor_entry.get() or not amount_entry.get():
                    messagebox.showwarning("Uwaga", "Wypełnij wszystkie wymagane pola")
                    return
                
                # Sprawdzenie poprawności kwoty
                amount = amount_entry.get()
                if not amount.replace('.', '').isdigit():  # Prosta walidacja kwoty
                    messagebox.showerror("Błąd", "Nieprawidłowy format kwoty. Wprowadź liczbę.")
                    return
            
                self.cursor.execute('''
                    INSERT INTO documentation (patient_id, date, doctor, amount)
                    VALUES (?, ?, ?, ?)
                ''', (
                    self.current_patient_id,
                    date_entry.get(),
                    doctor_entry.get(),
                    amount
                ))
                self.conn.commit()
                messagebox.showinfo("Sukces", "Dokumentacja dodana pomyślnie")
                add_window.destroy()
                self.show_patient_documentation(self.current_patient_id, self.current_patient_label.cget("text"))
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać dokumentacji: {e}")
    
        save_button = tk.Button(add_window, text="Zapisz", command=save_documentation)
        save_button.grid(row=3, column=1, pady=10, sticky='e')

    
    
    def create_payments_interface(self):
        self.payments_frame.configure(bg="#B6ECF8")
        tk.Label(self.payments_frame, text="PŁATNOŚCI", font=('Arial', 24, 'bold')).pack(pady=20)

        # Ramka wyszukiwania dla płatności
        search_payments_frame = tk.Frame(self.payments_frame, bg="white")
        search_payments_frame.pack(pady=10)

        tk.Label(search_payments_frame, text="Wyszukaj pacjenta (Nazwisko/Imię/PESEL):", bg="white").pack(side=tk.LEFT, padx=5)
        self.patient_search_payments = tk.Entry(search_payments_frame, width=40)
        self.patient_search_payments.pack(side=tk.LEFT, padx=5)
        self.patient_search_payments.bind("<Return>", lambda event: self.search_patient_payments())

        search_button_payments = tk.Button(search_payments_frame, text="Wyszukaj płatności pacjenta", command=self.search_patient_payments, bg="white")
        search_button_payments.pack(side=tk.LEFT, padx=5)

        self.current_patient_label_payments = tk.Label(self.payments_frame, text="Brak wybranego pacjenta", font=('Arial', 12, 'bold'), bg="white")
        self.current_patient_label_payments.pack(pady=10)

        # POPRAWIONE NAZWY KOLUMN W TREEVIEW
        columns = ("date", "number", "amount", "status", "actions")
        self.payments_tree = ttk.Treeview(self.payments_frame, columns=columns, show="headings", height=10)

        self.payments_tree.heading("date", text="Data Płatności")
        self.payments_tree.heading("number", text="Numer Płatności")
        self.payments_tree.heading("amount", text="Kwota")
        self.payments_tree.heading("status", text="Status")
        self.payments_tree.heading("actions", text="Akcje")

        self.payments_tree.column("date", width=120, anchor=tk.CENTER)
        self.payments_tree.column("number", width=150, anchor=tk.W)
        self.payments_tree.column("amount", width=100, anchor=tk.E)
        self.payments_tree.column("status", width=100, anchor=tk.CENTER)
        self.payments_tree.column("actions", width=150, anchor=tk.CENTER)

        self.payments_tree.pack(fill='both', expand=True, padx=20, pady=10)

        self.payments_tree.bind("<Button-1>", self.on_payments_tree_click)

        add_payment_button = tk.Button(self.payments_frame, text="DODAJ PŁATNOŚĆ", command=self.add_payment)
        add_payment_button.pack(pady=10)

    def search_patient_payments(self):
        """
        Wyszukuje pacjenta na podstawie podanego terminu i wyświetla jego płatności.
        """
        search_term = self.patient_search_payments.get().strip()
        if not search_term:
            messagebox.showwarning("Uwaga", "Wprowadź ID, nazwisko, imię lub PESEL do wyszukiwania")
            return
        
        try:
            self.cursor.execute('''
                SELECT id, first_name, last_name, pesel
                FROM patients
                WHERE id = ? OR last_name LIKE ? OR first_name LIKE ? OR pesel LIKE ?
            ''', (search_term, f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

            patients = self.cursor.fetchall()

            if not patients:
                messagebox.showinfo("Info", "Nie znaleziono pacjentów pasujących do kryteriów.")
                self.current_patient_id = None
                self.current_patient_name = ""
                self.current_patient_label_payments.config(text="Brak wybranego pacjenta")
                for item in self.payments_tree.get_children():
                    self.payments_tree.delete(item)
                return

            if len(patients) > 1:
                self.show_patient_selection_for_payments(patients)
            else:
                patient_id = patients[0][0]
                patient_name = f"{patients[0][1]} {patients[0][2]}"
                self.show_patient_payments(patient_id, patient_name)

        except sqlite3.Error as e:
            messagebox.showerror("Błąd", f"Błąd bazy danych podczas wyszukiwania pacjentów: {e}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {e}")

    def show_patient_selection_for_payments(self, patients):
        """
        Wyświetla okno z listą pacjentów do wyboru, gdy wyszukiwanie zwróci wiele wyników.
        """
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Wybierz pacjenta")

        tk.Label(selection_window, text="Znaleziono wielu pacjentów. Wybierz jednego:").pack(pady=10)

        tree = ttk.Treeview(selection_window, columns=("id", "first_name", "last_name", "pesel"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("first_name", text="Imię")
        tree.heading("last_name", text="Nazwisko")
        tree.heading("pesel", text="PESEL")

        tree.column("id", width=50)
        tree.column("first_name", width=120)
        tree.column("last_name", width=120)
        tree.column("pesel", width=100)

        for patient in patients:
            tree.insert("", "end", values=(patient[0], patient[1], patient[2], patient[3]), iid=patient[0])

        tree.pack(fill='both', expand=True, padx=10, pady=10)

        def on_select():
            selected_item = tree.focus()
            if selected_item:
                patient_id = int(selected_item)
                patient_data = tree.item(selected_item)['values']
                patient_name = f"{patient_data[1]} {patient_data[2]}"
                selection_window.destroy()
                self.show_patient_payments(patient_id, patient_name)

        select_button = tk.Button(selection_window, text="Wybierz", command=on_select)
        select_button.pack(pady=10)

    def show_patient_payments(self, patient_id, patient_name):
        """
        Wyświetla płatności dla wybranego pacjenta w Treeview.
        """
        self.current_patient_label_payments.config(text=f"Płatności dla pacjenta: {patient_name}")
        self.current_patient_id = patient_id
        self.current_patient_name = patient_name

        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)
        
        try:
            # POPRAWIONA WERSJA ZAPYTANIA SELECT DLA WYŚWIETLANIA W TREEVIEW
            self.cursor.execute('''
                SELECT date, number, amount, status, id
                FROM payments
                WHERE patient_id = ?
                ORDER BY date DESC
            ''', (patient_id,))
            
            for row in self.cursor.fetchall():
                payment_id = row[4]
                amount_value = "N/A"
                try:
                    amount_value = f"{float(row[2]):.2f} zł"
                except (ValueError, TypeError):
                    amount_value = f"{row[2]} zł (nieprawidłowa)" 

                self.payments_tree.insert("", "end", values=(
                    row[0], # Odpowiada kolumnie 'date'
                    row[1], # Odpowiada kolumnie 'number'
                    amount_value,
                    row[3], # Odpowiada kolumnie 'status'
                    "Szczegóły / Edytuj"
                ), iid=payment_id)
        except sqlite3.Error as e:
            messagebox.showerror("Błąd", f"Błąd przy ładowaniu płatności: {e}")

    def on_payments_tree_click(self, event):
        """
        Obsługuje kliknięcia w Treeview płatności, umożliwiając wyświetlenie szczegółów lub edycję.
        """
        item = self.payments_tree.identify_row(event.y)
        col = self.payments_tree.identify_column(event.x)

        if item and col == '#5':  # Kolumna "Akcje"
            payment_id = int(self.payments_tree.item(item, "iid"))
            x_in_cell = event.x - self.payments_tree.bbox(item, col)[0]
            if x_in_cell < self.payments_tree.column('#5', width) / 2:
                 self.show_payment_details(payment_id)
            else:
                 self.edit_payment(payment_id)

    def show_payment_details(self, payment_id):
        """
        Wyświetla szczegóły wybranej płatności w nowym oknie.
        """
        payment_data = next((p for p in self.payments if p["id"] == payment_id), None)
        if not payment_data:
            messagebox.showerror("Błąd", "Nie znaleziono płatności.")
            return

        details_window = tk.Toplevel(self.root)
        details_window.title("Szczegóły Płatności")

        tk.Label(details_window, text=f"Pacjent: {payment_data['patient_name']}", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Label(details_window, text=f"Data Płatności: {payment_data['payment_date']}").pack(pady=2) # Używamy klucza ze słownika
        tk.Label(details_window, text=f"Numer Płatności: {payment_data['payment_number']}").pack(pady=2) # Używamy klucza ze słownika
        tk.Label(details_window, text=f"Kwota: {payment_data['amount']:.2f} zł").pack(pady=2)
        tk.Label(details_window, text=f"Status: {payment_data['status']}").pack(pady=2)

        close_button = tk.Button(details_window, text="Zamknij", command=details_window.destroy)
        close_button.pack(pady=10)

    def add_payment(self):
        """
        Otwiera okno do dodawania nowej płatności dla aktualnie wybranego pacjenta.
        """
        if not self.current_patient_id:
            messagebox.showwarning("Uwaga", "Najpierw wybierz pacjenta w zakładce 'Płatności' lub 'Pacjenci' (szukając).")
            return

        add_window = tk.Toplevel(self.root)
        add_window.title(f"Dodaj płatność dla: {self.current_patient_name}")

        tk.Label(add_window, text="Data Płatności (RRRR-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        date_entry = tk.Entry(add_window) # Zmieniono nazwę zmiennej
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Numer Płatności:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        number_entry = tk.Entry(add_window) # Zmieniono nazwę zmiennej
        number_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Kwota:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        amount_entry = tk.Entry(add_window)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        status_options = ["Zapłacono", "Do zapłaty", "Częściowo zapłacono", "Anulowano"]
        status_var = tk.StringVar(add_window)
        status_var.set(status_options[0])
        status_menu = ttk.OptionMenu(add_window, status_var, *status_options)
        status_menu.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        def save_payment():
            try:
                # Używamy zmiennych z nowymi nazwami
                if not date_entry.get() or not number_entry.get() or not amount_entry.get():
                    messagebox.showwarning("Uwaga", "Wypełnij wszystkie wymagane pola.")
                    return
                
                amount_str = amount_entry.get().replace(',', '.')
                try:
                    amount = float(amount_str)
                except ValueError:
                    messagebox.showerror("Błąd", "Nieprawidłowy format kwoty. Wprowadź liczbę.")
                    return

                # POPRAWIONA WERSJA ZAPYTANIA INSERT
                self.cursor.execute('''
                    INSERT INTO payments (patient_id, date, number, amount, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    self.current_patient_id,
                    date_entry.get(),    # Odpowiada kolumnie 'date'
                    number_entry.get(),  # Odpowiada kolumnie 'number'
                    amount,
                    status_var.get()
                ))
                self.conn.commit()
                messagebox.showinfo("Sukces", "Płatność dodana pomyślnie!")
                add_window.destroy()
                self.load_data_from_db()
                self.show_patient_payments(self.current_patient_id, self.current_patient_name)
            except sqlite3.IntegrityError:
                messagebox.showerror("Błąd", "Płatność o podanym numerze już istnieje. Użyj unikalnego numeru.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać płatności: {e}")

        save_button = tk.Button(add_window, text="Zapisz", command=save_payment)
        save_button.grid(row=4, column=1, pady=10, sticky='e')

    def edit_payment(self, payment_id):
        """
        Otwiera okno do edycji istniejącej płatności.
        """
        payment_data = next((p for p in self.payments if p["id"] == payment_id), None)
        if not payment_data:
            messagebox.showerror("Błąd", "Nie znaleziono płatności do edycji.")
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edytuj płatność")

        tk.Label(edit_window, text="Data Płatności (RRRR-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        date_entry = tk.Entry(edit_window) # Zmieniono nazwę zmiennej
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        date_entry.insert(0, payment_data['payment_date']) # Używamy klucza ze słownika

        tk.Label(edit_window, text="Numer Płatności:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        number_entry = tk.Entry(edit_window) # Zmieniono nazwę zmiennej
        number_entry.grid(row=1, column=1, padx=5, pady=5)
        number_entry.insert(0, payment_data['payment_number']) # Używamy klucza ze słownika
        number_entry.config(state='disabled') # Numeru płatności nie powinno się zmieniać

        tk.Label(edit_window, text="Kwota:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        amount_entry = tk.Entry(edit_window)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        amount_entry.insert(0, str(payment_data['amount']))

        tk.Label(edit_window, text="Status:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        status_options = ["Zapłacono", "Do zapłaty", "Częściowo zapłacono", "Anulowano"]
        status_var = tk.StringVar(edit_window)
        status_var.set(payment_data['status'])
        status_menu = ttk.OptionMenu(edit_window, status_var, *status_options)
        status_menu.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        def save_edit():
            try:
                # Używamy zmiennych z nowymi nazwami
                if not date_entry.get() or not amount_entry.get():
                    messagebox.showwarning("Uwaga", "Wypełnij wszystkie wymagane pola (Data Płatności, Kwota).")
                    return
                
                amount_str = amount_entry.get().replace(',', '.')
                try:
                    amount = float(amount_str)
                except ValueError:
                    messagebox.showerror("Błąd", "Nieprawidłowy format kwoty. Wprowadź liczbę.")
                    return

                # POPRAWIONA WERSJA ZAPYTANIA UPDATE
                self.cursor.execute('''
                    UPDATE payments
                    SET date = ?, amount = ?, status = ?
                    WHERE id = ?
                ''', (date_entry.get(), amount, status_var.get(), payment_id))
                self.conn.commit()
                messagebox.showinfo("Sukces", "Płatność zaktualizowana pomyślnie!")
                edit_window.destroy()
                self.load_data_from_db()
                self.show_patient_payments(self.current_patient_id, self.current_patient_name)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zaktualizować płatności: {e}")

        save_button = tk.Button(edit_window, text="Zapisz Zmiany", command=save_edit)
        save_button.grid(row=4, column=1, pady=10, sticky='e')


    def __del__(self):
        if self.conn:
            self.conn.close()
    
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Sprawdź w bazie danych
        self.cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = self.cursor.fetchone()
    
        if result and result[0] == password:
            self.notebook.hide(0)
            self.notebook.add(self.dashboard_frame)
            self.notebook.add(self.calendar_frame)
            self.notebook.add(self.patients_frame)
            self.notebook.add(self.documentation_frame)
            self.notebook.add(self.payments_frame)
            self.notebook.select(1)
        else:
            messagebox.showerror("Błąd logowania", "Nieprawidłowy email lub hasło.")

    
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
        #self.notebook.select(2)
        self.notebook.select(self.calendar_frame)
    
    def show_patients(self):
       # self.notebook.select(3)
       self.notebook.select(self.patients_frame)
    
    def show_new_patient(self):
        # Create a new window for adding a patient
        new_window = tk.Toplevel(self.new_patients_frame)
        new_window.title("Dodaj nowego pacjenta")
        new_window.geometry("500x500")
        
        # Form fields
        tk.Label(new_window, text="DODAJ PACJENTA", font=('Arial', 16, 'bold')).pack(pady=10)
        
        fields = [
            ("Nazwisko i imię", ""),
            ("Pesel", ""),
            ("Data ur.", ""),
            ("Państwo", ""),
            ("Miasto", ""),
            ("Kod poczt.", ""),
            ("Ulica", ""),
            ("Nr miesz.", ""),
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
        try:
            # Pobieranie danych z formularza
            last_name = self.new_patient_entries["Nazwisko i imię"].get().split()[0]
            first_name = ' '.join(self.new_patient_entries["Nazwisko i imię"].get().split()[1:])
            pesel = self.new_patient_entries["Pesel"].get()
            birth_date = self.new_patient_entries["Data ur."].get()
            country = self.new_patient_entries["Państwo"].get()
            city = self.new_patient_entries["Miasto"].get()
            postal_code = self.new_patient_entries["Kod poczt."].get()
            street = self.new_patient_entries["Ulica"].get()
            apartment = self.new_patient_entries["Nr miesz."].get()
        
            # Zapisywanie do bazy danych
            self.cursor.execute('''
                INSERT INTO patients 
                (last_name, first_name, pesel, birth_date, country, city, postal_code, street, apartment_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (last_name, first_name, pesel, birth_date, country, city, postal_code, street, apartment))
        
            self.conn.commit()
            messagebox.showinfo("Sukces", "Nowy pacjent został dodany")
        
            # Odśwież listę pacjentów
            self.load_data_from_db()
            self.refresh_patients_tree()
        
            window.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")
            self.conn.rollback()
    def refresh_patients_tree(self):
        # Czyszczenie obecnych danych
        for i in self.patients_tree.get_children():
            self.patients_tree.delete(i)
    
        # Dodawanie nowych danych
        for patient in self.patients:
            self.patients_tree.insert("", "end", values=(
                patient["last_name"],
                patient["first_name"],
                patient["pesel"],
                "Profil    Dokumentacja    Płatności"
            ))
    #def search_patient(self):
    #    search_term = self.search_entry.get()
    #    # Here you would implement search functionality
    #    messagebox.showinfo("Wyszukiwanie", f"Wyszukiwanie pacjenta: {search_term}")
    def search_patient(self):
        query = self.search_entry.get().lower()
    
        # Czyszczenie TreeView
        for i in self.patients_tree.get_children():
            self.patients_tree.delete(i)
    
        # Wyszukiwanie w bazie danych
        self.cursor.execute('''
            SELECT * FROM patients 
            WHERE LOWER(last_name) LIKE ? OR LOWER(first_name) LIKE ?
        ''', (f"%{query}%", f"%{query}%"))
    
        # Dodawanie wyników
        for patient in self.cursor.fetchall():
            self.patients_tree.insert("", "end", values=(
                patient[1],  # last_name
                patient[2],  # first_name
                patient[3],  # pesel
                "Profil    Dokumentacja    Płatności"
            ))
    
    #def add_appointment(self):
    #    messagebox.showinfo("Dodaj wizytę", "Formularz dodawania nowej wizyty")
    
    #def add_documentation(self):
    #    messagebox.showinfo("Dodaj dokumentację", "Formularz dodawania nowej dokumentacji")
    
    #def add_payment(self):
    #    messagebox.showinfo("Dodaj płatność", "Formularz dodawania nowej płatności")
    
    def show_settings(self):
        messagebox.showinfo("Ustawienia", "Panel ustawień systemu")
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    def load_data_from_db(self):
        """Ładuje dane z bazy danych do atrybutów klasy"""
        try:
            # Pobierz pacjentów
            self.cursor.execute("SELECT id, last_name, first_name, pesel, birth_date FROM patients")
            self.patients = [
                {"id": row[0], "last_name": row[1], "first_name": row[2], 
                 "pesel": row[3], "birth_date": row[4]}
                for row in self.cursor.fetchall()
            ]
            
            # Pobierz wizyty z nazwiskami pacjentów
            self.cursor.execute('''
                SELECT a.id, a.date, a.time, p.last_name || ' ' || p.first_name as patient, a.procedure, a.patient_id
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
            ''')
            self.appointments = [
                {"id": row[0], "date": row[1], "time": row[2], "patient": row[3], "procedure": row[4], "patient_id": row[5]}
                for row in self.cursor.fetchall()
            ]
            
            # Pobierz płatności
            self.cursor.execute("SELECT patient_id, date, number, amount, status FROM payments")
            self.payments = [
                {"patient_id":row[0],"date": row[1], "number": row[2], "amount": row[3], "status": row[4]}
                for row in self.cursor.fetchall()
            ]
            
            # Pobierz dokumentację
            self.cursor.execute('''
                SELECT d.date, d.doctor, d.amount, p.last_name || ' ' || p.first_name as patient
                FROM documentation d
                JOIN patients p ON d.patient_id = p.id
            ''')
            self.documentation = [
                {"date": row[0], "doctor": row[1], "amount": row[2], "patient": row[3]}
                for row in self.cursor.fetchall()
            ]
            
            # Pobierz użytkowników
            self.cursor.execute("SELECT email, password FROM users")
            self.users = {row[0]: row[1] for row in self.cursor.fetchall()}
            
        except sqlite3.Error as e:
            print(f"Błąd podczas ładowania danych z bazy: {e}")
        #print("Dane załadowane: appointments =", hasattr(self, 'appointments'))



if __name__ == "__main__":

    create_db();
    root = tk.Tk()
    app = DentalOfficeApp(root)
    root.mainloop()