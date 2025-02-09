import json

JSON_FILE = "narzedzia.json"

# Mapowanie wartości liczbowych na nazwy trybu pracy
TRYB_PRACY_MAP = {0: "Dół", 1: "Góra"}
TRYB_PRACY_REVERSE = {"Dół": 0, "Góra": 1}

tool_old_id     =  d.getSpindleToolNumber()
tool_old_pocket_id = tool_old_id

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

def zapisz_ustawienia(data):
    """Zamienia nazwy trybów na wartości 0/1 i zapisuje do JSON."""
    for tool, params in data.items():
        params["tryb_pracy"] = TRYB_PRACY_REVERSE.get(params["tryb_pracy"], 0)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def ustaw_tryb_pracy(tool, tryb):
    """Zapisuje nowy tryb pracy dla narzędzia."""
    data = wczytaj_ustawienia()
    if str(tool) in data:
        data[str(tool)]["tryb_pracy"] = tryb
    else:
        data[str(tool)] = {"tryb_pracy": tryb, "kieszen": 0}  # Domyślnie 0, jeśli brak danych
    zapisz_ustawienia(data)

def ustaw_kieszen(tool, kieszen):
    """Zapisuje numer kieszeni dla narzędzia."""
    data = wczytaj_ustawienia()
    if str(tool) in data:
        data[str(tool)]["kieszen"] = kieszen
    else:
        data[str(tool)] = {"tryb_pracy": "Dół", "kieszen": kieszen}  # Domyślny tryb pracy
    zapisz_ustawienia(data)

def odczytaj_kieszen(narzedzie):
    """Odczytuje numer kieszeni dla podanego narzędzia z pliku JSON."""
    data = wczytaj_ustawienia()  # Wczytuje dane z pliku JSON

    # Sprawdza, czy narzędzie istnieje w danych
    if str(narzedzie) in data:
        kieszen = data[str(narzedzie)]["kieszen"]  # Pobiera numer kieszeni
        return kieszen
    else:
        messagebox.showerror("Błąd", f"Narzędzie {narzedzie} nie znaleziono w pliku JSON.")
        return None


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

# Test - ustawienie wartości dla narzędzi
#ustaw_tryb_pracy(1, "Dół")
#ustaw_kieszen(2, 2)


kieszen = odczytaj_kieszen(tool_old_pocket_id)
if kieszen is not None:
    print(f"Numer kieszeni dla  T{tool_old_pocket_id}: {kieszen}")

#print(f"Numer narzędzia starego {tool_old_id}")

#tryb_pracy = odczytaj_tryb_pracy(narzedzie)
#if tryb_pracy is not None:
   # print(f"Tryb pracy dla narzędzia T{narzedzie}: {tryb_pracy}")



# Wypisanie zawartości JSON po zmianach
# print(wczytaj_ustawienia())
# print("Zaktualizowano parametry narzędzi")
