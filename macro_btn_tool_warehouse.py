from ___CONF import *
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION to GET status of IO pin
# Args: pin_in(int)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_digital_input(pin_tuple):
    """Odczytuje stan wejścia cyfrowego z odpowiedniego modułu."""
    module_id, pin, module_type = pin_tuple

    # Wybór odpowiedniego modułu
    if module_type == "IP":
        csmio = d.getModule(ModuleType.IP, module_id)
    elif module_type == "IO":
        csmio = d.getModule(ModuleType.IO, module_id)
    else:
        print(f"Błąd: Nieznany typ modułu {module_type}")
        return None

    if pin is None:
        print("Błąd: Pin nie został podany.")
        return None

    value = csmio.getDigitalIO(IOPortDir.InputPort, pin) == DIOPinVal.PinSet
    #print(f"Odczytano wejście: module_id={module_id}, pin={pin}, wartość={value}")
    return value

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION to SET status of IO pin
# Args: pin_out(int), state(boolean)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def set_digital_output(pin_tuple, state):
    """Ustawia stan wyjścia cyfrowego w odpowiednim module."""
    module_id, pin, module_type = pin_tuple  # Rozpakowanie wartości
    state2 = DIOPinVal.PinSet if state else DIOPinVal.PinReset

    # Wybór odpowiedniego modułu
    if module_type == "IP":
        csmio = d.getModule(ModuleType.IP, module_id)
    elif module_type == "IO":
        csmio = d.getModule(ModuleType.IO, module_id)
    else:
        print(f"Błąd: Nieznany typ modułu {module_type}")
        return None

    if pin is None:
        print("Błąd: Pin nie został podany.")
        return None
    
    try:
        csmio.setDigitalIO(pin, state2)
    except NameError as e:
        print(f"Błąd: Digital Output został błędnie zdefiniowany. Szczegóły: {e}")

def open_magazine():
    """
    Otwiera magazyn narzędzi.
    - Otwiera osłonę pionową i poziomą.
    - Sprawdza czujniki otwarcia osłon.
    """
    # Otwórz osłonę pionową i poziomą
    print("Otwieram magazyn...")
    set_digital_output(OUT_MAGAZINE_OPEN, True)
    time.sleep(0.25)
    set_digital_output(OUT_MAGAZINE_OPEN, False)
    
    # Sprawdź osłonę pionową
    start_time = time.time()
    while not get_digital_input(IN_Oslona_Pion_Open):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pionowa nie otworzyła się.")
            return False
        time.sleep(0.1)

    # Sprawdź osłonę poziomą
    start_time = time.time()
    while not get_digital_input(IN_Oslona_Poz_Open):
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
    print("Zamykanie magazynu...")

    # Zamknij osłonę poziomą
    set_digital_output(OUT_MAGAZINE_CLOSE, True)
    time.sleep(0.25)
    set_digital_output(OUT_MAGAZINE_CLOSE, False)

    # Sprawdź osłonę poziomą
    start_time = time.time()
    while not get_digital_input(IN_Oslona_Poz_Close):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pozioma nie zamknęła się.")
            return False
        time.sleep(0.1)

    # Sprawdź osłonę pionową
    start_time = time.time()
    while not get_digital_input(IN_Oslona_Pion_Close):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pionowa nie zamknęła się.")
            return False
        time.sleep(0.1)

    print("Magazyn został zamknięty.")
    return True



def main():
    """Obsługuje otwieranie i zamykanie magazynu po naciśnięciu przycisku."""
    print("Uruchomiono obsługę magazynu.")

    last_button_state = False  # Poprzedni stan przycisku
    magazine_open = False  # Aktualny stan magazynu

    while True:
        button_state = get_digital_input(IN_btn_tools_warehouse)  # Odczyt przycisku

        if button_state and not last_button_state:  # Wykrycie zbocza narastającego
            if magazine_open:
                if close_magazine():  # Zamykanie magazynu
                    magazine_open = False
            else:
                if open_magazine():  # Otwieranie magazynu
                    magazine_open = True

        last_button_state = button_state  # Aktualizacja stanu przycisku
        time.sleep(0.1)  # Opóźnienie dla stabilności


if __name__ == "__main__":
    main()