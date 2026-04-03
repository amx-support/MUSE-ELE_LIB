# MUSEでのUDPサーバー通信の実装

### 機能
UDPサーバー通信を行います。<br/>
URLとポートを指定して送信を行うこともできます。<br/><br/>

### 使用方法

プログラムフォルダに **ele_libフォルダ** をコピーし、メインプログラムから **import** します。<br/>

##### オブジェクト生成

`udp = udp_server.UdpServer(device,recv_port,receive_bytes)`

|引数|型|説明|
|-|-|-|
|device|str|識別用ID イベント処理などで対象を識別する為に使用|
|recv_port|int|受信IPポート番号|
|receive_bytes|int|最大受信バイト数 (デフォルト:1024)|


##### クラスメソッド<br/>

###### インスタンス確認<br/>
`dev(device)`

|引数|型|説明|
|-|-|-|
|device|str|識別用ID|

識別用IDから生成済みのインスタンスを取得する


##### インスタンスメソッド<br/>

###### ソケットオープン<br/>
`open()`

サーバーをオープンし待ち受けを開始する

###### ソケットクローズ<br/>
`close()`

サーバーをクローズし待ち受けを終了する

###### 送信<br/>
`send(address,port,command)`

|引数|型|説明|
|-|-|-|
|address|str|送信先URL|
|port|int|送信先IPポート番頭|
|command|strまたはbytes|送信するデータ|

指定先にデータ送信する<br/>
**事前にサーバーをオープンしておく必要があることに注意**

###### ONLINEイベント登録<br/>
`online(func)`

|引数|型|説明|
|-|-|-|
|func|関数|コールバック関数|

ONLINEイベント用のコールバック関数を登録する

###### OFFLINEイベント登録<br/>
`offline(func)`

|引数|型|説明|
|-|-|-|
|func|関数|コールバック関数|

OFFLINEイベント用のコールバック関数を登録する

###### データ受信イベント登録<br/>
`listen(func)`

|引数|型|説明|
|-|-|-|
|func|関数|コールバック関数|

データ受信イベント用のコールバック関数を登録する<br/>
**receive.listen()ではないので注意**

###### ONERRORイベント登録<br/>
`onerror(func)`

|引数|型|説明|
|-|-|-|
|func|関数|コールバック関数|

ONERRORイベント用のコールバック関数を登録する

###### オンライン状態の確認<br/>
`isOnline()`

ONLINEの場合**True**が、OFFLINEの場合**False**が戻る

###### オフライン状態の確認<br/>
`isOffline()`

OFFLINEの場合**True**が、ONLINEの場合**False**が戻る


##### イベントパラメータ<br/>

###### ONLINEイベント<br/>

|引数|型|説明|
|-|-|-|
|source|インスタンス|対象のインスタンス|
|device|str|識別用ID|
|id|str|online|
|path|str|UdpServer/online|
|value|bool|True|

###### OFFLINEイベント<br/>

|引数|型|説明|
|-|-|-|
|source|インスタンス|対象のインスタンス|
|device|str|識別用ID|
|id|str|offline|
|path|str|UdpServer/offline|
|value|bool|False|

###### 受信イベント<br/>

|引数|型|説明|
|-|-|-|
|source|インスタンス|対象のインスタンス|
|device|str|識別用ID|
|id|str|receive|
|path|str|UdpServer/receive|
|value|bool|True|
|arguments["data"]|bytes|受信データ|
|arguments["length"]|int|受信データの長さ|
|arguments["address"]|str|送信元URL|
|arguments["port"]|int|送信元IPポート|

###### ONERRORイベント<br/>

|引数|型|説明|
|-|-|-|
|source|インスタンス|対象のインスタンス|
|device|str|識別用ID|
|id|str|メソッド名|
|path|str|UdpServer/メソッド名|
|value|int|エラーコード|
|arguments["text"]|str|エラーの内容|

|コード|定数|説明|
|-|-|-|
|1|ERR_SOCK_OPEN|すでにソケットが開いている|
|2|ERR_SOCK_NOT_OPEN|ソケットが開かれていない|
|3|ERR_SOCK_CONNECTION_REFUSED|接続が拒否された|
|4|ERR_SOCK_NO_ROUTE|ルートがない (相手がいない、MUSE側のLAN抜け)|
|5|ERR_SOCK_TIMEOUT|接続タイムアウト|
|6|ERR_SOCK_ADDR_ALREADY_IN_USED|ポートバインド失敗|
|21|ERR_SEND_INVALID_ARGS|送信データの型が不正 (str, bytesのみ)|
