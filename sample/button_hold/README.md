# ButtonのHold処理の実装

### 機能
NetLinxプログラムの**BUTTON_EVENT-HOLD**に相当するボタン押し続け処理を行う。

### 使用方法

プログラムフォルダに **ele_libフォルダ** をコピーし、メインプログラムから **import** します。
- button_hold.py
<br/>
Hold処理用の関数を用意し、イベント処理の登録を行います。<br/>

`button_hold.Hold(dvTP.button[1],HoldEvent,0.3,1.0,True)`<br/><br/>

##### Hold処理の実行

`button_hold.Hold(button,event,holdtime,delaytime,repeat)`<br/><br/>
**button**はHoldを行うボタンを指定<br/>
**event**はHold処理用のコールバック関数を指定<br/>
**holdtime**は押し続け時間を指定 (単位：秒 初期値0.5)<br/>
**delaytime**は押し続けを検知するまでの時間を指定 (単位：秒 初期値0.0)<br/>
**repeat**は繰り返しを行うかを指定 (True=繰り返し / False=1回限り)

**holdtime=1.0 / delaytime=0.0 / repeat=True の場合**<br/>
ボタン押下後1.0秒間隔で繰り返しHold処理を実行<br/><br/>

**holdtime=0.3 / delaytime=1.0 / repeat=True の場合**<br/>
ボタン押下から1.0秒後に一度だけHold処理を実行、それ以降は0.3秒間隔で繰り返しHold処理を実行
