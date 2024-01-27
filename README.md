# Roomba_ml_conyrol
## 概要
2023年度制御工学特論の最終レポートに向けて，深層学習と強化学習を用いてRoombaを制御する試みを行った．

## メンバー
現在は以下のメンバーで開発した．
| group | number | クラス | 氏名 | シメイ | 研究室 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 2 |	6302285	|	1M1002	|	青木　敦郎	|	アオキ　アツロウ		|	土居研	|
| 2 |	6300537	|	1M1026	|	垣内　皐良	|	カイトウ　タカラ		|	竹井研	|
| 1 |	6302012	|	1M1033	|	四之宮　啓悟	|	シノミヤ　ケイゴ		|	土居研	|
| 1 |	6300607	|	1M1066	|	山崎　楓	|	ヤマザキ　カエデ		|	土居研	|


## それぞれのファイルの機能について
### Roomba_Q_Learning.ipynb
Roombaのシミュレータと，シミュレータを用いてQ学習を行わせるためのNotebook.

### Roomba_Q_inference.ipynb
`Roomba_Q_Learning.ipynb`で学習させたQ_tableの推論テストを行わせるためのNotebook.

### Roomba_DQN.ipynb
当初，DQNを使ってRoombaを学習させようとした名残．

### object_detection_webcam3.py
yolo-V8の学習済みのモデルを用いて，ボールを検出し，ボールとの相対角度と相対距離をUDP通信で送信する．

### Roomba_Q_ctrl.py
`object_detection_webcam3.py`から，ボールとの相対角度と相対距離を受信し，`action_decision.py`より行動を決定してRoombaを動作させる．

### action_decision.py
Qテーブルを読み込み，`Roomba_Q_ctrl.py`を介して得たRoombaの状態より，Qテーブルから適切な行動を返す．