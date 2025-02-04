#-----------------------------------------------------------
# Ports & Pins 
#-----------------------------------------------------------

# Sekcja wyjść (sterowanie)
OUT_HV_ENABLE = 0              # HV Enable (K814)
OUT_RESET = 1                  # Wyjście reset
OUT_TOOL_CHANGE_POS = 2        # Wyjście do aktywacji pozycji wymiany narzędzia
OUT_ENABLE = 3                 # Enable, Hamulec osi Z
OUT_MAGAZINE_OPEN = 4          # Wyjście do otwierania magazynu
OUT_MAGAZINE_CLOSE = 5         # Wyjście do zamykania magazynu
OUT_AGGREGATE_DOWN = 6         # Wyjście do opuszczania agregatu
OUT_AGGREGATE_UP = 7           # Wyjście do podnoszenia agregatu
OUT_CURTAIN_DOWN = 8           # Wyjście do opuszczania szczotki
OUT_CURTAIN_UP = 9             # Wyjście do podnoszenia szczotki
OUT_COLLET_OPEN = 10           # Wyjście do otwierania uchwytu narzędzia
OUT_COLLET_CLOSE = 11          # Wyjście do zamykania uchwytu narzędzia
OUT_CLEANCONE = 12             # Czyszczenie stożka

# Sekcja wejść (czujniki)
IN_COLLET_OPEN = 13            # Czujnik otwarcia uchwytu narzędzia 1==True
IN_TOOL_INSIDE = 12            # Czujnik obecności narzędzia w uchwycie 1==True
IN_CURTAIN_UP = 6              # Czujnik górnej pozycji szczotki
IN_CURTAIN_DOWN = 5            # Czujnik dolnej pozycji szczotki
IN_Oslona_Pion_Open = 7        # Czujnik otwarcia osłony pionowej
IN_Oslona_Pion_Close = 8       # Czujnik zamknięcia osłony pionowej
IN_Oslona_Poz_Open = 9         # Czujnik otwarcia osłony poziomej
IN_Oslona_Poz_Close = 11       # Czujnik zamknięcia osłony poziomej
IN_AGGREGATE_UP = 3            # Czujnik górnej pozycji agregatu A1
IN_AGGREGATE_DOWN = 4          # Czujnik dolnej pozycji agregatu A1
IN_Narzedzie_W_Magazynie = 14  # Czujnik obecności narzędzia w magazynie
IN_PRESSURE = 999              # Czujnik ciśnienia (active when ok)

#-----------------------------------------------------------
# External Module 0
#-----------------------------------------------------------

# WYJŚCIA 
OUT_SECTION_1 = 0                # Wyjście Sekcji 1
OUT_SECTION_2 = 1                # Wyjście Sekcji 2
OUT_SECTION_3 = 2                # Wyjście Sekcji 3
OUT_SECTION_4 = 3                # Wyjście Sekcji 4

# WEJŚCIA
IN_SECTION_1 = 0                # Przycisk Sekcji 1
IN_SECTION_2 = 1                # Przycisk Sekcji 2
IN_SECTION_3 = 2                # Przycisk Sekcji 3
IN_SECTION_4 = 3                # Przycisk Sekcji 4
#-----------------------------------------------------------
#  Deklaracja zmiennych globalnych
#-----------------------------------------------------------

Z_TOOLGET = -88           # Z pozycja (absolutna) pobierania/zwalniania narzędzia
Z_LIFT = 10               # Odległość unoszenia do czyszczenia stożka
Z_SAFE = -10              # Bezpieczna Z do poruszania się nad uchwytami narzędzi
Y_FORSLIDE = 1764.8       # Y pozycja przed wsunięciem narzędzia do uchwytu
Y_LOCK = 1914.8           # Y pozycja do blokowania narzędzia w uchwycie
X_BASE = 436.55           # X pozycja pierwszego narzędzia
X_TOOLOFFSET = 143.0      # Odległość między narzędziami
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
