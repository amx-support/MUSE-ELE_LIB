# -------------------------------------------------------------------------------------------------
#
# Muse WAIT実行モジュール v1.1
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

import inspect
import time
from mojo import context

class Wait:
    """
    WAIT処理管理用のインスタンスを生成します。
    """

    # 初期化 -----------------------------------------------------------------------------------------
    def __init__(self):
        self.__wait_list = []
        self.__perf_counter = 0.0
        self.__tl = context.services.get("timeline")
        self.__tl.expired.listen(self.__wait_check)


    # WAIT登録 --------------------------------------------------------------------------------------
    # WAIT追加
    def __wait_append(self, type, flag_func, wait_time, func, args, name):
        # リストが空だったらtimelineを開始
        if self.__wait_list == []:
            self.__tl.start([100], False, -1)
            self.__perf_counter = time.perf_counter()

        # 多重登録チェック
        for ls in self.__wait_list:
            if ls["name"] == name:
                return
        
        # WAIT追加
        self.__wait_list.append({"type":type,"flag_func":flag_func,"time":wait_time,"func":func,"args":args,"name":name,"execute":False})

    # 指定時間WAIT
    def wait(self, time:int, func, args=None, name=None):
        """
        指定時間後に処理を実行します。

        Parameters
        ----------
        time : int
            実行までの待ち時間 (0.1秒単位)
        func : func
            実行する関数
        args : list
            関数に使用する引数リスト (None)
        name : str
            キャンセル用の名前 (None)
        """

        #名前無しWAITの場合はファイル名と行番号で名前生成
        if name is None:
            frame = inspect.currentframe().f_back
            name = "%s%s"%(frame.f_code.co_filename, frame.f_lineno)

        self.__wait_append("wait", None, time, func, args, name)
    
    # 条件付きWAIT
    def wait_until(self, flag_func, func, args=None, name=None):
        """
        指定条件成立後に処理を実行します。

        Parameters
        ----------
        flag_func : func
            条件用関数 (戻り値がTrueになると実行)
        func : func
            実行する関数
        args : list
            関数に使用する引数リスト (None)
        name : str
            キャンセル用の名前 (None)
        ----------
        """

        #名前無しWAITの場合はファイル名と行番号で名前生成
        if name is None:
            frame = inspect.currentframe().f_back
            name = "%s%s"%(frame.f_code.co_filename, frame.f_lineno)

        self.__wait_append("wait_until", flag_func, 0, func, args,name)
    
    # 指定時間条件付きWAIT
    def timed_wait_until(self, flag_func, time:int, func, args=None, name=None):
        """
        指定条件成立後に処理を実行します。（時間制限あり）

        Parameters
        ----------
        flag_func : func
            条件洋館数 (戻り値がTrueになると実行)
        time : int
            制限時間 (0.1秒単位)
        func : func
            実行する関数
        args : list
            関数に使用する引数リスト (None)
        name : str
            キャンセル用の名前 (None)
        ----------
        """

        #名前無しWAITの場合はファイル名と行番号で名前生成
        if name is None:
            frame = inspect.currentframe().f_back
            name = "%s%s"%(frame.f_code.co_filename, frame.f_lineno)

        self.__wait_append("timed_wait_until", flag_func, time, func, args, name)

    # WAIT実行
    def __wait_execute(self, func, args):
        if args is None:
            func()
        else:
            func(*args)
    
    # 指定時間WAITのキャンセル
    def cancel_wait(self, name:str):
        """
        WAITをキャンセルします。

        Parameters
        ----------
        name : str
            キャンセルするWAITの名前
        ----------
        """

        check = False
        count = 0
        for l in self.__wait_list:
            if l["type"] == "wait" and l["name"] == name:
                check = True
                break
            count += 1
        
        if check:
            del self.__wait_list[count]
        
            if not self.__wait_list:
                self.__tl.stop()

    # 条件付きWAIT系のキャンセル
    def cancel_wait_until(self, name:str):
        """
        WAIT_UNTILをキャンセルします。

        Parameters
        ----------
        name : str
            キャンセルするWAIT_UNTILの名前
        ----------
        """

        check = False
        count = 0
        for l in self.__wait_list:
            if (l["type"] == "wait_until" or l["type"] == "timed_wait_until") and l["name"] == name:
                check = True
                break
            count +=1
        
        if check:
            del self.__wait_list[count]
        
            if not self.__wait_list:
                self.__tl.stop()
    
    # 指定時間WAITのすべてをキャンセル
    def cancel_all_wait(self):
        """
        WAITをすべてキャンセルします。
        """

        check = False
        for l in self.__wait_list:
            if l["type"] == "wait":
                check = True
                break
        
        # キャンセルするWAITがあった場合
        if check:
            tmp = []

            # WAITリストを確認
            while self.__wait_list:
                ls = self.__wait_list.pop()
                
                # キャンセル対称以外は再登録
                if ls["type"] != "wait":
                    tmp.append(ls)

            # リスト再構成
            if tmp:
                while tmp:
                    self.__wait_list.append(tmp.pop())
            else:
                self.__tl.stop()
        
    # 条件付きWAITのすべてをキャンセル
    def cancel_all_wait_until(self):
        """
        WAIT_UNTIL / TIMED_WAIT_UNTILをすべてキャンセルします。
        """

        check = False
        for l in self.__wait_list:
            if l["type"] != "wait":
                check = True
                break
        
        # キャンセルするWAITがあった場合
        if check:
            tmp = []

            # WAITリストを確認
            while self.__wait_list:
                ls = self.__wait_list.pop()
                
                # キャンセル対称以外は再登録
                if ls["type"] == "wait":
                    tmp.append(ls)

            # リスト再構成
            if tmp:
                while tmp:
                    self.__wait_list.append(tmp.pop())
            else:
                self.__tl.stop()


    # WAIT実行チェック ---------------------------------------------------------------------------------
    def __wait_check(self,e):
        # 経過時間を確認
        now_time = time.perf_counter()
        elapsed_time = (now_time - self.__perf_counter) * 10
        self.__perf_counter = now_time

        # カウントダウンと実行確認
        check = False
        for l in self.__wait_list:
            if l["type"] == "wait":
                l["time"] -= elapsed_time
                if l["time"] <= 0:
                    check = True
                    l["execute"] = True

            elif l["type"] == "wait_until":
                if l["flag_func"]():
                    check = True
                    l["execute"] = True

            elif l["type"] == "timed_wait_until":
                l["time"] -= elapsed_time
                if l["time"] <= 0 or l["flag_func"]():
                    check = True
                    l["execute"] = True
        
        # 実行するWAITがあった場合
        if check:
            tmp = []

            # WAITリストを確認
            while self.__wait_list:
                ls = self.__wait_list.pop()
                
                # WAIT継続
                if ls["execute"] == False:
                    tmp.append(ls)
                
                # WAIT実行
                else:
                    if ls["type"] == "wait":
                        self.__wait_execute(ls["func"],ls["args"])
                    elif ls["type"] == "wait_until":
                        self.__wait_execute(ls["func"],ls["args"])
                    elif ls["type"] == "timed_wait_until" and ls["time"] > 0:
                        self.__wait_execute(ls["func"],ls["args"])

            # リスト再構成
            if tmp:
                while tmp:
                    self.__wait_list.append(tmp.pop())
            else:
                self.__tl.stop()