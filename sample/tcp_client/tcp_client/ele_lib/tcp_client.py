#--------------------------------------------------------------------------------------------------
#
# TCP Client モジュール v0.9
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

import inspect
import queue
import socket
import threading

from mojo import context

# イベントパラメータ用クラス -----------------------------------------------------------------------------------
class EvParams:
    def __init__(self, source, device:str, id:str, path:str, value=False, arguments=None):
        self.source = source
        self.device = device
        self.id = id
        self.path = path
        self.value = value
        self.arguments = arguments

# 本体 ----------------------------------------------------------------------------------------------
class TcpClient:
    """
    インスタンスを生成します。

    Parameters
    ----------
    device : str
        インスタンス識別用ID 重複不可
    address : str
        接続先URL
    port : int
        接続先IPポート番号
    receive_bytes : int
        最大受信バイト数 (1024)
    keepidle : int
        Keep Alive設定用 (30)
    kiipintval : int
        Keep Alive設定用 (5)
    keepcnt : int
        Keep Alive設定用 (3)
    sendtimeout : int
        送信タイムアウト (10000 =10秒)
    """

    __dev_list = {}                     # デバイスリスト

    ERR_SOCK_OPEN = 1                   # すでにソケットが開いている
    ERR_SOCK_NOT_OPEN = 2               # ソケットが開かれていない
    ERR_SOCK_CONNECTION_REFUSED = 3     # 接続が拒否された
    ERR_SOCK_NO_ROUTE = 4               # ルートがない (相手がいない、MUSE側のLAN抜け)
    ERR_SOCK_TIMEOUT = 5                # 接続タイムアウト
    ERR_SOCK_ADDR_ALREADY_IN_USED = 6   # ポートバインド失敗
    ERR_SEND_INVALID_ARGS = 21          # 送信データの型が不正 (str, bytesのみ)

    # 初期化 -----------------------------------------------------------------------------------------
    def __init__(self, device:str, address:str, port:int, receive_bytes = 1024, keepidle = 30, keepintval = 5, keepcnt = 3, sendtimeout = 10000):
        # デバイス名がstrでなければ例外をスロー
        if type(device) is not str:
            raise ValueError(f"device<{device}({type(device).__name__})> is not str")

        # デバイス名が重複している場合は例外をスロー
        if self.__class__.__dev_list is not None and device in self.__class__.__dev_list:
            raise ValueError(f"device<{device}> already exists")
        
        # アドレスがstrでなければ例外をスロー
        if type(address) is not str:
            raise ValueError(f"address<{address}({type(address).__name__})> is not str")

        # ポート番号がintでなければ例外をスロー
        if type(port) is not int:
            raise ValueError(f"port<{port}({type(port).__name__})> is not int")
        
        # receive_bytesがintでなければ例外をスロー
        if type(receive_bytes) is not int:
            raise ValueError(f"receive_bytes<{receive_bytes}({type(receive_bytes).__name__})> is not int")
        
        # keepidleがintでなければ例外をスロー
        if type(keepidle) is not int:
            raise ValueError(f"keepidle<{keepidle}({type(keepidle).__name__})> is not int")

        # keepintvalがintでなければ例外をスロー
        if type(keepintval) is not int:
            raise ValueError(f"keepintval<{keepintval}({type(keepintval).__name__})> is not int")

        # keepcntがintでなければ例外をスロー
        if type(keepcnt) is not int:
            raise ValueError(f"keepcnt<{keepcnt}({type(keepcnt).__name__})> is not int")
        
        # sendtimeoutがintでなければ例外をスロー
        if type(sendtimeout) is not int:
            raise ValueError(f"sendtimeout<{sendtimeout}({type(sendtimeout).__name__})> is not int")

        self.__device = device                          # デバイス名
        self.__socket = None                            # ソケット
        self.__address = address                        # 接続先URL
        self.__port = port                              # 接続先IPポート
        self.__online = False                           # オンライン状態
        self.__receive_bytes = receive_bytes            # 最大受信量
        self.__command_queue = queue.Queue()            # 送信データキュー
        self.__connect_thread = None                    # 接続処理用スレッド
        self.__receive_thread = None                    # 受信処理用スレッド
        self.__send_thread = None                       # 送信処理用スレッド
        self.__online_callback_func = None              # ONLINEコールバック関数
        self.__offline_callback_func = None             # OFFLINEコールバック関数
        self.__receive_callback_func = None             # 受信コールバック関数
        self.__onerror_callback_func = None             # ONERRORコールバック関数
        self.__keepidle = keepidle                      # Keep Alive設定用
        self.__keepintval = keepintval                  # Keep Alive設定用
        self.__keepcnt = keepcnt                        # Keep Alive設定用
        self.__sendtimeout = sendtimeout                # 送信タイムアウト

        self.__class__.__dev_list[device] = self        # デバイスリストに追加

    # インスタンスの取得 -----------------------------------------------------------------------------------
    @classmethod
    def dev(cls, device:str):
        """
        インスタンスを取得します。

        Parameters
        ----------
        device : str
            デバイスID

        Returns
        -----------
        instance : instance
            存在する場合はインスタンスを返す。存在しない場合はNoneを返す
        ----------

        """

        if cls.__dev_list is not None and device in cls.__dev_list:
            return cls.__dev_list[device]
        else:
            return None

    # 接続処理（スレッド用） ---------------------------------------------------------------------------------
    def __open(self):
        # ソケットを開いてなければ
        if self.__socket is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, self.__keepidle)
            self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, self.__keepintval)
            self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, self.__keepcnt)
            self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_USER_TIMEOUT, self.__sendtimeout)

            try:
                # 接続
                self.__socket.connect((self.__address, self.__port))
                self.__online = True

                # ONLINEイベント生成
                self.__ev_online()

                # 受信処理開始
                self.__receive()
            
            # 例外：接続タイムアウト
            except TimeoutError as e:
                self.__ev_onerror("open", f"{self.__class__.__name__}/open", self.__class__.ERR_SOCK_TIMEOUT, "Connection timed out")
                self.__socket.close()
                self.__socket = None
                self.__online = False
            
            # 例外：接続が拒否された
            except ConnectionRefusedError as e:
                match(e.errno):
                    case 111:   # Connection refused (接続が拒否された：相手がオープンされていない)
                        self.__ev_onerror("open", f"{self.__class__.__name__}/open", self.__class__.ERR_SOCK_CONNECTION_REFUSED, "Connection refused")
                        self.__socket = None
                        self.__online = False

                    case _:     # 対象外の例外を再スロー
                        raise
            
            # 例外：相手がいないなど
            except OSError as e:
                match(e.errno):
                    case 113:   # No route to host (相手がいない、MUSE側のLAN抜け)
                        self.__ev_onerror("open", f"{self.__class__.__name__}/open", self.__class__.ERR_SOCK_NO_ROUTE, "No route to host")
                        self.__socket = None
                        self.__online = False

                    case _:     # 対象外の例外を再スロー
                        raise

    
    # 接続処理 ----------------------------------------------------------------------------------------
    def open(self):
        """
        ソケットを開きます。
        """

        # オンラインなら ONERROR
        if self.__online == True:
            self.__ev_onerror(inspect.currentframe().f_code.co_name, f"{self.__class__.__name__}/{inspect.currentframe().f_code.co_name}", self.__class__.ERR_SOCK_OPEN, "socket is already open")

        # オフラインなら
        if self.__online == False:
            # キューを空に
            for _ in range(self.__command_queue.qsize()):
                self.__command_queue.get()

            # 接続処理スレッド開始
            self.__connect_thread = threading.Thread(target=self.__open)
            self.__connect_thread.start()
    
    # 切断処理（スレッド用） ---------------------------------------------------------------------------------
    def __close(self):
        # ソケットが開いていれば
        if self.__socket is not None:
            self.__socket.close()
            self.__socket = None
            self.__online = False

            # 受信用スレッドを終了
            if self.__receive_thread is not None:
                self.__receive_thread = None

            # OFFLINEイベント生成
            self.__ev_offline()
    
    # 切断処理 ----------------------------------------------------------------------------------------
    def close(self):
        """
        ソケットを閉じます。
        """

        # オフラインなら ONERROR
        if self.__online == False:
            self.__ev_onerror(inspect.currentframe().f_code.co_name, f"{self.__class__.__name__}/{inspect.currentframe().f_code.co_name}", self.__class__.ERR_SOCK_NOT_OPEN, "socket is not open")

        # オンラインなら
        if self.__online == True:
            # キューを空に
            for _ in range(self.__command_queue.qsize()):
                self.__command_queue.get()

            # 切断処理スレッド開始
            self.__connect_thread = threading.Thread(target=self.__close)
            self.__connect_thread.start()
    
    # 受信処理（スレッド用） ---------------------------------------------------------------------------------
    def __recv(self):
        # ソケットが開いていたら
        if self.__socket is not None:
            # タイムアウトを１秒に
            self.__socket.settimeout(1)

            # 受信ループ
            while True:
                try:
                    # 受信待ち受け
                    data, address = self.__socket.recvfrom(self.__receive_bytes)

                    # 相手が切断した場合や送信タイムアウトによる切断（その場合受信が0byteになる）
                    # または LANケーブル抜けなどの Keep Aliveタイムアウト
                    if not data:
                        # 切断処理実行
                        self.__close()
                        break
                    else:
                        # 受信イベント生成
                        self.__ev_receive(data, (self.__address, self.__port))

                # 例外：時間切れ（デッドロック防止用　特に対応は必要なし）
                except TimeoutError as e:
                    pass

                # 例外：待ち受け中に自分で切断した場合など
                except OSError as e:
                    match(e.errno):
                        case 9:     # Bad file descriptor (待ち受け中に自分で切断)
                            break
                        case 113:   # No route to host (MUSE側LAN抜けや送信タイムアウト時など)
                            self.__close()
                            self.__socket = None
                            self.__online = False
                            break
                        case _:     # 対象外の例外を再スロー
                            raise


    # 受信処理 ----------------------------------------------------------------------------------------
    def __receive(self):
        # オンラインだったら
        if self.__online == True:
            # 受信処理スレッド開始
            self.__receive_thread = threading.Thread(target=self.__recv)
            self.__receive_thread.start()
    
    # 送信処理（スレッド用） ---------------------------------------------------------------------------------
    def __send(self):
        # ソケットを開いていたら
        if self.__socket is not None:
            # 送信キューが空でなければ
            while self.__command_queue.qsize() > 0:
                # キューからデータを取り出し
                cmd = self.__command_queue.get()
                # データの型チェック
                match(cmd):
                    case bytes():
                        pass
                    case str():
                        cmd = cmd.encode()
                    case _:
                        self.__ev_onerror("send", f"{self.__class__.__name__}/send", self.__class__.ERR_SEND_INVALID_ARGS, f"invalid args [{type(cmd).__name__}] (str or bytes)")
                        continue

                # 送信
                self.__socket.sendall(cmd)

    
    # 送信処理 ----------------------------------------------------------------------------------------
    def send(self, command:str | bytes):
        """
        サーバーへデータを送信します。

        Parameters
        ----------
        command : str | bytes
            送信データ
        """

        # オフラインだったら
        if self.__online == False:
            self.__ev_onerror(inspect.currentframe().f_code.co_name, f"{self.__class__.__name__}/{inspect.currentframe().f_code.co_name}", self.__class__.ERR_SOCK_NOT_OPEN, "socket is not open")

        # オンラインだったら
        else:
            # キューが空だったら
            if self.__command_queue.qsize() == 0:
                # キューに追加
                self.__command_queue.put(command)
                # 送信処理スレッド開始
                self.__send_thread = threading.Thread(target=self.__send)
                self.__send_thread.start()
            
            # キューが空でなかったら
            else:
                # キューに追加
                self.__command_queue.put(command)
    
    # ONLINEコールバック登録 ------------------------------------------------------------------------------
    def online(self, func):
        """
        オンラインイベントコールバックを登録します。

        Parameters
        ----------
        func : function
            オンライン処理用関数
        ----------
        """

        self.__online_callback_func = func
    
    # ONLINEイベント生成 --------------------------------------------------------------------------------
    def __ev_online(self):
        if self.__online_callback_func is not None:
            e = EvParams(self, self.__device, "online", f"{self.__class__.__name__}/online", True)
            self.__online_callback_func(e)
    
    # OFFLINEコールバック登録 -----------------------------------------------------------------------------
    def offline(self, func):
        """
        オフラインイベントコールバックを登録します。

        Parameters
        ----------
        func : function
            オフライン処理用関数
        ----------
        """

        self.__offline_callback_func = func
    
    # OFFLINEイベント生成 -------------------------------------------------------------------------------
    def __ev_offline(self):
        if self.__offline_callback_func is not None:
            e = EvParams(self, self.__device, "offline", f"{self.__class__.__name__}/offline",False)
            self.__offline_callback_func(e)
    
    # 受信コールバック登録 ----------------------------------------------------------------------------------
    def listen(self, func):
        """
        データ受信イベントコールバックを登録します。

        Parameters
        ----------
        func : function
            データ受信処理用関数
        ----------
        """

        self.__receive_callback_func = func
    
    # 受信イベント生成 ------------------------------------------------------------------------------------
    def __ev_receive(self, data:bytes, address:list):
        if self.__receive_callback_func is not None:
            e = EvParams(self, self.__device, "receive", f"{self.__class__.__name__}/receive", True, {"data":data,"length":len(data),"address":address[0],"port":address[1]})
            self.__receive_callback_func(e)
    
    # ONERRORコールバック登録 -----------------------------------------------------------------------------
    def onerror(self, func):
        self.__onerror_callback_func = func

    # ONERRORイベント生成 -------------------------------------------------------------------------------
    def __ev_onerror(self, id:str, path:str, code:int, text:str):
        context.log.error(f"ele_lib ONERROR in {path}: ({code}, {text})")
        if self.__onerror_callback_func is not None:
            e = EvParams(self, self.__device, id,path,code,{"text":text})
            self.__onerror_callback_func(e)
    
    # オンライン状態取得 -----------------------------------------------------------------------------------
    def isOnline(self) -> bool:
        """
        接続状態がオンラインか取得します。

        Returns
        ----------
        bool
            True オンライン時
            False オフライン時
        ----------
        """

        return self.__online
    
    # オフライン状態取得 -----------------------------------------------------------------------------------
    def isOffline(self) -> bool:
        """
        接続状態がオフラインか取得します。

        Returns
        ----------
        bool
            True オフライン時
            False オンライン時
        ----------
        """
        
        return not self.__online