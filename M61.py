import time
from ___CONF import * 


def check_z_zero_safe():
    try:
        tool_number = d.getSpindleToolNumber()
        tool_length = d.getToolLength(tool_number)

        if tool_length is None or tool_length >= 0:
            msg.err(f"Narzędzie T{tool_number} ma niepoprawną długość: {tool_length}")
            d.setTrajectoryPause(True)
            msg.info("Wciśnij START po korekcie.")
            return False

        work_offset_z = d.getWorkOffset(d.getWorkOffsetNumber())[Z]
        z_machine_at_work_zero = work_offset_z + tool_length

        # msg.info(f"Z maszyny przy Z=0 roboczym: {z_machine_at_work_zero:.3f} mm")

        if z_machine_at_work_zero < Z_LIMIT_SAFE:
            d.setTrajectoryPause(True)
            msg.err(f"Z=0 robocze ({z_machine_at_work_zero:.2f}) poniżej limitu stołu ({Z_LIMIT_SAFE})")
            msg.info("Program wstrzymany. Skoryguj bazę lub długość narzędzia.")
            return False
        else:
            # msg.info(f"Z=0 bezpieczne: {z_machine_at_work_zero:.2f} mm nad limitem {Z_LIMIT_SAFE}")
            return True

    except Exception as e:
        d.setTrajectoryPause(True)
        msg.err(f"Błąd sprawdzania Z=0: {str(e)}")
        msg.info("Wciśnij START po naprawie błędu.")
        return False

check_z_zero_safe()
