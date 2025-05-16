import sqlite3
 
# Połączenie z bazą danych
conn = sqlite3.connect("Gabinet_baza.db")
cursor = conn.cursor()
 
# Tabele z pierwszego diagramu (dostawy, produkty, magazyn)
cursor.executescript("""
CREATE TABLE Adres_dostawcy (
    ID_adresu INTEGER PRIMARY KEY,
    ID_dostawcy INTEGER,
    Ulica VARCHAR(100),
    Miasto VARCHAR(100),
    Kod_pocztowy VARCHAR(6),
    Kraj INT
);
 
CREATE TABLE Dostawca (
    ID_dostawcy INTEGER PRIMARY KEY,
    Nazwa_firmy VARCHAR(100),
    Telefon VARCHAR(15),
    Email VARCHAR(100),
    NIP VARCHAR(100)
);
 
CREATE TABLE Pracownik (
    ID_pracownika INTEGER PRIMARY KEY,
    Imie VARCHAR(50),
    Nazwisko VARCHAR(50),
    Stanowisko VARCHAR(50)
);
 
CREATE TABLE Zamowienie (
    ID_zamowienia INTEGER PRIMARY KEY,
    ID_dostawcy INTEGER,
    ID_pracownika INTEGER,
    Data_zamowienia DATE,
    Status VARCHAR(100),
    Data_dostawy DATE,
    Koszt_calkowity INTEGER
);
 
CREATE TABLE Platnosc_dostawa (
    ID_platnosci INTEGER PRIMARY KEY,
    ID_zamowienia INTEGER,
    Kwota DECIMAL(10,2),
    Data_platnosci DATE,
    Sposob_platnosci VARCHAR(100)
);
 
CREATE TABLE Kategoria (
    ID_kategorii INTEGER PRIMARY KEY,
    Nazwa VARCHAR(100),
    Opis VARCHAR(100)
);
 
CREATE TABLE Produkt (
    ID_produktu INTEGER PRIMARY KEY,
    ID_kategorii INTEGER,
    Nazwa VARCHAR(255),
    Jednostka_miary VARCHAR(20)
);
 
CREATE TABLE Zamowienie_produkt (
    ID_produktu INTEGER,
    ID_zamowienia INTEGER,
    Ilosc INTEGER,
    Cena_produktu DECIMAL(10,2),
    PRIMARY KEY (ID_produktu, ID_zamowienia)
);
 
CREATE TABLE Stan_magazynowy (
    ID_stanu_magazynowego INTEGER PRIMARY KEY,
    ID_produktu INTEGER,
    Ilosc INTEGER,
    Min_ilosc INTEGER,
    Lokalizacja VARCHAR(20),
    Data_waznosci DATE
);
""")
 
# Tabele z drugiego diagramu (gabinet lekarski)
cursor.executescript("""
CREATE TABLE Pacjent (
    ID_pacjenta INTEGER PRIMARY KEY,
    Imie VARCHAR(50),
    Nazwisko VARCHAR(50),
    Pesel INT,
    Data_urodzenia DATE,
    Nr_tel VARCHAR(15),
    Email VARCHAR(100)
);
 
CREATE TABLE Adres (
    ID_adresu INTEGER PRIMARY KEY,
    ID_pacjenta INTEGER,
    Ulica VARCHAR(100),
    Miasto VARCHAR(100),
    Kod_pocztowy VARCHAR(6),
    Kraj INT
);
 
CREATE TABLE Specjalizacja (
    ID_specjalizacji INTEGER PRIMARY KEY,
    Nazwa VARCHAR(100),
    Opis VARCHAR(100)
);
 
CREATE TABLE Lekarz (
    ID_lekarza INTEGER PRIMARY KEY,
    ID_specjalizacji INTEGER,
    Imie VARCHAR(50),
    Nazwisko VARCHAR(50),
    Telefon VARCHAR(15),
    Email VARCHAR(100)
);
 
CREATE TABLE Wizyta (
    ID_wizyty INTEGER PRIMARY KEY,
    ID_pacjenta INTEGER,
    ID_lekarza INTEGER,
    Notatka VARCHAR(255),
    Data_wizyty DATE,
    Godzina_wizyty TIMESTAMP,
    Status VARCHAR(255),
    Nr_gabinetu INT
);
 
CREATE TABLE Platnosc (
    ID_platnosci INTEGER PRIMARY KEY,
    ID_wizyty INTEGER,
    Kwota DECIMAL(10,2),
    Sposob_platnosci VARCHAR(50),
    Data_platnosci DATE
);
""")
# Zatwierdzenie zmian i zamknięcie połączenia
conn.commit()
conn.close()