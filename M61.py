import time
import sys
from ___CONF import *

Z_LIMIT_SAFE = -210  # Twardy limit – poziom stołu maszyny w maszynowych współrzędnych

def check_z_zero_safe():
    try:
        pos = d.getPosition(CoordMode.Machine)
        machine_z = pos[Z]

        work_offset = d.getWorkOffset(d.getWorkOffsetNumber())
        work_z_zero = work_offset[Z]

        tool_number = d.getSpindleToolNumber()
        tool_length = d.getToolLength(tool_number)

        # >>> Sprawdzenie długości narzędzia <<<
        if tool_length is None or tool_length <= 0:
            msg.err(f"⚠️ Narzędzie T{tool_number} nie ma ustawionej długości!")
            d.stopTrajectory()
            sys.exit(1)

        # >>> Główne sprawdzenie Z <<<
        z_real = machine_z - work_z_zero + tool_length

        if z_real < Z_LIMIT_SAFE:
            msg.err(f"❗ Niebezpieczna pozycja Z=0! ({z_real:.2f} mm poniżej limitu stołu)")
            d.stopTrajectory()
            sys.exit(0)
        else:
            print(f"✅ Z=0 bezpieczne: {z_real:.2f} mm nad limitem {Z_LIMIT_SAFE}")

    except Exception as e:
        msg.err(f"🛑 Błąd sprawdzania Z=0: {str(e)}")
        d.stopTrajectory()
        sys.exit(1)

print("📏 Sprawdzanie bezpieczeństwa Z=0 względem stołu...")
check_z_zero_safe()
