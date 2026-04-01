from mojo import context
from ele_lib import button_hold as bh

# デバイス定義 ------------------------------------------------------------------------------------------

# MU-3300
muse = context.devices.get("idevice")
relay = muse.relay

# VARIA-100
varia = context.devices.get("AMX-10001")
tp = varia.port[1]

# イベント定義 ------------------------------------------------------------------------------------------
def btn_ev(e):
    ch = int(e.id)

    print(f"Push/Release: {ch}")

    tp.channel[ch].value = e.value

    relay[0].state.value = False

def hold_ev(e):
    ch = int(e.id)

    print(f"Hold: {ch}")

    relay[0].state.value = not relay[0].state.value


tp.button[1].watch(btn_ev)
bh.Hold(tp.button[1], hold_ev, 1.0, 0.0, True)
tp.button[2].watch(btn_ev)
bh.Hold(tp.button[2], hold_ev, 0.3, 1.0, True)

context.run(globals())