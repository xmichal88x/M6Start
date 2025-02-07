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


def main():
    """Główna funkcja sprawdzająca stan wejścia i ustawiająca wyjście."""
    print("Uruchomiono obsługę uchwytu.")

    action_performed = False  # Zmienna śledząca, czy akcja została wykonana
    first_press_detected = False  # Zmienna do wykrycia pierwszego naciśnięcia przycisku

    action_performed = False  # Zmienna śledząca, czy akcja została wykonana
    first_press_detected = False  # Zmienna do wykrycia pierwszego naciśnięcia przycisku

    while True:
        if get_digital_input(IN_btn_collet):  # Jeśli przycisk jest wciśnięty (stan wysoki)
            set_digital_output(OUT_COLLET_OPEN, True)  # Ustaw wyjście na stan wysoki (otwarte)
            action_performed = False  # Resetuj akcję, jeśli przycisk jest wciśnięty
            first_press_detected = True  # Zarejestruj, że przycisk został wciśnięty po raz pierwszy
        else:  # Jeśli przycisk nie jest wciśnięty (stan niski)
            if first_press_detected and not action_performed:  # Sprawdź, czy przycisk był już wciśnięty
                set_digital_output(OUT_COLLET_OPEN, False)  # Wyłącz otwarcie
                time.sleep(0.5)
                set_digital_output(OUT_COLLET_CLOSE, True)  # Włącz zamknięcie
                time.sleep(0.25)  # Czekaj 0.25 sekundy
                set_digital_output(OUT_COLLET_CLOSE, False)  # Wyłącz zamknięcie
                action_performed = True  # Oznacz, że akcja została wykonana

        time.sleep(0.1)  # Krótka przerwa, aby nie obciążać CPU

if __name__ == "__main__":
    main()
