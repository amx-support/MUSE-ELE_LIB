#--------------------------------------------------------------------------------------------------
#
# Emulate Device モジュール v1.0
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

def btn_ev(func, dev, port:int, ch:int, val:bool):
    """
    ボタン入力のイベントをエミュレートします。

    Parameters
    ----------
    func : func
        イベント用コールバック関数
    dev
        対象デバイス
    port : int
        ポート番号
    ch : int
        チャンネル番号
    val : bool
        動作 (True:Push / False:Release)
    ----------
    """
    class Ev:
        def __init__(self,dev,port,ch,val):
            self.id = str(ch)
            self.path = f"port/{port}/button/{ch}"
            self.value = val 
            self.device = dev.id
            self.value = val
            self.newValue = val
            self.oldValue = not val
    ev = Ev(dev,port,ch,val)
    func(ev)

def lv_ev(func, dev, port:int, lv:int, val:int):
    """
    レベル変動のイベントをエミュレートします。

    Parameters
    ----------
    func : func
        イベント用コールバック関数
    dev
        対象デバイス
    port : int
        ポート番号
    lv : int
        レベル番号
    val : int
        レベル値
    ----------
    """

    class Ev:
        def __init__(self,dev,port,lv,val):
            self.id = str(lv)
            self.path = f"port/{port}/level/{lv}"
            self.device = dev.id
            self.value = float(val)
            self.newValue = float(val)
            self.oldValue = dev.port[port].level[lv].value
            self.normalized = 0.0
    ev = Ev(dev,port,lv,val)
    func(ev)

def data_ev(func, dev, port:int, data:str | bytes):
    """
    データ受信のイベントをエミュレートします。

    Parameters
    ----------
    func
        イベント用コールバック関数
    dev
        対象デバイス
    port : int
        ポート番号
    data : str | bytes
        受信データ
    ----------
    """

    class Ev:
        def __init__(self,dev,port,data):
            # idevice / CE-COM2
            if hasattr(dev,"serial"):
                self.id = "receive"
                self.path = f"serial/{port}/receive"
            # NetLinx
            elif hasattr(dev,"port"):
                self.id = str(port)
                self.path = f"port/{port}/string"
            
            # その他 (ipcommなど)
            else:
                self.id = "receive"
                self.path = "receive"

            self.device = dev.id
            self.arguments = {"data":data.encode(),"length":len(data.encode())}
    ev = Ev(dev,port,data)
    func(ev)