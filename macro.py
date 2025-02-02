from ___CONF import * 
import time   
import sys

timezone = time.localtime() 

mode = "debug" # normal or debug (for more info output)


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

    close_collect()

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
def curtain_up():
    """
    Podnosi szczotkę.
    - Wysyła sygnał do podnoszenia szczotki.
    - Sprawdza czujnik pozycji górnej szczotki.
    """
    print("Rozpoczynam podnoszenie szczotki...")
    set_digital_output(OUT_CURTAIN_UP, True)
    time.sleep(0.25)
    set_digital_output(OUT_CURTAIN_UP, False)

    start_time = time.time()
    while not get_digital_input(IN_CURTAIN_UP):
        if time.time() - start_time > 5:
            print("Błąd: Szczotka nie osiągnęła pozycji górnej.")
            return False
        time.sleep(0.1)
    print("Szczotka podniesiona.")
    return True

def curtain_down():
    """
    Opuszcza szczotkę.
    - Wysyła sygnał do opuszczania szczotki.
    - Sprawdza czujnik pozycji dolnej szczotki.
    """
    print("Rozpoczynam opuszczanie szczotki...")
    set_digital_output(OUT_CURTAIN_DOWN, True)
    time.sleep(0.25)
    set_digital_output(OUT_CURTAIN_DOWN, False)

    start_time = time.time()
    while not get_digital_input(IN_CURTAIN_DOWN):
        if time.time() - start_time > 5:
            print("Błąd: Szczotka nie osiągnęła pozycji dolnej.")
            return False
        time.sleep(0.1)
    print("Szczotka opuszczona.")
    return True

def aggregate_up():
    """
    Podnosi agregat.
    - Wysyła sygnał do podnoszenia agregatu.
    - Sprawdza czujnik pozycji górnej agregatu.
    """
    print("Rozpoczynam podnoszenie agregatu...")
    set_digital_output(OUT_AGGREGATE_UP, True)
    time.sleep(0.25)
    set_digital_output(OUT_AGGREGATE_UP, False)

    start_time = time.time()
    while not get_digital_input(IN_AGGREGATE_UP):
        if time.time() - start_time > 5:
            print("Błąd: Agregat nie osiągnął pozycji górnej.")
            return False
        time.sleep(0.1)
    print("Agregat podniesiony.")
    return True


def aggregate_down():
    """
    Opuszcza agregat.
    - Wysyła sygnał do opuszczania agregatu.
    - Sprawdza czujnik pozycji dolnej agregatu.
    """
    print("Rozpoczynam opuszczanie agregatu...")
    set_digital_output(OUT_AGGREGATE_DOWN, True)
    time.sleep(0.25)
    set_digital_output(OUT_AGGREGATE_DOWN, False)

    start_time = time.time()
    while not get_digital_input(IN_AGGREGATE_DOWN):
        if time.time() - start_time > 5:
            print("Błąd: Agregat nie osiągnął pozycji dolnej.")
            return False
        time.sleep(0.1)
    print("Agregat opuszczony.")
    return True

def activate_tool_change_position():
    """
    Aktywuje pozycję wymiany narzędzia.
    - Wysyła sygnał aktywujący pozycję wymiany narzędzia.
    """
    print("Aktywuję pozycję wymiany narzędzia...")
    set_digital_output(OUT_TOOL_CHANGE_POS, True)
    time.sleep(0.25)
    print("Pozycja wymiany aktywowana.")

def deactivate_tool_change_position():
    """
    Dezaktywuje pozycję wymiany narzędzia.
    - Wysyła sygnał dezaktywujący pozycję wymiany narzędzia.
    """
    print("Dezaktywuję pozycję wymiany narzędzia...")
    set_digital_output(OUT_TOOL_CHANGE_POS, False)
    time.sleep(0.25)
    print("Pozycja wymiany dezaktywowana.")


def open_collect():
    """
    Otwiera uchwyt narzędzia.
    - Wysyła sygnał otwarcia uchwytu.
    - Sprawdza czujnik potwierdzający otwarcie uchwytu.
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

def open_magazine():
    """
    Otwiera magazyn narzędzi.
    - Otwiera osłonę pionową i poziomą.
    - Sprawdza czujniki otwarcia osłon.
    """
    print("Rozpoczynam otwieranie magazynu...")

    # Otwórz osłonę pionową
    print("Otwieram osłonę pionową...")
    set_digital_output(OUT_MAGAZINE_OPEN, True)
    time.sleep(0.25)
    set_digital_output(OUT_MAGAZINE_OPEN, False)

    start_time = time.time()
    while not get_digital_input(IN_OslonaPionOpen):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pionowa nie otworzyła się.")
            return False
        time.sleep(0.1)

    # Otwórz osłonę poziomą
    print("Otwieram osłonę poziomą...")
    start_time = time.time()
    while not get_digital_input(IN_OslonaPozOpen):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pozioma nie otworzyła się.")
            return False
        time.sleep(0.1)

    print("Magazyn został otwarty.")
    return True


def close_magazine():
    """
    Zamyka magazyn narzędzi.
    - Zamykana jest osłona pionowa i pozioma.
    - Sprawdza czujniki zamknięcia osłon.
    """
    print("Rozpoczynam zamykanie magazynu...")

    # Zamknij osłonę poziomą
    print("Zamykam osłonę poziomą...")
    set_digital_output(OUT_MAGAZINE_CLOSE, True)
    time.sleep(0.25)
    set_digital_output(OUT_MAGAZINE_CLOSE, False)

    start_time = time.time()
    while not get_digital_input(IN_OslonaPozClose):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pozioma nie zamknęła się.")
            return False
        time.sleep(0.1)

    # Zamknij osłonę pionową
    print("Zamykam osłonę pionową...")
    start_time = time.time()
    while not get_digital_input(IN_OslonaPionClose):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pionowa nie zamknęła się.")
            return False
        time.sleep(0.1)

    print("Magazyn został zamknięty.")
    return True

# Uruchomienie programu, jeśli jest wywoływany jako główny skrypt
if __name__ == "__main__":
    main()
