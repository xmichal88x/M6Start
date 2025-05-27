from ___CONF import * 
import time   
import sys
import json

JSON_FILE = "narzedzia.json"

# Mapowanie wartości liczbowych na nazwy trybu pracy
TRYB_PRACY_MAP = {0: "Dół", 1: "Góra"}
TRYB_PRACY_REVERSE = {"Dół": 0, "Góra": 1}

timezone = time.localtime() 

mode = "normal" # normal or debug (for more info output)

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
def throwMessage(message, action):
    ttime = time.strftime("%H:%M:%S", timezone)    
    print("\n"  + ttime + " - " + message)

    if message == True: 
        
        msg.info("\n"  + ttime + " - " + message)

    if action == "exit":
        d.setTrajectoryPause(True)
        time.sleep(3.5)      
        sys.exit(0)

#-----------------------------------------------------------
# Prep
#-----------------------------------------------------------

# Store some info for later use
tool_old_id     =  d.getSpindleToolNumber()
tool_new_id     =  d.getSelectedToolNumber()
tool_new_length =  d.getToolLength(tool_new_id)
machine_pos     =  d.getPosition(CoordMode.Machine)
# spindle_speed =  d.getSpindleSpeed()
spindle_state   =  d.getSpindleState()
# tool_old_pocket_id  =  tool_old_id
# tool_new_pocket_id  =  tool_new_id


# warunek sprawdzania obecnosci narzędzia podczas pobierania
if check_tool == "nie"    # tak lub nie

# if debug is enabled, output some helpful information
if mode == "debug":        # normal or debug (for more info output)
    print(f"{tool_old_id}  -> {tool_new_id}")

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
# Operacje na json
#-----------------------------------------------------------

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
    if mode == "debug":
        print("Rozpoczynam podnoszenie szczotki...")
    set_digital_output(OUT_CURTAIN_UP, True)
    time.sleep(0.25)
    set_digital_output(OUT_CURTAIN_UP, False)

    start_time = time.time()
    while not get_digital_input(IN_CURTAIN_UP):
        if time.time() - start_time > 5:
            print("Błąd: Szczotka nie osiągnęła pozycji górnej.")
            d.stopTrajectory( )
            sys.exit(0)
            return False
        time.sleep(0.1)
    if mode == "debug":
        print("Szczotka podniesiona.")
    return True

def curtain_down():
    """
    Opuszcza szczotkę.
    - Sprawdza czujnik pozycji dolnej szczotki.
    """
    if mode == "debug":
        print("Rozpoczynam opuszczanie szczotki...")
    set_digital_output(OUT_CURTAIN_DOWN, True)
    time.sleep(0.25)
    set_digital_output(OUT_CURTAIN_DOWN, False)

    start_time = time.time()
    while not get_digital_input(IN_CURTAIN_DOWN):
        if time.time() - start_time > 5:
            print("Błąd: Szczotka nie osiągnęła pozycji dolnej.")
            d.stopTrajectory( )
            sys.exit(0)
            return False
        time.sleep(0.1)
    if mode == "debug":    
        print("Szczotka opuszczona.")
    return True

def aggregate_up():
    """
    Podnosi agregat.
    - Sprawdza czujnik pozycji górnej agregatu.
    """
    if mode == "debug":
        print("Rozpoczynam podnoszenie agregatu...")
    set_digital_output(OUT_AGGREGATE_UP, True)
    time.sleep(0.25)
    set_digital_output(OUT_AGGREGATE_UP, False)

    start_time = time.time()
    while not get_digital_input(IN_AGGREGATE_UP):
        if time.time() - start_time > 5:
            print("Błąd: Agregat nie osiągnął pozycji górnej.")
            d.stopTrajectory( )
            sys.exit(0)
            return False
        time.sleep(0.1)
    if mode == "debug":
        print("Agregat podniesiony.")
    return True


def aggregate_down():
    """
    Opuszcza agregat.
    - Sprawdza czujnik pozycji dolnej agregatu.
    """
    if mode == "debug":
        print("Rozpoczynam opuszczanie agregatu...")
    set_digital_output(OUT_AGGREGATE_DOWN, True)
    time.sleep(0.25)
    set_digital_output(OUT_AGGREGATE_DOWN, False)

    start_time = time.time()
    while not get_digital_input(IN_AGGREGATE_DOWN):
        if time.time() - start_time > 5:
            print("Błąd: Agregat nie osiągnął pozycji dolnej.")
            d.stopTrajectory( )
            sys.exit(0)
            return False
        time.sleep(0.1)
    if mode == "debug":
        print("Agregat opuszczony.")
    return True

def activate_tool_change_position():
    """
    Aktywuje pozycję wymiany narzędzia.
    """
    if mode == "debug":
        print("Aktywuję pozycję wymiany narzędzia...")
    set_digital_output(OUT_TOOL_CHANGE_POS, True)
    time.sleep(0.25)
    if mode == "debug":
        print("Pozycja wymiany aktywowana.")

def deactivate_tool_change_position():
    """
    Dezaktywuje pozycję wymiany narzędzia.
    """
    if mode == "debug":
        print("Dezaktywuję pozycję wymiany narzędzia...")
    set_digital_output(OUT_TOOL_CHANGE_POS, False)
    time.sleep(0.25)
    if mode == "debug":
        print("Pozycja wymiany dezaktywowana.")


def open_collet():
    """
    Otwiera uchwyt narzędzia.
    - Sprawdza czujnik potwierdzający otwarcie uchwytu.
    """
    if mode == "debug":
        print("Rozpoczynam otwieranie uchwytu narzędzia...")
    set_digital_output(OUT_COLLET_OPEN, True)
    time.sleep(0.25)
    set_digital_output(OUT_COLLET_OPEN, False)

    start_time = time.time()
    while not get_digital_input(IN_COLLET_OPEN):
        if time.time() - start_time > 5:
            print("Błąd: Uchwyt narzędzia nie otworzył się.")
            throwMessage(msg_clamp_error, "exit")
            return False
        time.sleep(0.1)
    if mode == "debug":
        print("Uchwyt narzędzia otwarty.")
    return True

def close_collet():
    """
    Zamyka uchwyt narzędzia.
    - Sprawdza czujnik potwierdzający zamknięcie uchwytu.
    """
    if mode == "debug":
        print("Rozpoczynam zamykanie uchwytu narzędzia...")
    set_digital_output(OUT_COLLET_CLOSE, True)
    time.sleep(0.25)
    set_digital_output(OUT_COLLET_CLOSE, False)

    start_time = time.time()
    while get_digital_input(IN_COLLET_OPEN):
        if time.time() - start_time > 5:
            print("Błąd: Uchwyt narzędzia nie zamknął się.")
            throwMessage(msg_clamp_error_close, "exit")
            return False
        time.sleep(0.1)
    if mode == "debug":
        print("Uchwyt narzędzia zamknięty.")
    return True

def open_magazine():
    """
    Otwiera magazyn narzędzi.
    - Otwiera osłonę pionową i poziomą.
    - Sprawdza czujniki otwarcia osłon.
    """
    # Otwórz osłonę pionową i poziomą
    if mode == "debug":
        print("Otwieram magazyn...")
    set_digital_output(OUT_MAGAZINE_OPEN, True)
    time.sleep(0.25)
    set_digital_output(OUT_MAGAZINE_OPEN, False)
    
    # Sprawdź osłonę pionową
    start_time = time.time()
    while not get_digital_input(IN_Oslona_Pion_Open):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pionowa nie otworzyła się.")
            d.stopTrajectory( )
            sys.exit(0)
            return False
        time.sleep(0.1)

    # Sprawdź osłonę poziomą
    start_time = time.time()
    while not get_digital_input(IN_Oslona_Poz_Open):
        if time.time() - start_time > 5:
            print("Błąd: Osłona pozioma nie otworzyła się.")
            d.stopTrajectory( )
            sys.exit(0)
            return False
        time.sleep(0.1)
    if mode == "debug":
        print("Magazyn został otwarty.")
    return True

def close_magazine():
    """
    Zamyka magazyn narzędzi.
    - Zamykana jest osłona pionowa i pozioma.
    - Sprawdza czujniki zamknięcia osłon.
    """
    if mode == "debug":
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
    if mode == "debug":
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
    
    # Odczytaj z json
    tool_old_pocket_id = odczytaj_kieszen(tool_old_id)               # Odczytaj kieszeń dla starego narzędzia
    if tool_old_pocket_id is not None:
         print(f"Numer kieszeni dla  T{tool_old_id}: {tool_old_pocket_id}")
        
    tool_new_pocket_id = odczytaj_kieszen(tool_new_id)               # Odczytaj kieszeń dla nowego narzędzia
    if tool_new_pocket_id is not None:
         print(f"Numer kieszeni dla  T{tool_new_id}: {tool_new_pocket_id}")
        
    tryb_pracy = odczytaj_tryb_pracy(tool_new_id)                    # Odczytaj Tryb pracy nowego narzędzia
    
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
        throwMessage(msg_old_equal_new, "")
        sys.exit(0)
    
    # exit on tool zero
    if tool_new_id == 0: 
        throwMessage(msg_tool_zero, "exit") 
    
    # exit if tool is out of range
    if tool_new_pocket_id > TOOLCOUNT:
        throwMessage(msg_tool_count, "exit") 	 
    
    # exit if unknown tool in the holder
    if tool_old_id == 0 and get_digital_input(IN_TOOL_INSIDE):
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
    
    # Opuść Agregat
    aggregate_down()
    
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

            # Obliczenie pozycji narzędzia
            tool_pos_x = X_BASE + (X_TOOLOFFSET * (tool_old_pocket_id - 1))

            # Określenie czujnika i pozycji sprawdzającej
            if tool_old_pocket_id <= 10:
                # Lewy czujnik (pozycja +2.5 offsetu od X_BASE)
                check_sensor_input = IN_Narzedzie_W_Magazynie
                sensor_pos_x = tool_pos_x + (2.5 * X_TOOLOFFSET)
            else:
                # Prawy czujnik (pozycja -2.5 offsetu od X_BASE)
                check_sensor_input = IN_Narzedzie_W_Magazynie_2
                sensor_pos_x = tool_pos_x - (2.5 * X_TOOLOFFSET)
            
            # Podjazd do pozycji czujnika
            machine_pos[X] = sensor_pos_x
            machine_pos[Y] = Y_FORSLIDE
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
            
            # Sprawdzenie, czy narzędzie jest obecne
            if not get_digital_input(check_sensor_input):
                throwMessage(msg_magazine, "exit")
            
            # Podjedź do pozycji narzędzia
            machine_pos[X] = tool_pos_x
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)            

            # opuść Agregat
            aggregate_down()
            
            machine_pos[Z] = Z_TOOLGET
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
            machine_pos[Y] = Y_LOCK
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
                        
            # otwórz uchwyt
            open_collet()

            # exit is collet not open
            if not open_collet():
                throwMessage(msg_clamp_error, "exit")
            
            # załącz czyszczenie stożka
            set_digital_output(OUT_CLEANCONE , True)
    
            # odjedź na bezpieczną pozycję osi Z
            machine_pos[Z] = Z_SAFE
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
            
            # zamknij uchwyt, wyłącz czyszczenie stożka, podnieś agregat i wyświetl wiadomość
            close_collet()
            set_digital_output(OUT_CLEANCONE, False)
            # aggregate_up()    
            d.setSpindleToolNumber(0)
            throwMessage(msg_tool_dropoff, "")
    
    #-----------------------------------------------------------
    # Pobierz nowe narzędzie
    #-----------------------------------------------------------
    
    # if a number > 0 was selected
    if tool_new_id > 0:
        if get_digital_input(IN_TOOL_INSIDE):
            throwMessage(msg_tool_unload_error, "exit")
        
        # odjedź na bezpieczną pozycję osi Z
            machine_pos[Z] = Z_SAFE
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_z_fast)
            
        # Podnieś Agregat
        # aggregate_up()

        # Obliczenie pozycji narzędzia
        tool_pos_x = X_BASE + (X_TOOLOFFSET * (tool_new_pocket_id - 1))

        # sprawdz czy narzędzie jest obecne
        if check_tool == "tak"
            # Określenie czujnika i pozycji sprawdzającej
            if tool_new_pocket_id <= 10:
                # Lewy czujnik (pozycja +2.5 offsetu od X_BASE)
                check_sensor_input = IN_Narzedzie_W_Magazynie
                sensor_pos_x = tool_pos_x + (2.5 * X_TOOLOFFSET)
            else:
                # Prawy czujnik (pozycja -2.5 offsetu od X_BASE)
                check_sensor_input = IN_Narzedzie_W_Magazynie_2
                sensor_pos_x = tool_pos_x - (2.5 * X_TOOLOFFSET)
            
            # Podjazd do pozycji czujnika
            machine_pos[X] = sensor_pos_x
            machine_pos[Y] = Y_FORSLIDE
            d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
            
            # Sprawdzenie, czy narzędzie JEST obecne w magazynie
            if get_digital_input(check_sensor_input):
                throwMessage(msg_magazine_get, "exit")
        
        # Podjedź do pozycji nowego narzędzia
        machine_pos[Y] = Y_FORSLIDE
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
        machine_pos[X] = tool_pos_x
        machine_pos[Y] = Y_LOCK
        d.moveToPosition(CoordMode.Machine, machine_pos, feed_atc_xy)
        
        # Otwórz uchwyt
        open_collet()
        
        # exit is collet not open             
        if not open_collet():                 
            throwMessage(msg_clamp_error, "exit")()
    
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
    
        # przejedź do bezpiecznej pozycji Z poza magazyn
        machine_pos[Z] = Z_SAFE
        machine_pos[Y] = 1550
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

    # Ustaw tryb pracy dla narzędzia
    if tryb_pracy is not None:
        print(f"Tryb pracy dla narzędzia T{tool_new_id}: {tryb_pracy}")
    if tryb_pracy == "Góra":
        aggregate_up()
    elif tryb_pracy == "Dół":
        aggregate_down()
    
    # Zamknij mgazyn narzędzi
    close_magazine()
    
    # Przywrócenie softlimitów
    d.ignoreAllSoftLimits(False)
    print("Softlimity przywrócone.")
    throwMessage(msg_m6_end, "")
    
# Uruchomienie programu, jeśli jest wywoływany jako główny skrypt
if __name__ == "__main__":
    main()
