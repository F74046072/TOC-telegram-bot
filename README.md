# **TOC 2017 Project: Telegram Chat Bot**
---
## 目的
~~業配persona~~，讓一般用戶可以知道**persona**的有趣之處，也能讓進階用戶可以使用**怪盜團**所提供的進階功能:smiley:
## 事前準備
### 軟體
* Python 3
* Google Chrome
    * 最好是安裝在預設路徑
* chromedriver
    * repo裡附的webdriver是windows版本，請自行到[seleniumhq](http://www.seleniumhq.org/download/)下載對應的webdriver
### 安裝套件
```sh
pip3 install -r requirements.txt
```
* pygraphviz (For visualizing Finite State Machine)
    * [在Ubuntu安裝pygraphviz](http://www.jianshu.com/p/a3da7ecc5303)
### bot設置
修改 server.py
```python=
def main():
    Updater("改為你從bot father獲得的API token")
```
### 測試環境
```
Linux version 4.4.0-43-Microsoft (Microsoft@Microsoft.com) (gcc version 5.4.0 (GCC) )
```
> Windows10的Linux子系統
## 使用說明
### 執行server
```sh
python3 server.py
```
### State Machine
[原始圖片](https://i.imgur.com/ZIPwxpD.png)
![Imgur](https://i.imgur.com/ZIPwxpD.png)
### 功能
* 表服務
    * persona介紹
    * persona5角色抽抽樂
* 裏服務
    * google關鍵字搜尋(可調整顯示資料數)
    * youtube影片搜尋(可調整顯示資料數)，並附上自動導向的下載網址
    * 網頁截圖(不含捲動)
### 詳細步驟
確認好開啟server並設置好API token後，以下以我的bot以及使用桌面版telegram為例
* 先開啟telegram，搜尋設置好的bot
![Imgur](https://i.imgur.com/fTek7jo.png)

* /start後會進到歡迎畫面並可選擇服務，同時也是所有state重頭開始的點，手機版需注意一下鍵盤的部分
(若需要圖片和音樂需再次/start)
![Imgur](https://i.imgur.com/3ZCYpx7.png)

* 進入表服務，要注意的是，在有選擇的情形下，亂打字並不會做出任何回應，請善用提供的選項，此外這也是裏服務打錯通關密語所回到的地方
![Imgur](https://i.imgur.com/nENWm29.png)
* 除了基本的介紹連結
![Imgur](https://i.imgur.com/43gR4eq.png)
* 也可以玩角色抽抽樂
![Imgur](https://i.imgur.com/tNwbqQc.png)
* 進入裏服務，通關密語大小寫互通，答錯會直接進入表服務
![Imgur](https://i.imgur.com/qCCfwSw.png)
* 選擇好需要的服務後，系統便會提示要輸入的內容
![Imgur](https://i.imgur.com/FXt3X7N.png)
* server這邊處理好後會將結果回傳，網址會以markdown語法呈現
![Imgur](https://i.imgur.com/aSGEZCA.png)
* youtube會額外附上下載的連結
![Imgur](https://i.imgur.com/dLPpd1G.png)
* 至於網頁截圖需要先提供一個網址，會直接將擷取到的圖片回傳
![Imgur](https://i.imgur.com/G1Wjv40.png)
* 最後，隨時都可以輸入state和fsm兩個指令來獲取現在的狀態
![Imgur](https://i.imgur.com/uJDB2E3.png)