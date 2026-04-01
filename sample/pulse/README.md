# MUSEでのPULSE動作の実装 v1.1

### 機能
**MUSE(idevice)** / **CEシリーズ** / **NetLinx系デバイス** のチャンネル制御でPULSEを実行します。
同一のPULSEは多重登録されず、個別に時間を設定できます。

### 使用方法

プログラムフォルダに **ele_libフォルダ** をコピーし、メインプログラムから **import** します。

##### オブジェクト生成

`pl = pulse.Pulse()`

##### PULSE実行

###### MUSE Relay / CE-REL8<br/>
`pl.pulse_muse_relay(デバイス,チャンネル,時間)`

チャンネルは0番から<br/>
時間は0.1秒単位<br/><br/>

###### MUSE IR / CE-IRS8<br/>
`pl.pulse_muse_ir(デバイス,チャンネル,時間)`

チャンネルは1番から<br/>
時間は0.1秒単位<br/><br/>

###### MUSE I/O / CE-IO4<br/>
`pl.pulse_muse_io(デバイス,チャンネル,時間)`

チャンネルは0番から<br/>
時間は0.1秒単位<br/><br/>

###### NetLinx系<br/>
`pl.pulse_netlinx(デバイス,チャンネル,時間)`

チャンネルは1番から<br/>
時間は0.1秒単位<br/>
