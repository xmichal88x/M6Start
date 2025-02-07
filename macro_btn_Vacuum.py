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
    """Główna funkcja obsługująca przełączanie wyjść na podstawie przycisków."""
    print("Uruchomiono obsługę przycisków.")

    # Przechowuje poprzedni stan każdego przycisku
    last_button_states = {
        IN_SECTION_1: False,
        IN_SECTION_2: False,
        IN_SECTION_3: False,
        IN_SECTION_4: False
    }

    # Przechowuje aktualny stan każdego wyjścia
    output_states = {
        OUT_SECTION_1: get_digital_input(OUT_SECTION_1),
        OUT_SECTION_2: get_digital_input(OUT_SECTION_2),
        OUT_SECTION_3: get_digital_input(OUT_SECTION_3),
        OUT_SECTION_4: get_digital_input(OUT_SECTION_4)
    }

    # Mapa przypisania wejść do wyjść i nazw sekcji
    BUTTON_OUTPUT_MAP = {
        IN_SECTION_1: (OUT_SECTION_1, "Sekcja 1"),
        IN_SECTION_2: (OUT_SECTION_2, "Sekcja 2"),
        IN_SECTION_3: (OUT_SECTION_3, "Sekcja 3"),
        IN_SECTION_4: (OUT_SECTION_4, "Sekcja 4"),
    }

    while True:
        for input_pin, (output_pin, section_name) in BUTTON_OUTPUT_MAP.items():
            button_state = get_digital_input(input_pin)  # Odczyt stanu przycisku

            if button_state and not last_button_states[input_pin]:  # Wykrycie zbocza narastającego
                output_states[output_pin] = not output_states[output_pin]  # Odwrócenie stanu wyjścia
                set_digital_output(output_pin, output_states[output_pin])  # Ustawienie nowego stanu wyjścia

                # Komunikat o zmianie
                print(f"{section_name} {'ZAŁĄCZONA' if output_states[output_pin] else 'WYŁĄCZONA'}.")

            last_button_states[input_pin] = button_state  # Aktualizacja stanu przycisku
        
        time.sleep(0.1)  # Opóźnienie dla stabilności


if __name__ == "__main__":
    main()