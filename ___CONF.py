# -----------------------------------------------------------
# Moduły sterowania
# -----------------------------------------------------------

MAIN_MODULE_ID = 0  # Główny sterownik CSMIO-IP
IO_MODULE_ID = 1  # Pierwszy dodatkowy moduł wejść/wyjść CSMIO-IO

# -----------------------------------------------------------
# IO CSMIO-IP - główny moduł
# -----------------------------------------------------------

# WYJŚCIA
OUT_HV_ENABLE = (MAIN_MODULE_ID, 0)              # HV Enable (K814)
OUT_RESET = (MAIN_MODULE_ID, 1)                  # Wyjście reset
OUT_TOOL_CHANGE_POS = (MAIN_MODULE_ID, 2)        # Wyjście do aktywacji pozycji wymiany narzędzia
OUT_ENABLE = (MAIN_MODULE_ID, 3)                 # Enable, Hamulec osi Z
OUT_MAGAZINE_OPEN = (MAIN_MODULE_ID, 4)          # Wyjście do otwierania magazynu
OUT_MAGAZINE_CLOSE = (MAIN_MODULE_ID, 5)         # Wyjście do zamykania magazynu
OUT_AGGREGATE_DOWN = (MAIN_MODULE_ID, 6)         # Wyjście do opuszczania agregatu
OUT_AGGREGATE_UP = (MAIN_MODULE_ID, 7)           # Wyjście do podnoszenia agregatu
OUT_CURTAIN_DOWN = (MAIN_MODULE_ID, 8)           # Wyjście do opuszczania szczotki
OUT_CURTAIN_UP = (MAIN_MODULE_ID, 9)             # Wyjście do podnoszenia szczotki
OUT_COLLET_OPEN = (MAIN_MODULE_ID, 10)           # Wyjście do otwierania uchwytu narzędzia
OUT_COLLET_CLOSE = (MAIN_MODULE_ID, 11)          # Wyjście do zamykania uchwytu narzędzia
OUT_CLEANCONE = (MAIN_MODULE_ID, 12)             # Czyszczenie stożka

# WEJŚCIA
IN_COLLET_OPEN = (MAIN_MODULE_ID, 13)            # Czujnik otwarcia uchwytu narzędzia 1==True
IN_TOOL_INSIDE = (MAIN_MODULE_ID, 12)            # Czujnik obecności narzędzia w uchwycie 1==True
IN_CURTAIN_UP = (MAIN_MODULE_ID, 6)              # Czujnik górnej pozycji szczotki
IN_CURTAIN_DOWN = (MAIN_MODULE_ID, 5)            # Czujnik dolnej pozycji szczotki
IN_Oslona_Pion_Open = (MAIN_MODULE_ID, 7)        # Czujnik otwarcia osłony pionowej
IN_Oslona_Pion_Close = (MAIN_MODULE_ID, 8)       # Czujnik zamknięcia osłony pionowej
IN_Oslona_Poz_Open = (MAIN_MODULE_ID, 9)         # Czujnik otwarcia osłony poziomej
IN_Oslona_Poz_Close = (MAIN_MODULE_ID, 11)       # Czujnik zamknięcia osłony poziomej
IN_AGGREGATE_UP = (MAIN_MODULE_ID, 3)            # Czujnik górnej pozycji agregatu A1
IN_AGGREGATE_DOWN = (MAIN_MODULE_ID, 4)          # Czujnik dolnej pozycji agregatu A1
IN_Narzedzie_W_Magazynie = (MAIN_MODULE_ID, 14)  # Czujnik obecności narzędzia w magazynie
IN_PRESSURE = (MAIN_MODULE_ID, 16)               # Czujnik ciśnienia (active when ok)

#-----------------------------------------------------------
# IO Module 0
#-----------------------------------------------------------

# WYJŚCIA 
OUT_SECTION_1 = (IO_MODULE_ID, 0)                # Wyjście Sekcji 1
OUT_SECTION_2 = (IO_MODULE_ID, 1)                # Wyjście Sekcji 2
OUT_SECTION_3 = (IO_MODULE_ID, 2)                # Wyjście Sekcji 3
OUT_SECTION_4 = (IO_MODULE_ID, 3)                # Wyjście Sekcji 4

# WEJŚCIA
IN_SECTION_1 = (IO_MODULE_ID, 0)                 # Przycisk Sekcji 1
IN_SECTION_2 = (IO_MODULE_ID, 1)                 # Przycisk Sekcji 2
IN_SECTION_3 = (IO_MODULE_ID, 2)                 # Przycisk Sekcji 3
IN_SECTION_4 = (IO_MODULE_ID, 3)                 # Przycisk Sekcji 4

#-----------------------------------------------------------
#  Deklaracja zmiennych globalnych
#-----------------------------------------------------------

Z_TOOLGET = -95           # Z pozycja (absolutna) pobierania/zwalniania narzędzia
Z_LIFT = 10               # Odległość unoszenia do czyszczenia stożka
Z_SAFE = -10              # Bezpieczna Z do poruszania się nad uchwytami narzędzi
Y_FORSLIDE = 1675         # Y pozycja przed wsunięciem narzędzia do uchwytu
Y_LOCK = 1915             # Y pozycja do blokowania narzędzia w uchwycie
X_BASE = 458              # X pozycja pierwszego narzędzia
X_TOOLOFFSET = 143.0      # Odległość między narzędziami (2575mm/18)
TOOLCOUNT = 6             # Maksymalna liczba narzędzi

feed_atc_z_final    = 800           # Z feed before reaching tool
feed_atc_z_fast     = 2500          # Z feed general
feed_atc_xy         = 2500          # XY feed in general 

# config
conf_atc_purge_time = 0.5           # purge time in sec
conf_tools_special  = {0}           # No automatic tool change 
conf_tools_noprobe  = {0,10}        # No automatic length probing 
conf_pause_debounce = 0.5           # debounce time for tool clamp close before checking sensor

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
