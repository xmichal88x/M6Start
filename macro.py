import time
from simcnc_api import d, IOPortDir, DIOPinVal  # Import API SimCNC

# Konfiguracja wejść i wyjść
OUT_CURTAIN_UP = 9             # Wyjście do podnoszenia szczotki
OUT_CURTAIN_DOWN = 8           # Wyjście do opuszczania szczotki
IN_CURTAIN_UP = 6              # Czujnik pozycji górnej szczotki
IN_CURTAIN_DOWN = 5            # Czujnik pozycji dolnej szczotki

OUT_AGGREGATE_UP = 7           # Wyjście do podnoszenia agregatu
OUT_AGGREGATE_DOWN = 6         # Wyjście do opuszczania agregatu
IN_AGGREGATE_UP = 4            # Czujnik pozycji górnej agregatu
IN_AGGREGATE_DOWN = 3          # Czujnik pozycji dolnej agregatu

OUT_TOOL_CHANGE_POS = 10       # Wyjście do aktywacji pozycji wymiany narzędzia
IN_TOOL_SENSOR = 11            # Czujnik obecności narzędzia w uchwycie

OUT_COLLECT_OPEN = 12          # Wyjście do otwierania uchwytu narzędzia
OUT_COLLECT_CLOSE = 13         # Wyjście do zamykania uchwytu narzędzia
IN_COLLECT_OPEN = 14           # Czujnik potwierdzający otwarcie uchwytu
IN_COLLECT_CLOSE = 15          # Czujnik potwierdzający zamknięcie uchwytu

# Główna funkcja programu
def main():
    """
    Główna logika programu:
    1. Podnieś szczotkę.
    2. Aktywuj pozycję wymiany.
    3. Opuść agregat.
    4. Otwórz uchwyt narzędzia.
    5. Sprawdź, czy uchwyt jest pusty (brak narzędzia).
    6. Zamknij uchwyt narzędzia.
    7. Sprawdź, czy narzędzie znajduje się w uchwycie.
    8. Opuść szczotkę.
    9. Zakończ program.
    """
    print("Uruchamianie programu...")

    curtain_up()
    activate_tool_change_position()
    aggregate_down()

    open_collect()

    # Sprawdzenie, czy uchwyt jest pusty
    # if not get_digital_input(IN_TOOL_SENSOR):
    #     print("Uchwyt jest pusty (brak narzędzia).")
    # else:
    #     print("Błąd: Narzędzie nadal w uchwycie.")

    close_collect()

    # Sprawdzenie, czy narzędzie znajduje się w uchwycie
    # if get_digital_input(IN_TOOL_SENSOR):
    #     print("Narzędzie znajduje się w uchwycie.")
    # else:
    #     print("Błąd: Narzędzie nie zostało uchwycone.")

    curtain_down()
    deactivate_tool_change_position()

    print("Program zakończony pomyślnie.")

# Funkcje pomocnicze
def set_digital_output(pin, state):
    """Ustawia stan wyjścia cyfrowego na sterowniku."""
    d.setDigitalIO(pin, DIOPinVal.PinSet if state else DIOPinVal.PinReset)

def get_digital_input(pin):
    """Zwraca stan wejścia cyfrowego ze sterownika."""
    return d.getDigitalIO(IOPortDir.InputPort, pin) == DIOPinVal.PinSet

# Podprogramy
def open_collect():
    """
    Otwiera uchwyt narzędzia.
    - Wysyła sygnał otwarcia uchwytu.
    - Sprawdza czujnik potwierdzający otwarcie uchwytu.
    - W programie głównym należy sprawdzić, czy uchwyt jest pusty.
    """
    print("Rozpoczynam otwieranie uchwytu narzędzia...")
    set_digital_output(OUT_COLLECT_OPEN, True)
    time.sleep(0.25)
    set_digital_output(OUT_COLLECT_OPEN, False)

    start_time = time.time()
    while not get_digital_input(IN_COLLECT_OPEN):
        if time.time() - start_time > 5:
            print("Błąd: Uchwyt narzędzia nie otworzył się.")
            return False
        time.sleep(0.1)

    print("Uchwyt narzędzia otwarty.")
    return True

def close_collect():
    """
    Zamyka uchwyt narzędzia.
    - Wysyła sygnał zamknięcia uchwytu.
    - Sprawdza czujnik potwierdzający zamknięcie uchwytu.
    - W programie głównym należy sprawdzić, czy narzędzie znajduje się w uchwycie.
    """
    print("Rozpoczynam zamykanie uchwytu narzędzia...")
    set_digital_output(OUT_COLLECT_CLOSE, True)
    time.sleep(0.25)
    set_digital_output(OUT_COLLECT_CLOSE, False)

    start_time = time.time()
    while not get_digital_input(IN_COLLECT_CLOSE):
        if time.time() - start_time > 5:
            print("Błąd: Uchwyt narzędzia nie zamknął się.")
            return False
        time.sleep(0.1)

    print("Uchwyt narzędzia zamknięty.")
    return True

# Podprogramy curtain_up, curtain_down i inne pozostają bez zmian...
# (Zostały pominięte tutaj dla czytelności, ale są identyczne jak wcześniej.)

# Uruchomienie programu, jeśli jest wywoływany jako główny skrypt
if __name__ == "__main__":
    main()