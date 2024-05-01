from mojo import context
from ele_lib import button_hold as bh

# デバイス定義 ------------------------------------------------------------------------------------------

# MU-3300
dvMUSE = context.devices.get("idevice")
dvREL = dvMUSE.relay

# VARIA-100
dvVARIA = context.devices.get("AMX-10001")
dvTP = dvVARIA.port[1]

# イベント定義 ------------------------------------------------------------------------------------------
def ButtonEvent(e):
    ch = int(e.id)

    print("Push/Release: %s" %ch)

    dvTP.channel[ch] = e.value

    dvREL[0].state = False

def HoldEvent(e):
    ch = int(e.id)

    print("Hold: %s" %ch)

    dvREL[0].state = not dvREL[0].state.value


dvTP.button[1].watch(ButtonEvent)
bh.Hold(dvTP.button[1],HoldEvent,1.0,0,True)
dvTP.button[2].watch(ButtonEvent)
bh.Hold(dvTP.button[2],HoldEvent,0.3,1,True)

context.run(globals())