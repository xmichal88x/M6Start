#-----------------------------------------------------------
# Ports & Pins 
#-----------------------------------------------------------

# Sekcja wyjść (sterowanie)
OUT_HV_ENABLE = 0              # HV Enable (K814)
OUT_RESET = 1                  # Wyjście reset
OUT_CURTAIN_UP = 9             # Wyjście do podnoszenia szczotki
OUT_CURTAIN_DOWN = 8           # Wyjście do opuszczania szczotki
OUT_AGGREGATE_UP = 7           # Wyjście do podnoszenia agregatu
OUT_CLEANCONE = 12             # Czyszczenie stożka
OUT_AGGREGATE_DOWN = 6         # Wyjście do opuszczania agregatu
OUT_TOOL_CHANGE_POS = 2        # Wyjście do aktywacji pozycji wymiany narzędzia
OUT_COLLECT_OPEN = 10          # Wyjście do otwierania uchwytu narzędzia
OUT_COLLECT_CLOSE = 11         # Wyjście do zamykania uchwytu narzędzia
OUT_MAGAZINE_OPEN = 4          # Wyjście do otwierania magazynu
OUT_MAGAZINE_CLOSE = 5         # Wyjście do zamykania magazynu

# Sekcja wejść (czujniki)
IN_COLLET_OPENED = 13          # Czujnik otwarcia uchwytu narzędzia
IN_TOOL_INSIDE = 12            # Czujnik obecności narzędzia w uchwycie
IN_SzczotkaUp = 6              # Czujnik górnej pozycji szczotki
IN_SzczotkaDown = 5            # Czujnik dolnej pozycji szczotki
IN_OslonaPionOpen = 7          # Czujnik otwarcia osłony pionowej
IN_OslonaPionClose = 8         # Czujnik zamknięcia osłony pionowej
IN_OslonaPozOpen = 9           # Czujnik otwarcia osłony poziomej
IN_OslonaPozClose = 11         # Czujnik zamknięcia osłony poziomej
IN_AGREGAT1_UP = 3             # Czujnik górnej pozycji agregatu A1
IN_AGREGAT1_Down = 4           # Czujnik dolnej pozycji agregatu A1
IN_NarzedzieWMagazynie = 14    # Czujnik obecności narzędzia w magazynie
IN_PRESSURE = 999                # Czujnik ciśnienia (active when ok)


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
