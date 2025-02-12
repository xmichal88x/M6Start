from ___CONF import *
import json
import time
import sys

JSON_FILE = "narzedzia.json"

def wczytaj_ustawienia():
    """Wczytuje ustawienia z JSON i konwertuje wartości na nazwy."""
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
        # Zamiana wartości 0/1 na nazwy trybu pracy
        for tool, params in data.items():
            params["tryb_pracy"] = TRYB_PRACY_MAP.get(params["tryb_pracy"], "Nieznany")
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def odczytaj_tryb_pracy(narzedzie):
    """Odczytuje tryb pracy dla podanego narzędzia z pliku JSON."""
    data = wczytaj_ustawienia()  # Wczytuje dane z pliku JSON

    # Sprawdza, czy narzędzie istnieje w danych
    if str(narzedzie) in data:
        tryb_pracy = data[str(narzedzie)]["tryb_pracy"]  # Pobiera tryb pracy
        return tryb_pracy
    else:
        messagebox.showerror("Błąd", f"Narzędzie {narzedzie} nie znaleziono w pliku JSON.")
        return None

# Funkcja odczytuje offset dla danego narzędzia z SimCNC
def odczytaj_offset(tool):
    return d.getToolLength(tool)

# Funkcja zapisuje nowy offset do tabeli narzędziowej SimCNC
def zapisz_offset(tool, offset):
    d.setToolLength(tool, offset)
    print(f"Zapisano nowy offset dla narzędzia T{tool}: {offset:.4f}")

# Funkcja sprawdza aktualny tryb pracy na podstawie czujnika agregatu
def sprawdz_aktualny_tryb():
    if get_digital_input(IN_AGGREGATE_UP):
        return "Góra"
    elif get_digital_input(IN_AGGREGATE_DOWN):
        return "Dół"
    return None

# Sprawdzenie narzędzia aktualnie zamontowanego we wrzecionie
toolNr = d.getSpindleToolNumber()
if toolNr == 0:
    print("Brak narzędzia w uchwycie. Pominięto zmianę offsetu.")
    sys.exit(0)

# Pobranie zapisanej konfiguracji narzędzia
zapisany_tryb = odczytaj_tryb_pracy(toolNr)
aktualny_tryb = sprawdz_aktualny_tryb()

if zapisany_tryb == aktualny_tryb:
    print("Tryb pracy nie uległ zmianie. Brak potrzeby aktualizacji offsetu.")
    sys.exit(0)

print(f"Wykryto zmianę trybu pracy narzędzia! {zapisany_tryb} -> {aktualny_tryb}")

# Pobranie offsetu wrzeciona dla nowego trybu
try:
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
    offset_wrzesiona_gora = data.get("0", {}).get("offset_gora", 0)
    offset_wrzesiona_dol = data.get("0", {}).get("offset_dol", 0)
except (FileNotFoundError, json.JSONDecodeError):
    print("Błąd odczytu pliku JSON! Użyto wartości domyślnych.")
    offset_wrzesiona_gora = 0
    offset_wrzesiona_dol = 0

offset_wrzesiona = offset_wrzesiona_gora if aktualny_tryb == "Góra" else offset_wrzesiona_dol
offset_narzedzia = odczytaj_offset(toolNr)

# Obliczenie nowego offsetu
offset_nowy = offset_narzedzia - offset_wrzesiona
print(f"Nowy obliczony offset: {offset_nowy:.4f}")

# Wyświetlenie komunikatu i decyzja użytkownika
wybor = input("Czy chcesz wykonać nowy pomiar? (T/N): ").strip().lower()
if wybor == "t":
    print("Uruchamiam pomiar długości narzędzia...")
    exec(open("tool_probe.py").read())
else:
    zapisz_offset(toolNr, offset_nowy)
    print("Offset został zapisany w tabeli narzędzi.")
