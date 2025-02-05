from ___CONF import * 
import time   
import sys

timezone = time.localtime() 

mode = "debug" # normal or debug (for more info output)

#-----------------------------------------------------------
# Check status of pin 
#-----------------------------------------------------------

msg_air_warning         = "🔴 ERR - ATC - air pressure too low"
msg_clamp_error         = "🔴 ERR - ATC - Clamp could not be opened"
msg_clamp_error_close	= "🔴 ERR - ATC - Clamp could not be closed"
msg_spindle_error       = "🔴 ERR - ATC - Spindle still spinning" 
msg_old_equal_new       = "ℹ️ ATC - New tool equal to old tool. M6 aborted"
msg_tool_out_range      = "🔴 ERR - ATC - Selected tool out of range"
msg_tool_unload_error   = "🔴 ERR - ATC - Could not unload tool"
msg_tool_load_error     = "🔴 ERR - ATC - Could not load tool" 
msg_ref_error           = "🔴 ERR - ATC - Axis not referenced"
msg_tool_zero           = "🔴 ERR - ATC - Tool zero cannot be called"
msg_tool_count          = "🔴 ERR - ATC - Tool number out of range"
msg_tool_special        = "🔴 ERR - ATC - Special tool, not available for auto tool change"
msg_tool_dropoff        = "✅ ATC - Old tool dropped off"
msg_m6_end              = "✅ ATC - M6 successful"
msg_noprobe             = "ℹ️ ATC - Tool probing aborted, tool number in exception list"
msg_unknow_tool         = "⚠️ Nieznane narzędzie w uchwycie"
msg_magazine            = "⚠️ Brak miejsca w magazynie narzędzi"
msg_magazine_get        = "⚠️ Brak narzędzia w magazynie narzędzi"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION to throw message in py status line and optionally end program 
# Args: message(string), action(boolean)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def throwMessage(message, action=None):

    ttime = time.strftime("%H:%M:%S", timezone)
    print("\n"  + ttime + " - " + message)
    
    msg.info("\n"  + ttime + " - " + message)  # To zawsze powinno działać

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
# spindle_speed   =  d.getSpindleSpeed()
spindle_state   =  d.getSpindleState()


# if debug is enabled, output some helpful information
if mode == "debug":
    print(f"{tool_old_id}  -> {tool_new_id}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION to GET status of IO pin
# Args: pin_in(int)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_digital_input(pin_tuple):
    """Odczytuje stan wejścia cyfrowego z odpowiedniego modułu."""
    module_id, pin = pin_tuple  # Rozpakowanie wartości
    
    # Sprawdzenie, czy to główny sterownik CSMIO-IP
    if module_id == MAIN_MODULE_ID:
        csmio = d.getModule(ModuleType.IP, module_id)
    else:  
        # Jeśli to dodatkowy moduł, użyj ModuleType.IO
        csmio = d.getModule(ModuleType.IO, module_id)

    if pin is None:
        return None

    return csmio.getDigitalIO(IOPortDir.InputPort, pin) == DIOPinVal.PinSet
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION to SET status of IO pin
# Args: pin_out(int), state(boolean)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def set_digital_output(pin_tuple, state):
    """Ustawia stan wyjścia cyfrowego w odpowiednim module."""
    module_id, pin = pin_tuple  # Rozpakowanie wartości
    state2 = DIOPinVal.PinSet if state else DIOPinVal.PinReset

    # Sprawdzenie, czy to główny sterownik CSMIO-IP
    if module_id == MAIN_MODULE_ID:
        csmio = d.getModule(ModuleType.IP, module_id)
    else:  
        # Jeśli to dodatkowy moduł, użyj ModuleType.IO
        csmio = d.getModule(ModuleType.IO, module_id)

    if pin is None:
        return None
    try:
        csmio.setDigitalIO(pin, state2)
    except NameError:
        print("------------------\nBłąd: Digital Output został błędnie zdefiniowany")

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

def aggregate_up():
    """
    Podnosi agregat.
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


def open_collet():
    """
    Otwiera uchwyt narzędzia.
    - Sprawdza czujnik potwierdzający otwarcie uchwytu.
    """
    print("Rozpoczynam otwieranie uchwytu narzędzia...")
    set_digital_output(OUT_COLLET_OPEN, True)
    time.sleep(0.25)
    set_digital_output(OUT_COLLET_OPEN, False)

    start_time = time.time()
    while not get_digital_input(IN_COLLET_OPEN):
        if time.time() - start_time > 5:
            print("Błąd: Uchwyt narzędzia nie otworzył się.")
            return False
        time.sleep(0.1)

    print("Uchwyt narzędzia otwarty.")
    return True

def close_collet():
    """
    Zamyka uchwyt narzędzia.
    - Sprawdza czujnik potwierdzający zamknięcie uchwytu.
    """
    print("Rozpoczynam zamykanie uchwytu narzędzia...")
    set_digital_output(OUT_COLLET_CLOSE, True)
    time.sleep(0.25)
    set_digital_output(OUT_COLLET_CLOSE, False)

    start_time = time.time()
    while get_digital_input(IN_COLLET_OPEN):
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

#-----------------------------------------------------------
#-----------------------------------------------------------
# M6 START
#-----------------------------------------------------------
#-----------------------------------------------------------

def main():
    
    #-----------------------------------------------------------
    # Perform pre-checks
    #-----------------------------------------------------------

    # exit if axes not referenced
    check_axes_referenced()
    
    # exit if tool is in exception list for auto-tool-change 
    if tool_new_id in conf_tools_special:
        throwMessage(msg_tool_special, "exit")   
    
    # exit if air pressure is too low 
    if not get_digital_input(IN_PRESSURE):  
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
        throwMessage(msg_unknow_tool, "exit")
    
    #-----------------------------------------------------------
    # Główna funkcja programu
    #-----------------------------------------------------------
    
    # ignore softlimits
    d.ignoreAllSoftLimits(True)
    
    # Spindle off
    d.setSpindleState(SpindleState.OFF)
    if spindle_state != SpindleState.OFF:
        throwMessage(msg_spindle_error, "exit")
    
    # Curtain up 
    curtain_up()
    
    # Aktywuj pozycję wymiany
    activate_tool_change_position()
    
    # Otwórz mgazyn narzędzi
    open_magazine()
    
    # move to safe Z 
    machine_pos[Z] = Z_SAFE
    d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
    
    #-----------------------------------------------------------
    # if a tool is in spindle, go and drop that first
    # if there is no tool in spindle, skip this part
    #-----------------------------------------------------------
    if tool_old_id > 0:
        if get_digital_input(IN_TOOL_INSIDE):
            # move to the toolholder
            # Obliczenie nowej pozycji na podstawie ToolOld
            machine_pos[X] = X_BASE + (X_TOOLOFFSET * (tool_old_id - 1))
            machine_pos[Y] = Y_FORSLIDE
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
            
            # Sprawdź, czy jest wolne miejsce w magazynie narzędziowym
            if not get_digital_input(IN_Narzedzie_W_Magazynie):
                throwMessage(msg_magazine, "exit")
            
            # opuść Agregat
            aggregate_down()
            
            machine_pos[Z] = Z_TOOLGET
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
            machine_pos[Y] = Y_LOCK
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
                        
            # otwórz uchwyt
            open_collet()
            
            # załącz czyszczenie stożka
            set_digital_output(OUT_CLEANCONE , True)
    
            # odjedź na bezpieczną pozycję osi Z
            machine_pos[Z] = Z_SAFE
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
            
            # zamknij uchwyt, wyłącz czyszczenie stożka, podnieś agregat i wyświetl wiadomość
            close_collet()
            set_digital_output(OUT_CLEANCONE, False)
            aggregate_up()    
            d.setSpindleToolNumber(0)
            throwMessage(msg_tool_dropoff, "")
    
    #-----------------------------------------------------------
    # Pobierz nowe narzędzie
    #-----------------------------------------------------------
    
    # if a number > 0 was selected
    if tool_new_id > 0:
        if get_digital_input(IN_TOOL_INSIDE):
            throwMessage(msg_tool_unload_error, "exit")
            
        # podnieś Agregat
        aggregate_up()
    
        # Sprawdź, czy narzędzie jest w magazynie narzędzi
        machine_pos[Y] = Y_FORSLIDE
        machine_pos[X] = X_BASE + (X_TOOLOFFSET * (tool_new_id - 1))
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
        
        if get_digital_input(IN_Narzedzie_W_Magazynie):
            throwMessage(msg_magazine_get, "exit")
    
        # przejedź do pozycji nowego narzędzia
        machine_pos[Y] = Y_LOCK
        machine_pos[X] = X_BASE + (X_TOOLOFFSET * (tool_new_id - 1))
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
    
        # otwórz uchwyt
        open_collet()
    
        # opuść Agregat
        aggregate_down()
    
        # załącz czyszczenie stożka
        set_digital_output(OUT_CLEANCONE , True)
        
        machine_pos[Z] = Z_TOOLGET + Z_LIFT
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
        machine_pos[Z] = Z_TOOLGET
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
        machine_pos[Z] = Z_TOOLGET + Z_LIFT
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
        machine_pos[Z] = Z_TOOLGET
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
        machine_pos[Z] = Z_TOOLGET + Z_LIFT
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
        machine_pos[Z] = Z_TOOLGET
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_final)
    
        # zamknij uchwyt i wyłącz czyszczenie stożka
        close_collet()
        set_digital_output(OUT_CLEANCONE, False)
        
        time.sleep(conf_pause_debounce)
    
        # exit if no tool was picked up 
        if not get_digital_input(IN_TOOL_INSIDE):
            throwMessage(msg_tool_load_error, "exit")
    
        # wyjedź poza uchwyt narzędzia
        machine_pos[Y] = Y_FORSLIDE
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
    
        # przejedź do bezpiecznej pozycji Z 
        machine_pos[Z] = Z_SAFE
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
    
    #-----------------------------------------------------------
    # Finish up and provide information to simCNC 
    #-----------------------------------------------------------
    
    # Set new tool in simCNC 
    d.setToolLength (tool_new_id, tool_new_length)
    d.setToolOffsetNumber(tool_new_id)
    d.setSpindleToolNumber(tool_new_id)

    # Dezaktywuje pozycję wymiany
    deactivate_tool_change_position()
    
    # Opuść szczotkę
    curtain_down()

    # Zamknij mgazyn narzędzi
    close_magazine()
    
    # Przywrócenie softlimitów
    d.ignoreAllSoftLimits(False)
    print("Softlimity przywrócone.")
    throwMessage(msg_m6_end, "")
    
# Uruchomienie programu, jeśli jest wywoływany jako główny skrypt
if __name__ == "__main__":
    main()
