# -------------------------------------------------------------------------------------------------
#
# Muse PULSE実行モジュール v1.1
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

from mojo import context

class Pulse:
    """
    パルス処理の管理用インスタンスを生成します。
    """

    # 初期化 -----------------------------------------------------------------------------------------
    def __init__(self):
        self.__pulse_list = []
        self.__tl = context.services.get("timeline")
        self.__tl.expired.listen(self.__pulse_check)


    # PULSE登録 -------------------------------------------------------------------------------------
    # PULSE追加
    def __pulse_append(self, dev, ch, time, type):
        # リストが空だったらtimelineを開始
        if self.__pulse_list == []:
            self.__tl.start([100],False,-1)
        
        # 多重登録チェック
        for ls in self.__pulse_list:
            if ls["device"] == dev and ls["channel"] == ch:
                return
        
        # タイプ別処理
        if type == "muse relay":
            dev[ch].state.value = True
        elif type == "muse ir":
            dev.onIr(ch)
        elif type == "muse io":
            dev[ch].output.value = True
        elif type == "netlinx":
            dev.channel[ch].value = True
        
        # パルス追加
        self.__pulse_list.append({"type":type,"device":dev,"channel":ch,"time":time})
 
    ##### MUSE系 relay #####
    def pulse_muse_relay(self, dev, ch:int, time:int):
        """
        idevice.relay / CE-REL8 のパルスを実行します。

        Parameters
        ----------
        dev
            対象のデバイス (dev.relay を指定)
        ch : int
            チャンネル番号 (0から)
        time : int
            パルス時間 (0.1秒単位)
        ----------
        """

        self.__pulse_append(dev, ch, time, "muse relay")
        
    ##### MUSE系 ir #####
    def pulse_muse_ir(self, dev, ch:int, time:int):
        """
        idevice.ir / CE-IRS4 のパルスを実行します。

        Parameters
        ----------
        dev
            対象のデバイス (dev.ir[n] を指定)
        ch : int
            コード番号 (1～255)
        time : int
            パルス時間 (0.1秒単位)
        ----------
        """

        self.__pulse_append(dev, ch, time,"muse ir")
    
    ##### MUSE系 io #####
    def pulse_muse_io(self, dev, ch:int, time:int):
        """
        idevice.io / CE-IO4 のパルスを実行します。

        Parameters
        ----------
        dev
            対象のデバイス (dev.io を指定)
        ch : int
            チャンネル番号 (0から)
        time : int
            パルス時間 (0.1秒単位)
        ----------
        """

        self.__pulse_append(dev, ch, time, "muse io")

    ##### netlinx #####
    def pulse_netlinx(self, dev, ch:int, time:int):
        """
        NetLinx系デバイスのパルスを実行します。

        Parameters
        ----------
        dev
            対象デバイス (dev.port[n].channel を指定)
        ch : int
            チャンネル番号 (1から)
        time : int
            パルス時間 (0.1秒単位)
        ----------
        """

        self.__pulse_append(dev,ch,time,"netlinx")


    # PULSE終了チェック ---------------------------------------------------------------------------------
    def __pulse_check(self,e):

        # カウントダウンと終了済みの確認
        check = False
        for l in self.__pulse_list:
            l["time"] -=1
            if l["time"] <= 0:
                check = True
        
        # 終了済みがあった場合
        if check:
            tmp = []

            # PULSEリストを確認
            while self.__pulse_list:
                ls = self.__pulse_list.pop()
                
                # PULSE継続
                if ls["time"]:
                    tmp.append(ls)
                
                # PULSE終了
                else:
                    # Muse系デバイス
                    if ls["type"] == "muse relay":
                        ls["device"][ls["channel"]].state.value = False
                    elif ls["type"] == "muse ir":
                        ls["device"].offIr(ls["channel"])
                    elif ls["type"] == "muse io":
                        ls["device"][ls["channel"]].output.value = False
                    
                    # Netlinx系デバイス
                    elif ls["type"] == "netlinx":
                        ls["device"].channel[ls["channel"]].value = False

            # リスト再構成
            if tmp:
                while tmp:
                    self.__pulse_list.append(tmp.pop())
            else:
                self.__tl.stop()