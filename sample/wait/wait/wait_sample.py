from mojo import context
from ele_lib import wait

# デバイス定義 ------------------------------------------------------------------------------------------
# MUSE
muse = context.devices.get("idevice")
serial = muse.serial
relay = muse.relay
io = muse.io

# TP
tp = context.devices.get("AMX-10001")

# TIMELINE
tl = context.services.get("timeline")
tl.start([300],False,-1)


# 変数定義 --------------------------------------------------------------------------------------------
# WAIT処理用インスタンス生成
wt = wait.Wait()


# 関数定義 --------------------------------------------------------------------------------------------
def serial_control(dev,data):
    dev.send(data)

def rel_control(devch,state):
    devch.state.value = state

def level_control(devlev,value):
    devlev.value = value

def io_state():
    return io[0].digitalInput.value

def send_data():
    wt.wait(20,serial_control,[serial[0],"Hello,world!"],"Wait Name Send 1")
    wt.wait(40,lambda:serial[0].send("hoge fuga piyo"),name="Wait Name Send 2")
    wt.wait(60,serial_control,[serial[0],"0123456789"],"Wait Name Send 3")


def refresh_tp():
    # ボタンのフィードバック
    tp.port[1].channel[11].value = relay[0].state.value
    tp.port[1].channel[12].value = io[0].digitalInput.value


# イベント定義 ------------------------------------------------------------------------------------------
# TIMELINE
def tl_ev(e):
    refresh_tp()
tl.expired.listen(tl_ev)

# SERIAL
def data_ev(e):
    data_text = e.arguments["data"].decode("UTF-8")

    tp.port[1].send_command(f"^TXT-1,0,{data_text}")
serial[0].receive.listen(data_ev)

# BUTTON
def btn_ev(e):
    ch = int(e.id)

    tp.port[1].channel[ch].value = e.value

    if e.value:
        match(ch):
            case 1:
                tp.port[1].level[1].value = 0
                wt.wait(10,level_control,[tp.port[1].level[1],1],"Wait Name 1")
                wt.wait(20,level_control,[tp.port[1].level[1],2],"Wait Name 2")
                wt.wait(30,level_control,[tp.port[1].level[1],3],"Wait Name 3")
                wt.wait(40,level_control,[tp.port[1].level[1],4],"Wait Name 4")
                wt.wait(50,level_control,[tp.port[1].level[1],5],"Wait Name 5")
                wt.wait(60,level_control,[tp.port[1].level[1],6],"Wait Name 6")
                wt.wait(70,level_control,[tp.port[1].level[1],7],"Wait Name 7")
                wt.wait(80,level_control,[tp.port[1].level[1],8],"Wait Name 8")
                wt.wait(90,level_control,[tp.port[1].level[1],9],"Wait Name 9")
                wt.wait(100,level_control,[tp.port[1].level[1],10],"Wait Name 10")

            case 2:
                wt.cancel_wait("Wait Name 1")
                wt.cancel_wait("Wait Name 2")
                wt.cancel_wait("Wait Name 3")
                wt.cancel_wait("Wait Name 4")
                wt.cancel_wait("Wait Name 5")
                wt.cancel_wait("Wait Name 6")
                wt.cancel_wait("Wait Name 7")
                wt.cancel_wait("Wait Name 8")
                wt.cancel_wait("Wait Name 9")
                wt.cancel_wait("Wait Name 10")
                tp.port[1].level[1].value = 0

            case 3:
                tp.port[1].level[1].value = 0
                wt.wait(10,level_control,[tp.port[1].level[1],1])
                wt.wait(20,level_control,[tp.port[1].level[1],2])
                wt.wait(30,level_control,[tp.port[1].level[1],3])
                wt.wait(40,level_control,[tp.port[1].level[1],4])
                wt.wait(50,level_control,[tp.port[1].level[1],5])
                wt.wait(60,level_control,[tp.port[1].level[1],6])
                wt.wait(70,level_control,[tp.port[1].level[1],7])
                wt.wait(80,level_control,[tp.port[1].level[1],8])
                wt.wait(90,level_control,[tp.port[1].level[1],9])
                wt.wait(100,level_control,[tp.port[1].level[1],10])

            case 4:
                wt.cancel_all_wait()
                tp.port[1].level[1].value = 0
        
            case 5:
                wt.wait_until(io_state,rel_control,[relay[0],True],"Wait Name Until 1")

            case 6:
                wt.cancel_wait_until("Wait Name Until 1")
                rel_control(relay[0],False)
        
            case 7:
                wt.timed_wait_until(lambda:io[0].digitalInput.value,100,rel_control,[relay[0],True])

            case 8:
                wt.cancel_all_wait_until()
                rel_control(relay[0],False)
        
            case 9:
                wt.wait(50,send_data)
        
            case 10:
                wt.cancel_wait("Wait Name Send 1")
                wt.cancel_wait("Wait Name Send 2")
                wt.cancel_wait("Wait Name Send 3")
                tp.port[1].send_command("^TXT-1,0,")
for ch in range(1,11):
    tp.port[1].button[ch].watch(btn_ev)

# MUSE ONLINE EVENT
def muse_online(e):
    serial[0].setCommParams("9600",8,1,"NONE","232")
    serial[0].setFlowControl("NONE")

    rel_control(relay[0],False)
    rel_control(relay[1],False)
    rel_control(relay[2],False)
    rel_control(relay[3],False)
    rel_control(relay[4],False)
    rel_control(relay[5],False)
    rel_control(relay[6],False)
    rel_control(relay[7],False)

    io[0].mode.value = "INPUT"
    io[0].inputMode.value = "DIGITAL"
    io[0].digitalInput2KPullup.value = True
muse.online(muse_online)

context.run(globals())
