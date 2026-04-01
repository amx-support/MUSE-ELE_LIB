# MUSEでのWAIT処理の実装

### 機能
MUSEでNetlinxライクなWAIT処理を実行する。

### 使用方法

プログラムフォルダに **ele_libフォルダ** をコピーし、メインプログラムから **import** します。
- muse_wait.py

##### オブジェクト生成

`wt = muse_wait.Wait()`<br/><br/>


##### 指定時間WAIT

`wt.wait(time,func,args,name)`<br/><br/>

指定時間が経過すると処理が実行されます。<br/>
実行する内容は関数(引数使用可)で指定します。<br/>
プログラムの同一箇所のWAITや同名のWAITは多重登録されません。<br/>
**time**は時間を指定します。(1=0.1秒)<br/>
**func**は実行する関数の名前を指定します。<br/>
**args**は実行する関数の引数をリストで指定します。(省略可)<br/>
**name**はWAITの名前を指定します。(省略可。引数を省略した場合は`name="hoge"`の形式で指定)<br/><br/>


##### 条件付きWAIT

`wt.wait_until(flag_func,func,args,name)`<br/><br/>

条件に指定した関数の戻り値がTrueになると処理が実行されます。<br/>
条件は関数(引数使用不可)で指定します。<br/>
実行する内容は関数(引数使用可)で指定します。<br/>
プログラムの同一箇所のWAITや同名のWAITは多重登録されません。<br/>
**flag_func**は実行条件となる関数を指定します。(Trueで実行)<br/>
**func**は実行する関数の名前を指定します。<br/>
**args**は実行する関数の引数をリストで指定します。(省略可)<br/>
**name**はWAITの名前を指定します。(省略可。引数を省略した場合は`name="hoge"`の形式で指定)<br/><br/>


##### 指定時間条件付きWAIT

`wt.timed_wait_until(flag_func,time,func,args,name)`<br/><br/>

制限時間内に条件に指定した関数の戻り値がTrueになると処理が実行されます。<br/>
条件は関数(引数使用不可)で指定します。<br/>
実行する内容は関数(引数使用可)で指定します。<br/>
プログラムの同一箇所のWAITや同名のWAITは多重登録されません。<br/>
**flag_func**は実行条件となる関数を指定します。(Trueで実行)<br/>
**time**は制限時間を指定します。(1=0.1秒)
**func**は実行する関数の名前を指定します。<br/>
**args**は実行する関数の引数をリストで指定します。(省略可)<br/>
**name**はWAITの名前を指定します。(省略可。引数を省略した場合は`name="hoge"`の形式で指定)<br/><br/>


##### 指定時間WAITのキャンセル(名前指定)

`wt.cancel_wait(name)`<br/><br/>

指定時間WAITを名前を指定してキャンセルします。<br/>
**name**はWAITの名前を指定します。<br/><br/>


##### 条件付きWAIT系のキャンセル(名前指定)

`wt.cancel_wait_until(name)`<br/><br/>

条件付きWAIT系(wait_until,timed_wait_until)を名前を指定してキャンセルします。<br/>
**name**はWAITの名前を指定します。<br/><br/>


##### 指定時間WAITをすべてキャンセル

`wt.cancel_all_wait()`<br/><br/>

指定時間WAITをすべてキャンセルします。<br/>
名前あり・なしに関わらずキャンセルされますが、条件付きWAIT系はキャンセルされません。<br/><br/>


##### 条件付きWAIT系をすべてキャンセル

`wt.cancel_all_wait_until()`<br/><br/>

条件付きWAIT系(wait_until,timed_wait_until)をすべてキャンセルします。<br/>
名前あり・なしに関わらずキャンセルされますが、指定時間WAITはキャンセルされません。<br/><br/>
