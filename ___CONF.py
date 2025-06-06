# -----------------------------------------------------------
# Moduły sterowania
# -----------------------------------------------------------

MAIN_MODULE_TYPE  = "IP"    # Typ głównego sterownika
IO_MODULE_TYPE    = "IO"    # Typ dodatkowego modułu

MAIN_MODULE_ID    = 0  # Główny sterownik CSMIO-IP
IO_0_MODULE_ID    = 0  # Pierwszy dodatkowy moduł wejść/wyjść CSMIO-IO

# -----------------------------------------------------------
# IO CSMIO-IP (MAIN_MODULE_ID)
# -----------------------------------------------------------

# WYJŚCIA
OUT_HV_ENABLE = (MAIN_MODULE_ID, 0, MAIN_MODULE_TYPE)              # HV Enable (K814)
OUT_RESET = (MAIN_MODULE_ID, 1, MAIN_MODULE_TYPE)                  # Wyjście reset
OUT_TOOL_CHANGE_POS = (MAIN_MODULE_ID, 2, MAIN_MODULE_TYPE)        # Wyjście do aktywacji pozycji wymiany narzędzia
OUT_ENABLE = (MAIN_MODULE_ID, 3, MAIN_MODULE_TYPE)                 # Enable, Hamulec osi Z
OUT_MAGAZINE_OPEN = (MAIN_MODULE_ID, 4, MAIN_MODULE_TYPE)          # Wyjście do otwierania magazynu
OUT_MAGAZINE_CLOSE = (MAIN_MODULE_ID, 5, MAIN_MODULE_TYPE)         # Wyjście do zamykania magazynu
OUT_AGGREGATE_DOWN = (MAIN_MODULE_ID, 6, MAIN_MODULE_TYPE)         # Wyjście do opuszczania agregatu
OUT_AGGREGATE_UP = (MAIN_MODULE_ID, 7, MAIN_MODULE_TYPE)           # Wyjście do podnoszenia agregatu
OUT_CURTAIN_DOWN = (MAIN_MODULE_ID, 8, MAIN_MODULE_TYPE)           # Wyjście do opuszczania szczotki
OUT_CURTAIN_UP = (MAIN_MODULE_ID, 9, MAIN_MODULE_TYPE)             # Wyjście do podnoszenia szczotki
OUT_COLLET_OPEN = (MAIN_MODULE_ID, 10, MAIN_MODULE_TYPE)           # Wyjście do otwierania uchwytu narzędzia
OUT_COLLET_CLOSE = (MAIN_MODULE_ID, 11, MAIN_MODULE_TYPE)          # Wyjście do zamykania uchwytu narzędzia
OUT_CLEANCONE = (MAIN_MODULE_ID, 12, MAIN_MODULE_TYPE)             # Czyszczenie stożka
OUT_LAMP_OGOLNA = (MAIN_MODULE_ID, 13, MAIN_MODULE_TYPE)           # Kontrolka cykl pracy
OUT_LAMP_START = (MAIN_MODULE_ID, 14, MAIN_MODULE_TYPE)            # Kontrolka START
OUT_ODCIĄG = (MAIN_MODULE_ID, 15, MAIN_MODULE_TYPE)                # Odciąg wiórów

#WEJŚCIA
IN_AGGREGATE_UP = (MAIN_MODULE_ID, 3, MAIN_MODULE_TYPE)            # Czujnik górnej pozycji agregatu A1
IN_AGGREGATE_DOWN = (MAIN_MODULE_ID, 4, MAIN_MODULE_TYPE)          # Czujnik dolnej pozycji agregatu A1
IN_CURTAIN_DOWN = (MAIN_MODULE_ID, 5, MAIN_MODULE_TYPE)            # Czujnik dolnej pozycji szczotki
IN_CURTAIN_UP = (MAIN_MODULE_ID, 6, MAIN_MODULE_TYPE)              # Czujnik górnej pozycji szczotki
IN_Oslona_Pion_Open = (MAIN_MODULE_ID, 7, MAIN_MODULE_TYPE)        # Czujnik otwarcia osłony pionowej
IN_Oslona_Pion_Close = (MAIN_MODULE_ID, 8, MAIN_MODULE_TYPE)       # Czujnik zamknięcia osłony pionowej
IN_Oslona_Poz_Open = (MAIN_MODULE_ID, 9, MAIN_MODULE_TYPE)         # Czujnik otwarcia osłony poziomej
IN_Oslona_Poz_Close = (MAIN_MODULE_ID, 11, MAIN_MODULE_TYPE)       # Czujnik zamknięcia osłony poziomej
IN_COLLET_OPEN = (MAIN_MODULE_ID, 13, MAIN_MODULE_TYPE)            # Czujnik otwarcia uchwytu narzędzia 1==True
IN_TOOL_INSIDE = (MAIN_MODULE_ID, 12, MAIN_MODULE_TYPE)            # Czujnik obecności narzędzia w uchwycie 1==True
IN_Narzedzie_W_Magazynie = (MAIN_MODULE_ID, 14, MAIN_MODULE_TYPE)  # Czujnik obecności narzędzia w magazynie
IN_PRESSURE = (MAIN_MODULE_ID, 16, MAIN_MODULE_TYPE)               # Czujnik ciśnienia (active when ok)
IN_btn_tools_warehouse = (MAIN_MODULE_ID, 17, MAIN_MODULE_TYPE)    # Przycisk obsługi magazynu narzędzi
IN_btn_pauza = (MAIN_MODULE_ID, 18, MAIN_MODULE_TYPE)              # Przycisk PAUZA
IN_btn_start = (MAIN_MODULE_ID, 19, MAIN_MODULE_TYPE)              # Przycisk START

#-----------------------------------------------------------
# IO Module 0 (IO_0_MODULE_ID)
#-----------------------------------------------------------

# WYJŚCIA 
OUT_SECTION_1 = (IO_0_MODULE_ID, 0, IO_MODULE_TYPE)                # Wyjście Sekcji 1
OUT_SECTION_2 = (IO_0_MODULE_ID, 1, IO_MODULE_TYPE)                # Wyjście Sekcji 2
OUT_SECTION_3 = (IO_0_MODULE_ID, 2, IO_MODULE_TYPE)                # Wyjście Sekcji 3
OUT_SECTION_4 = (IO_0_MODULE_ID, 3, IO_MODULE_TYPE)                # Wyjście Sekcji 4

# WEJŚCIA
IN_SECTION_1 = (IO_0_MODULE_ID, 0, IO_MODULE_TYPE)                 # Przycisk Sekcji 1
IN_SECTION_2 = (IO_0_MODULE_ID, 1, IO_MODULE_TYPE)                 # Przycisk Sekcji 2
IN_SECTION_3 = (IO_0_MODULE_ID, 2, IO_MODULE_TYPE)                 # Przycisk Sekcji 3
IN_SECTION_4 = (IO_0_MODULE_ID, 3, IO_MODULE_TYPE)                 # Przycisk Sekcji 4
IN_btn_collet = (IO_0_MODULE_ID, 4, IO_MODULE_TYPE)                # Przycisk obsługi uchwytu narzędzia

#-----------------------------------------------------------
#  Deklaracja zmiennych globalnych
#-----------------------------------------------------------

Z_LIMIT_SAFE = -124.75    # Maszynowy limit stołu (bufor 1mm; Z0=125.75)

Z_TOOLGET = -91.5         # Z pozycja (absolutna) pobierania/zwalniania narzędzia
Z_LIFT = 10               # Odległość unoszenia do czyszczenia stożka
Z_SAFE = 20               # Bezpieczna Z do poruszania się nad uchwytami narzędzi
Y_FORSLIDE = 1710         # Y pozycja przed wsunięciem narzędzia do uchwytu
Y_LOCK = 1971             # Y pozycja do blokowania narzędzia w uchwycie
X_BASE = 317              # X pozycja pierwszego narzędzia (868)
X_TOOLOFFSET = 143.0      # Odległość między narzędziami (2575mm/18)
TOOLCOUNT = 8             # Maksymalna liczba narzędzi

feed_atc_z_final    = 800           # Z feed before reaching tool
feed_atc_z_fast     = 10000         # Z feed general
feed_atc_xy         = 10000         # XY feed in general 

# config
conf_atc_purge_time = 0.5           # purge time in sec
conf_tools_special  = {0}           # No automatic tool change 
conf_tools_noprobe  = {0,10}        # No automatic length probing 
conf_pause_debounce = 1           # debounce time for tool clamp close before checking sensor

#-----------------------------------------------------------
# Pomiar długości narzędzia
#-----------------------------------------------------------

PROBE_INDEX = 0            # Indeks czujnika pomiarowego (jeśli w systemie jest więcej niż jeden)

PROBE_START_X = 1534          # Pozycja startowa X dla pomiaru
PROBE_START_Y = 1640            # Pozycja startowa Y dla pomiaru
PROBE_START_Z = 10         # Pozycja startowa Z dla pomiaru 
PROBE_END_Z = -200         # Końcowa pozycja Z do pomiaru (najniższy punkt do którego sonda ma się obniżyć)
REF_TOOL_PROBE_POS = -80  # Pozycja pomiarowa dla narzędzia odniesienia (np. długość wzorcowego narzędzia)

FEED_PROBE_MOVE = 8000     # Prędkość przemieszczania się do punktu pomiarowego
FEED_PROBE_FAST = 800      # Prędkość szybkiego pomiaru
FEED_PROBE_SLOW = 100      # Prędkość dokładnego pomiaru

PROBE_LIFT_UP_DIST = 2     # Wysokość podniesienia osi Z przed dokładnym pomiarem
PROBE_FINE_DELAY = 0.2     # Opóźnienie przed dokładnym pomiarem (sekundy)
PROBE_CHECK_DIFF = False   # Czy sprawdzać różnicę między szybkim a dokładnym pomiarem?
PROBE_MAX_DIFF = 0.1       # Maksymalna różnica pomiarów

PROBE_MOVE_X = True        # Czy przemieszczać się w osi X do punktu startowego pomiaru?
PROBE_MOVE_Y = True        # Czy przemieszczać się w osi Y do punktu startowego pomiaru?

#-----------------------------------------------------------
# Axis allocation
#-----------------------------------------------------------

X = 0
Y = 1
Z = 2
A = 3
C = 5

#-----------------------------------------------------------
# Lista osi do sprawdzania bazowania
#-----------------------------------------------------------

# AXES_TO_CHECK = [X, Y, Z]
