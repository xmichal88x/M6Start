from ___CONF import *
import time


def toggle_output(input_pin, output_pin, section_name):
    """
    Funkcja zmieniająca stan wyjścia na przeciwny po naciśnięciu przycisku i wyświetlająca komunikat.
    :param input_pin: Krotka (moduł, pin) wejścia cyfrowego (przycisk)
    :param output_pin: Krotka (moduł, pin) wyjścia cyfrowego (które ma być przełączone)
    :param section_name: Nazwa sekcji dla komunikatu
    """
    if get_digital_input(input_pin):  # Sprawdzenie czy przycisk został wciśnięty
        current_state = get_digital_input(output_pin)  # Pobranie aktualnego stanu wyjścia
        new_state = not current_state  # Odwrócenie stanu
        set_digital_output(output_pin, new_state)  # Zmiana stanu na przeciwny
        
        # Wyświetlenie komunikatu
        if new_state:
            print(f"{section_name} ZAŁĄCZONA.")
        else:
            print(f"{section_name} WYŁĄCZONA.")


# **Mapa przypisania wejść do wyjść z nazwami sekcji**
BUTTON_OUTPUT_MAP = {
    IN_SECTION_1: (OUT_SECTION_1, "Sekcja 1"),
    IN_SECTION_2: (OUT_SECTION_2, "Sekcja 2"),
    IN_SECTION_3: (OUT_SECTION_3, "Sekcja 3"),
    IN_SECTION_4: (OUT_SECTION_4, "Sekcja 4"),
}


def main():
    """
    Główna pętla obsługi przycisków.
    """
    print("Uruchomiono obsługę przycisków.")
    while True:
        for input_pin, (output_pin, section_name) in BUTTON_OUTPUT_MAP.items():
            toggle_output(input_pin, output_pin, section_name)

        time.sleep(0.1)  # Ograniczenie odpytywania wejść


# Uruchomienie programu, jeśli plik jest uruchamiany jako skrypt
if __name__ == "__main__":
    main()