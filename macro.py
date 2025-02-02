from ___CONF import * 
import time   
import sys

timezone = time.localtime() 

mode = "debug" # normal or debug (for more info output)

#-----------------------------------------------------------
# Check status of pin 
#-----------------------------------------------------------

msg_air_warning         = "ERR - ATC - air pressure too low"
msg_clamp_error         = "ERR - ATC - Clamp could not be opened"
msg_clamp_error_close	= "ERR - ATC - Clamp could not be closed"
msg_spindle_error       = "ERR - ATC - Spindle still spinning" 
msg_old_equal_new       = "INF - ATC - New tool equal to old tool. M6 aborted"
msg_tool_out_range      = "ERR - ATC - Selected tool out of range"
msg_tool_unload_error   = "ERR - ATC - Could not unload tool"
msg_tool_load_error     = "ERR - ATC - Could not load tool" 
msg_ref_error           = "ERR - ATC - Axis not referenced"
msg_tool_zero           = "ERR - ATC - Tool zero cannot be called"
msg_tool_count          = "ERR - ATC - Tool number out of range"
msg_tool_special        = "ERR - ATC - Special tool, not available for auto tool change"
msg_tool_dropoff        = "OK - ATC - Old tool dropped off"
msg_m6_end              = "OK - ATC - M6 successful"
msg_noprobe             = "INFO - ATC - Tool probing aborted, tool number in exception list"
msg_unknow_tool         = "Nieznane narzędzie w uchwycie"
msg_magazine            = "Brak miejsca w magazynie narzędzi"
msg_axes_referenced     = "f"Oś {axis} nie jest zbazowana! Uruchom proces bazowania.""


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

#-----------------------------------------------------------
# Prep
#-----------------------------------------------------------

# Store some info for later use
tool_old_id     =  d.getSpindleToolNumber()
tool_new_id     =  d.getSelectedToolNumber()
tool_new_len    =  d.getToolLength(tool_new_id)
machine_pos     =  d.getPosition(CoordMode.Machine)


# if debug is enabled, output some helpful information
if mode == "debug":
    print(f"{tool_old_id}  -> {tool_new_id}")

#-----------------------------------------------------------
# Perform pre-checks
#-----------------------------------------------------------

# exit if axes not referenced
required_axes = [0, 1, 2]  # Sprawdzamy X, Y, Z
    for axis in required_axes:
        if not is_axis_referenced(axis):
            throwMessage(msg_axes_referenced, "exit")   

# exit if tool is in exception list for auto-tool-change 
if tool_new_id in conf_tools_special:
    throwMessage(msg_tool_special, "exit")   

# exit if air pressure is too low 
if getPinStatus(IN_PRESSURE) == False:  
    throwMessage(msg_air_warning, "exit")

# exit if tool is already in spindle
if tool_old_id == tool_new_id: 
    throwMessage(msg_old_equal_new, "exit")

# exit on tool zero
if tool_new_id == 0: 
    throwMessage(msg_tool_zero, "exit") 

# exit if tool is out of range
if tool_new_id > TOOLCOUNT:
    throwMessage(msg_tool_count, "exit") 	 

# exit if unknown tool in the holder
if tool_old_id == 0 and get_digital_input(IN_TOOLINSIDE):
    throwMessage("msg_unknow_tool, "exit")

#-----------------------------------------------------------
# Główna funkcja programu
#-----------------------------------------------------------

def main():

# ignore softlimits
d.ignoreAllSoftLimits(True)

# Spindle off
d.setSpindleState(SpindleState.OFF)

# Curtain up 
curtain_up()

# Aktywuj pozycję wymiany
activate_tool_change_position()

# Otwórz mgazyn narzędzi
open_magazine()

# move to safe Z 
machine_pos[Z] =  move_atc_z_safe
d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)

# if a tool is in spindle, go and drop that first
# if there is no tool in spindle, skip this part
if get_digital_input(IN_TOOL_INSIDE):
    # move to the toolholder
    # Obliczenie nowej pozycji na podstawie ToolOld
    machine_pos[X] = X_BASE + (X_TOOLOFFSET * (tool_old_id - 1))
    machine_pos[Y] = Y_FORSLIDE
    d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
    d.waitForMotionEnd()
    
    # Sprawdź, czy jest wolne miejsce w magazynie narzędziowym
    if not get_digital_input(IN_NarzedzieWMagazynie):
    throwMessage(msg_magazine, "exit")
    
    # opuść Agregat 1
    aggregate_down()
    machine_pos[Z] = Z_TOOLGET
    d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
    d.waitForMotionEnd()
    machine_pos[Y] = Y_LOCK
    d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
    d.waitForMotionEnd()
    
    # otwórz uchwyt
    open_collect()
    
    # czyszczenie stożka
    set_digital_output(OUT_CLEANCONE , True)
    machine_pos[Z] = Z_SAFE
    d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
    d.waitForMotionEnd()
    
    # close clamping and write message    
    set_digital_output(OUT_CLEANCONE, False)
    throwMessage(msg_tool_dropoff, "")
    
    

    




    
    
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
