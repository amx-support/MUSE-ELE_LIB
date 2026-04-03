from mojo import context
from ele_lib import udp_server as udps

# VARIA-100
varia = context.devices.get("AMX-10001")
tp = varia.port[1]

# TIMELINE
tl = context.services.get("timeline")
tl.start([300], False, -1)

IP_ADD = "192.168.52.101"
IP_SEND_PORT = 10000
IP_RECV_PORT = 20000


# UDP SERVER
udp = udps.UdpServer("UDP", IP_RECV_PORT)


# ONLINEイベント
def udp_online(e):
    device = e.device
    source = e.source
    print(f"[ONLINE] ID: {device} SOURCE: {source}")
udp.online(udp_online)

# OFFLINEイベント
def udp_offline(e):
    device = e.device
    source = e.source
    print(f"[OFFLINE] ID: {device} SOURCE: {source}")
udp.offline(udp_offline)

# ONERRORイベント
def udp_onerror(e):
    device = e.device
    source = e.source
    id = e.id
    path = e.path
    error_code = e.value
    error_text = e.arguments["text"]
    print(f"DEV: {device} SOURCE: {source} ID: {id} PATH: {path} CODE: {error_code} TEXT: {error_text}")
udp.onerror(udp_onerror)


# TIMELINEイベント
def tl_ev(e):
    tp.channel[3].value = udp.isOnline()
tl.expired.listen(tl_ev)


# 受信イベント
def data_ev(e):
    address = e.arguments["address"]
    port = e.arguments["port"]
    data_text = e.arguments["data"].decode("utf-8")
    length = e.arguments["length"]
    tp.send_command(f"^TXT-1,0,IP: {address}\nPORT: {port}\nDATA: {data_text}\nLEN: {length}")
udp.listen(data_ev)


# ボタンイベント
def btn_ev(e):
    ch = int(e.id)

    tp.channel[ch].value = e.value

    if e.value:
        match(ch):
            case 1:
                udp.open()
            case 2:
                udp.close()
            case 4:
                udp.send(IP_ADD, IP_SEND_PORT, "Hello, world!")
            case 5:
                udp.send(IP_ADD, IP_SEND_PORT, "XYZ")
            case 6:
                tp.send_command("^TXT-1,0,")
for ch in [1,2,4,5,6]:
    tp.button[ch].watch(btn_ev)

context.run(globals())
