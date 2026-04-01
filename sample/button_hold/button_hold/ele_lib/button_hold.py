#--------------------------------------------------------------------------------------------------
#
# Button Hold モジュール v1.1
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

from threading import Thread
import time

# Hold処理用クラス --------------------------------------------------------------------------------------
class Hold:
    """
    Hold処理の管理用インスタンスを生成します。

    Parameters
    ----------
    button
        タッチパネルのボタン
    evant_callback : func
        イベント処理用コールバック関数
    hold_time : float
        ホールド時間 (0.5 == 0.5秒)
    delay : float
        初回のディレイ時間 (0.0 == 0.0秒)
    repeat : bool
        繰り返しフラグ (False == 繰り返しなし)
    ----------
    """

    # 初期化
    def __init__(self,button,event_callback,hold_time:float=0.5,delay:float=0.0,repeat:bool=False):
        self.__button = button
        self.__event_callback = event_callback
        self.__hold_time = hold_time
        self.__delay = delay
        self.__repeat = repeat
        self.__event_parm = None
        self.__thread = None
        self.__button.watch(self.__button_update)

    # Push / Release 検知用コールバック関数
    def __button_update(self,e):
        self.__event_parm = e

        # 押したときHold処理用スレッド生成
        if e.value:
            if self.__thread is None:
                self.__thread = self.__HoldThread(self.__event_callback, self.__event_parm, self.__hold_time, self.__delay, self.__repeat)
                self.__thread.start()

        # 放したときスレッド終了
        else:
            self.__thread.shutdown = True
            self.__thread = None
    
    # Hold処理用スレッドクラス ------------------------------------------------------------------------------
    class __HoldThread(Thread):
        # 初期化
        def __init__(self, event_callback, event_parm, hold_time, delay, repeat):
            self.__event_callback = event_callback
            self.__event_parm = event_parm
            self.__hold_time = hold_time
            self.__delay = delay
            self.__repeat = repeat
            self.shutdown = False
            super().__init__(daemon=True)
        
        # Hold動作の実行用関数
        def run(self):
            if self.__delay > 0:
                time.sleep(self.__delay) # ディレイ処理
            else:
                time.sleep(self.__hold_time)
            
            if not self.shutdown:
                self.__event_callback(self.__event_parm)
                if not self.__repeat: # 繰り返しでなければ終了
                    return

            # Hold繰り返し
            while not self.shutdown:
                time.sleep(self.__hold_time)

                if not self.shutdown:
                    self.__event_callback(self.__event_parm)