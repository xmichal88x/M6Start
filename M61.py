# --------------------------------------------------------------------------

import time
from ___CONF import *  # Użyjemy stałych i funkcji zgodnych z resztą projektu

# Parametry bezpieczeństwa
Z_LIMIT_SAFE = -210  # Pozycja Z stołu w układzie maszynowym (z buforem bezpieczeństwa)

# --------------------------------------------------------------------------

# Funkcja: Sprawdzenie bezpieczeństwa Z=0 względem stołu

def check_z_zero_safe():
    machine_z = d.getPosition(CoordMode.Machine)[Z]                    # Aktualna pozycja Z w układzie maszynowym
    work_z_zero = d.getWorkOffset(d.getWorkOffsetNumber())[Z]          # Offset roboczy Z (np. G54)
    tool_length = d.getToolLength(d.getSpindleToolNumber())            # Długość aktualnego narzędzia

    # Pozycja fizyczna wrzeciona przy Z=0 (uwzględnia długość narzędzia i offset)
    z_real = machine_z - work_z_zero + tool_length

    if z_real < Z_LIMIT_SAFE:
        msg.err(f"❗ Niebezpieczna pozycja Z=0! ({z_real:.2f} mm poniżej limitu stołu)")
        d.stopTrajectory()
        sys.exit(0)
    else:
        print(f"✅ Z=0 bezpieczne: {z_real:.2f} mm nad limitem {Z_LIMIT_SAFE}")


# --------------------------------------------------------------------------

print("Sprawdzanie bezpieczeństwa Z=0...")
check_z_zero_safe()
