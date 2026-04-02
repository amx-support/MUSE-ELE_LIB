# -------------------------------------------------------------------------------------------------
#
# Muse TP List モジュール v1.1
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

class TPList:
    """
    タッチパネルリストを生成します。

    Parameters
    ----------
    tp_list : list
        タッチパネルのリスト
    ----------
    """

    # 初期化 -----------------------------------------------------------------------------------------
    def __init__(self,tp_list):
        self.l = {}
        for tp in tp_list:
            self.l[tp.id] = tp

    # ボタンイベント処理登録 ---------------------------------------------------------------------------------
    def button_watch(self, port:int, button:int, func, device=None):
        """
        button.watch のイベントを登録します。

        Parameters
        ----------
        port : int
            ポート番号
        button : int
            チャンネル番号
        func : func
            イベント用コールバック関数
        device : str
            対象デバイスのインスタンスID (None 個別処理の場合は指定する)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].button[button].watch(func)
        else:
            self.l[device].port[port].button[button].watch(func)
    
    # レベルイベント処理登録 ---------------------------------------------------------------------------------
    def level_watch(self, port:int, level:int, func, device=None):
        """
        level.watch のイベントを登録します。

        Parameters
        ----------
        port : int
            ポート番号
        level : int
            レベル番号
        func : func
            イベント用コールバック関数
        device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].level[level].watch(func)
        else:
            self.l[device].port[port].level[level].watch(func)
    
    # ストリングイベント処理登録 -------------------------------------------------------------------------------
    def string_listen(self, port:int ,func, device=None):
        """
        string.listen のイベントを登録します。

        Parameters
        ----------
        port : int
            ポート番号
        func : func
            イベント用コールバック関数
        device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].string.listen(func)
        else:
            self.l[device].port[port].string.listen(func)
    
    # コマンドイベント処理登録 --------------------------------------------------------------------------------
    def command_listen(self, port:int, func, device=None):
        """
        command.listen のイベントを登録します。

        Parameters
        ----------
        port : int
            ポート番号
        func : func
            イベント用コールバック関数
        device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].command.listen(func)
        else:
            self.l[device].port[port].command.listen(func)
    
    # カスタムイベント処理登録 --------------------------------------------------------------------------------
    def custom_listen(self,port,func,device=None):
        """
        custom.listen のイベントを登録します。

        Parameters
        ----------
        port : int
            ポート番号
        func : func
            イベント用コールバック関数
        device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].custom.listen(func)
        else:
            self.l[device].port[port].custom.listen(func)
    
    # SEND_COMMAND 送信 -----------------------------------------------------------------------------
    def send_command(self, port:int, command:str, device=None):
        """
        SEND_COMMANDを実行します。

        Parameters
        ----------
        port : int
            ポート番号
        command : str
            送信データ
        device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].send_command(command)
        else:
            self.l[device].port[port].send_command(command)
    
    # SEND_STRING 送信 ------------------------------------------------------------------------------
    def send_string(self, port:int, string:str, device=None):
        """
        SEND_STRINGを実行します。

        Parameters
        ----------
        port : int
            ポート番号
        string : str
            送信データ
        device : str
            対象デバイスのインスタンスID (None == すべて)
        -------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].send_string(string)
        else:
            self.l[device].port[port].send_string(string)
    
    # チャンネル操作 -------------------------------------------------------------------------------------
    def channel(self,port:int, channel:int, value:bool, device=None):
        """
        チャンネルを操作します。

        Parameters
        ----------
        port : int
            ポート番号
        channel : int
            チャンネル番号
        value : bool
            動作 (True == ON / False == OFF)
        device : str
            device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].channel[channel].value = value
        else:
            self.l[device].port[port].channel[channel].value = value
    
    # レベル操作 ---------------------------------------------------------------------------------------
    def level(self,port:int, level:int, value:int, device=None):
        """
        レベルを操作します。

        Parameters
        ----------
        port : int
            ポート番号
        level : int
            レベル番号
        value : int
            レベル値
        device : str
            対象デバイスのインスタンスID (None == すべて)
        ----------
        """

        if device is None:
            for l in self.l.values():
                l.port[port].level[level].value = value
        else:
            self.l[device].port[port].level[level].value = value