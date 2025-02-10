

from ___CONF import * 
import sys
import time
import json

JSON_FILE = "narzedzia.json"

#############################################
# Macro START - Uruchomienie procedury pomiaru długości narzędzia
#############################################

# Wyłącz wrzeciono
d.setSpindleState(SpindleState.OFF)

# Pobranie numeru narzędzia
toolNr = d.getSpindleToolNumber()
if toolNr == 0:
    sys.exit("Tool(0) has no tool length offset. Probing failed!")

# Pobranie aktualnej pozycji maszyny
machine_pos = d.getPosition(CoordMode.Machine)

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

# Zakończenie programu
print(f"Tool({toolNr}) offset set to: {toolOffset:.4f}")
