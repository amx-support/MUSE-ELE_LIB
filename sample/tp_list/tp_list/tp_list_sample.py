from mojo import context
from ele_lib import tp_list

# タッチパネル
varia_1 = context.devices.get("AMX-10001")
varia_2 = context.devices.get("AMX-10002")

# タッチパネルリスト生成
tpls = tp_list.TPList([varia_1,varia_2])


# ボタン操作
def btn_ev(e):
    ch = int(e.id)

    print(f"{e.device}: Ch {ch} - {'Push' if e.value else 'Release'}")

    # 押したボタンを点灯 (自分のみ)
    tpls.channel(1, ch, e.value, e.device)

    if e.value:
        match(ch):
            case 1:
                tpls.channel(1, 3, True)
            case 2:
                tpls.channel(1, 3, True, e.device)
            case 4:
                tpls.send_command(1, "^TXT-1,0,Hello, world!")
            case 5:
                tpls.send_command(1, "^TXT-1,0,Hello, world!", e.device)
            case 6:
                tpls.send_command(1, "^TXT-1,0,")
            case 7:
                tpls.send_command(1, "^PGE-Page2")
            case 8:
                tpls.send_command(1, "^PGE-Page2", e.device)
            case 9:
                tpls.send_command(1, '^PGE-Page')
    else:
        match(ch):
            case 1:
                tpls.channel(1, 3, False)
            case 2:
                tpls.channel(1, 3, False, e.device)
for ch in range(1,10):
    tpls.button_watch(1, ch, btn_ev)


# レベル操作
def lv_ev(e):
    lv = int(e.id)
    val = int(e.value)

    print(f"{e.device}: Lv {lv} Val {val}")

    match(lv):
        case 1:
            tpls.level(1, 3, val)
        case 2:
            tpls.level(1, 3, val, e.device)
for lv in range(1,3):
    tpls.level_watch(1, lv, lv_ev)


context.run(globals())
