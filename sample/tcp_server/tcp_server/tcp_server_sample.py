from mojo import context
from ele_lib import tcp_server as tcps

# VARIA-100
varia = context.devices.get("AMX-10001")
tp = varia.port[1]

# TIMELINE
tl = context.services.get("timeline")
tl.start([300], False, -1)

IP_ADD = "192.168.52.101"
IP_RECV_PORT = 20000


# TCP CLIENT
tcp = tcps.TcpServer("TCP", IP_RECV_PORT)


# ONLINEイベント
def tcp_online(e):
    device = e.device
    source = e.source
    address = e.arguments["address"]
    port = e.arguments["port"]
    print(f"[ONLINE] ID: {device} SOURCE: {source} ADDRESS: {address} PORT: {port}")
tcp.online(tcp_online)

# OFFLINEイベント
def tcp_offline(e):
    device = e.device
    source = e.source
    print(f"[OFFLINE] ID: {device} SOURCE: {source}")
tcp.offline(tcp_offline)

# ONERRORイベント
def tcp_onerror(e):
    device = e.device
    source = e.source
    id = e.id
    path = e.path
    error_code = e.value
    error_text = e.arguments["text"]
    print(f"DEV: {device} SOURCE: {source} ID: {id} PATH: {path} CODE: {error_code} TEXT: {error_text}")
tcp.onerror(tcp_onerror)


# TIMELINEイベント
def tl_ev(e):
    tp.channel[3].value = tcp.isOnline()
tl.expired.listen(tl_ev)


# 受信イベント
def data_ev(e):
    address = e.arguments["address"]
    port = e.arguments["port"]
    data_text = e.arguments["data"].decode("utf-8")
    length = e.arguments["length"]
    tp.send_command(f"^TXT-1,0,IP: {address}\nPORT: {port}\nDATA: {data_text}\nLEN: {length}")
tcp.listen(data_ev)


# ボタンイベント
def btn_ev(e):
    ch = int(e.id)

    tp.channel[ch].value = e.value

    if e.value:
        match(ch):
            case 1:
                tcp.open()
            case 2:
                tcp.close()
            case 4:
                tcp.send("Hello, world!")
            case 5:
                tcp.send("XYZ")
            case 6:
                tp.send_command("^TXT-1,0,")
for ch in [1,2,4,5,6]:
    tp.button[ch].watch(btn_ev)

context.run(globals())
