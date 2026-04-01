from mojo import context
from ele_lib import pulse

# MUSE-3300 ---------------------------------------------------------------------------------------
muse = context.devices.get("idevice")
relay = muse.relay
ir = muse.ir[0]
io = muse.io

# VARIA-100 ---------------------------------------------------------------------------------------
varia = context.devices.get("AMX-10001")
tp = varia.port[1]

# PULSE用オブジェクト生成 ----------------------------------------------------------------------------------
pl = pulse.Pulse()

# MUSEオンライン処理 -------------------------------------------------------------------------------------
def muse_online(e):
    for ch in range(8):
        io[ch].mode.value = "OUTPUT"    # 動作モードを OUTPUT に設定


# ボタン操作 -------------------------------------------------------------------------------------------
def btn_ev(e):
    ch = int(e.id)

    tp.channel[ch].value = e.value

    if e.value: # PUSH
        match(ch):
            case 1:
                pl.pulse_muse_relay(relay, 0, 5)
            case 2:
                pl.pulse_muse_relay(relay, 1, 10)
            case 3:
                pl.pulse_muse_relay(relay, 2, 20)
        
            case 11:
                pl.pulse_muse_ir(ir, 1, 5)
            case 12:
                pl.pulse_muse_ir(ir, 2, 5)
        
            case 21:
                pl.pulse_muse_io(io, 0, 5)
            case 22:
                pl.pulse_muse_io(io, 1, 10)
            case 23:
                pl.pulse_muse_io(io, 2, 20)
        
            case 31:
                pl.pulse_netlinx(tp, 41, 5)
            case 32:
                pl.pulse_netlinx(tp, 42, 10)
            case 33:
                pl.pulse_netlinx(tp, 43, 20)
            
            case 51:
                for i in range(8):
                    pl.pulse_muse_relay(relay, i, 10)
            case 52:
                for i in range(8):
                    pl.pulse_muse_io(io, i, 10)


# リレーチャンネルイベント ------------------------------------------------------------------------------------
def relay_ev(e):
    for ch in range(8):
        tp.channel[101 + ch].value = relay[ch].state.value

# I/Oチャンネルイベント ------------------------------------------------------------------------------------
def io_ev(e):
    for ch in range(8):
        tp.channel[111 + ch] = io[ch].output.value


# イベント取得 ------------------------------------------------------------------------------------------
ev_ch = [1,2,3,11,12,21,22,23,31,32,33,51,52]
for ch in ev_ch:
    tp.button[ch].watch(btn_ev)

for ch in range(8):
    relay[ch].state.watch(relay_ev)
    io[ch].output.watch(io_ev)

context.run(globals())