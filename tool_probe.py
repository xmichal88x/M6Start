      
from ___CONF import *
import sys
import time
import json

timezone = time.localtime() 

JSON_FILE = "narzedzia.json"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION to throw message in py status line and optionally end program 
# Args: message(string), action(boolean)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def throwMessage(message, action):

    ttime = time.strftime("%H:%M:%S", timezone)
    print("\n"  + ttime + " - " + message)

    if message == True: 
        
        msg.info("\n"  + ttime + " - " + message)

    if action == "exit":
        sys.exit(0)


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
    # print(f"Odczytano wejście: module_id={module_id}, pin={pin}, wartość={value}")
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

#-----------------------------------------------------------
# Lista programów
#-----------------------------------------------------------

def check_axes_referenced():
    axis_to_check = [Axis.X, Axis.Y, Axis.Z]
    not_referenced_axes = []  # Lista na niezreferowane osie

    for axis in axis_to_check:
        if not d.isAxisReferenced(axis):
            not_referenced_axes.append(axis)  # Dodajemy niezreferowaną oś

    # Jeśli są niezreferowane osie, zgłoś błąd
    if not_referenced_axes:
        msg_axes_referenced = f"🔴 Osi(e) {', '.join([str(axis) for axis in not_referenced_axes])} nie są zbazowane! Uruchom proces bazowania."
        throwMessage(msg_axes_referenced, "exit")

def curtain_up():
    """
    Podnosi szczotkę.
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

def activate_tool_change_position():
    """
    Aktywuje pozycję wymiany narzędzia.
    """
    print("Aktywuję pozycję wymiany narzędzia...")
    set_digital_output(OUT_TOOL_CHANGE_POS, True)
    time.sleep(0.25)
    print("Pozycja wymiany aktywowana.")

def deactivate_tool_change_position():
    """
    Dezaktywuje pozycję wymiany narzędzia.
    """
    print("Dezaktywuję pozycję wymiany narzędzia...")
    set_digital_output(OUT_TOOL_CHANGE_POS, False)
    time.sleep(0.25)
    print("Pozycja wymiany dezaktywowana.")




#############################################
# Macro START - Uruchomienie procedury pomiaru długości narzędzia
#############################################

#-----------------------------------------------------------
# Perform pre-checks
#-----------------------------------------------------------

# exit if axes not referenced
check_axes_referenced()

# Aktywuj pozycję wymiany
activate_tool_change_position()

# ignore softlimits
d.ignoreAllSoftLimits(True)
    
#ustaw_stan_procesu("Pomiar")

# Wyłącz wrzeciono
d.setSpindleState(SpindleState.OFF)

# Pobranie numeru narzędzia
toolNr = d.getSpindleToolNumber()
if toolNr == 0:
    sys.exit("Tool(0) has no tool length offset. Probing failed!")

# Pobranie aktualnej pozycji maszyny
machine_pos = d.getPosition(CoordMode.Machine)

# Podnieś szczotkę
curtain_up()

# Podniesienie osi Z do bezpiecznej wysokości
machine_pos[Z] = Z_SAFE
d.moveToPosition(CoordMode.Machine, machine_pos, FEED_PROBE_MOVE)

# Przejazd do pozycji startowej w osiach X i Y (jeśli włączone w ustawieniach)
if PROBE_MOVE_X:
    machine_pos[X] = PROBE_START_X
if PROBE_MOVE_Y:
    machine_pos[Y] = PROBE_START_Y
d.moveToPosition(CoordMode.Machine, machine_pos, FEED_PROBE_MOVE)

# Przejazd do pozycji startowej w osi Z
machine_pos[Z] = PROBE_START_Z
d.moveToPosition(CoordMode.Machine, machine_pos, FEED_PROBE_MOVE)

# Szybki pomiar długości narzędzia
machine_pos[Z] = PROBE_END_Z
probeResult = d.executeProbing(CoordMode.Machine, machine_pos, PROBE_INDEX, FEED_PROBE_FAST)

if not probeResult:
    sys.exit("Fast probing failed!")

# Pobranie pozycji zakończenia szybkiego pomiaru
machine_pos = d.getProbingPosition(CoordMode.Machine)
fast_probe_z = machine_pos[Z]  # Użycie spójnej zmiennej zamiast Axis.Z.value

# Podniesienie osi Z przed dokładnym pomiarem
d.moveAxisIncremental(Axis.Z, PROBE_LIFT_UP_DIST, FEED_PROBE_MOVE)
time.sleep(PROBE_FINE_DELAY)

# Dokładny (wolniejszy) pomiar długości narzędzia
probeResult = d.executeProbing(CoordMode.Machine, machine_pos, PROBE_INDEX, FEED_PROBE_SLOW)

if not probeResult:
    sys.exit("Slow probing failed!")

# Pobranie pozycji zakończenia dokładnego pomiaru
machine_pos = d.getProbingPosition(CoordMode.Machine)
fine_probe_z = machine_pos[Z]  # Użycie spójnej zmiennej

# Sprawdzenie różnicy między szybkim a dokładnym pomiarem
probeDiff = abs(fast_probe_z - fine_probe_z)
if PROBE_CHECK_DIFF and probeDiff > PROBE_MAX_DIFF:
    sys.exit(f"ERROR: fine probing difference limit exceeded! (diff: {probeDiff:.3f})")

# Obliczenie i zapisanie długości narzędzia
toolOffset = fine_probe_z - REF_TOOL_PROBE_POS
d.setToolLength(toolNr, toolOffset)

# Podniesienie osi Z do bezpiecznej wysokości
machine_pos[Z] = Z_SAFE
d.moveToPosition(CoordMode.Machine, machine_pos, FEED_PROBE_MOVE)

# przejedź do pozycji poza obaszarem wymiany narzędzia
machine_pos[Y] = 1550
d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)

# Dezaktywuje pozycję wymiany
deactivate_tool_change_position()

# Przywrócenie softlimitów
d.ignoreAllSoftLimits(False)
print("Softlimity przywrócone.")

# Zakończenie programu
print(f"Tool({toolNr}) offset set to: {toolOffset:.4f}")
#ustaw_stan_procesu(None)
