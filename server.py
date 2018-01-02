from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ParseMode
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler
from transitions.extensions import GraphMachine
import logging

from func import TocFunction

class TocMachine(GraphMachine):
    def __init__(self):
        self.machine = GraphMachine(
            model = self,
            states=[
                'welcome',
                'entry',
                'outside',
                'intro',
                'inside',
                'service',
                'google',
                'youtube',
                'screenshot'
            ],
            transitions=[
                {
                    'trigger': 'forward',
                    'source': 'welcome', 'dest': 'entry',
                },
                {
                    'trigger': 'forward', 'conditions': 'going_outside',
                    'source': 'entry', 'dest': 'outside'
                },
                {
                    'trigger': 'forward', 'conditions': 'going_intro',
                    'source': 'outside', 'dest': 'intro'
                },
                {
                    'trigger': 'forward', 'conditions': 'intro_repeat',
                    'source': 'intro', 'dest': 'intro'
                },
                {
                    'trigger': 'forward', 'conditions': 'going_inside',
                    'source': 'entry', 'dest': 'inside'
                },
                {
                    'trigger': 'wrong',
                    'source': 'inside', 'dest': 'outside'
                },
                {
                    'trigger': 'forward', 'conditions': 'going_service',
                    'source': 'inside', 'dest': 'service'
                },
                {
                    'trigger': 'forward', 'conditions': 'going_google',
                    'source': 'service', 'dest': 'google'
                },
                {
                    'trigger': 'forward', 'conditions': 'google_repeat',
                    'source': 'google', 'dest': 'google'
                },
                {
                    'trigger': 'forward', 'conditions': 'going_youtube',
                    'source': 'service', 'dest': 'youtube'
                },
                {
                    'trigger': 'forward', 'conditions': 'youtube_repeat',
                    'source': 'youtube', 'dest': 'youtube'
                },
                {
                    'trigger': 'forward', 'conditions': 'going_screenshot',
                    'source': 'service', 'dest': 'screenshot'
                },
                {
                    'trigger': 'forward', 'conditions': 'screenshot_repeat',
                    'source': 'screenshot', 'dest': 'screenshot'
                },
                {
                    'trigger': 'back',
                    'source': ['outside', 'inside'], 'dest': 'entry'
                },
                {
                    'trigger': 'back',
                    'source': ['google', 'youtube', 'screenshot'], 'dest': 'service'
                },
                {
                    'trigger': 'restart',
                    'source': [
                        'welcome',
                        'entry',
                        'outside',
                        'intro',
                        'inside',
                        'service',
                        'google',
                        'youtube',
                        'screenshot'
                    ],
                    'dest': 'entry'
                }
            ],
            initial='welcome',
            auto_transitions=True,
            show_conditions=True
        )
    # 選擇表裏
    def on_enter_entry(self, bot, update):
        print("進入entry")
        reply_keyboard = [["表", "裏"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("需要什麼服務？", reply_markup=reply_markup)
    # 表
    def going_outside(self, bot, update):
        print("檢查outside:" + update.message.text)
        if "表" == update.message.text:
            return True
    def on_enter_outside(self, bot, update):
        print("進入outside")
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        update.message.reply_photo(photo="https://i.imgur.com/6MvWENN.png") # 伊格爾
        reply_keyboard = [["繼續", "返回", "重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("看來是\"普通的\"客戶啊...", reply_markup=reply_markup)
    # 介紹persona
    def going_intro(self, bot, update):
        print("檢查intro:" + update.message.text)
        return "繼續" == update.message.text
    def on_enter_intro(self, bot, update):
        print("進入intro")
        reply_keyboard = [["重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("想了解我們，就到以下網站吧~", reply_markup=reply_markup)
        reply_keyboard2 = [[InlineKeyboardButton("P5 PS4官方網站", url="http://persona5.jp/")],
                        [InlineKeyboardButton("P5D和P3D PS4官方網站", url="http://persona-dance.jp/")],
                        [InlineKeyboardButton("凱薩琳 PS4官方網站", url="http://fullbody.jp/")],
                        [InlineKeyboardButton("P5 動畫官方網站", url="http://p5a.jp/")],
                        [InlineKeyboardButton("女神異聞錄系列 中文維基", url="https://zh.wikipedia.org/wiki/女神異聞錄系列")]]
        reply_markup2 = InlineKeyboardMarkup(reply_keyboard2)
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        update.message.reply_photo(photo=open("img/morgana.jpg", "rb"), reply_markup=reply_markup2) # 摩兒迦納
    def intro_repeat(self, bot, update): # 不會繼續forward
        return False
    # 裏
    def going_inside(self, bot, update):
        print("檢查inside:" + update.message.text)
        return "裏" == update.message.text
    def on_enter_inside(self, bot, update):
        print("進入inside")
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        update.message.reply_photo(photo="https://i.imgur.com/6MvWENN.png") # 伊格爾
        reply_keyboard = [["返回", "重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("想必帶來了不錯的回答吧...", reply_markup=reply_markup)
    # 選擇裏服務
    def going_service(self, bot, update):
        print("檢查service:" + update.message.text.lower())
        if "persona" == update.message.text.lower():
            return True
        else:
            self.wrong(bot, update) # 答錯直接跳至outside
    def on_enter_service(self, bot, update):
        print("進入service")
        reply_keyboard = [["關鍵字搜尋", "影片搜尋", "網頁截圖"],
                        ["返回", "重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("謹遵差遣...", reply_markup=reply_markup)
    # google關鍵字搜尋
    def going_google(self, bot, update):
        print("檢查google:" + update.message.text)
        return "關鍵字搜尋" == update.message.text
    def on_enter_google(self, bot, update):
        print("進入google")
        reply_keyboard = [["返回", "重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("給我們一個關鍵字，後面接分號(;)加數字可以決定顯示資料數", reply_markup=reply_markup)
    def google_repeat(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        text = update.message.text
        key = text.split(';', 1)[0] # 關鍵字
        num = 3
        num = text.split(';', 1)[1] # 資料數
        num = int(num)
        func = TocFunction()
        result = func.google(key, num)
        for i in range(num):
            text = "[" + result[0][i] + "]" + "(" + result[1][i] + ")" # 用成markdown語法
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return True
    # youtube影片搜尋
    def going_youtube(self, bot, update):
        print("檢查youtube:" + update.message.text)
        return "影片搜尋" == update.message.text
    def on_enter_youtube(self, bot, update):
        print("進入youtube")
        reply_keyboard = [["返回", "重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("給我們一個關鍵字，後面接分號(;)加數字可以決定顯示資料數", reply_markup=reply_markup)
    def youtube_repeat(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        text = update.message.text
        key = text.split(';', 1)[0] # 關鍵字
        num = 3
        num = text.split(';', 1)[1] # 資料數
        num = int(num)
        func = TocFunction()
        result = func.youtube(key, num)
        for i in range(num):
            text = "[" + result[0][i] + "]" + "(" + result[1][i] + ")"
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text("附帶一提，將網址的youtunbe加上to，將會自動導向至下載連結")
        return True
    # 網頁截圖(無捲動)
    def going_screenshot(self, bot, update):
        print("檢查screenshot:" + update.message.text)
        return "網頁截圖" == update.message.text
    def on_enter_screenshot(self, bot, update):
        print("進入screenshot")
        reply_keyboard = [["返回", "重頭"]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("給我們一個網址，我們會提供客人您網站截圖", reply_markup=reply_markup)
    def screenshot_repeat(self, bot, update):
        site = update.message.text
        func = TocFunction()
        if func.screenshot(site):
            bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
            update.message.reply_photo(photo=open("img/screenshot.png", "rb"))
        return True
    # 畫state diagram
    def draw(self):
        self.get_graph().draw('img/diagram.png', prog='dot')

machine = TocMachine()

# 除錯用
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def start(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    update.message.reply_photo(photo="https://i.imgur.com/Awb2lFA.jpg")
    update.message.reply_text("有事找怪盜團前，不妨先來點音樂吧？")
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_AUDIO)
    update.message.reply_audio(audio="https://goo.gl/h88yto")
    machine.restart(bot, update) # 跑到entry

def echo(bot, update):
    text = update.message.text
    if text == "返回":
        machine.back(bot, update)
    elif text == "重頭":
        machine.restart(bot, update)
    elif text == "state":
        state = machine.state
        update.message.reply_text("目前state為: " + state)
    elif text == "fsm":
        machine.draw()
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        update.message.reply_photo(photo=open("img/diagram.png", "rb"))
    else:
        machine.forward(bot, update)

# 沒被處理的command
def unknown(bot, update):
    update.message.reply_text("慎選你的發言...")

# 可收到telegram的error
def error(bot, update, error):
    logger.warning("Update '%s' caused error '%s'", update, error)

def main():
    # 建立event handler
    updater = Updater("527954221:AAEi036WqXGAAqsnpOxX8EYMkm1n7taLcFs")
    # 註冊handler
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)
    # 開啟bot
    updater.start_polling(clean=True)
    # 接收SIGINT、SIGTERM、SIGABRT時會先關閉thread再退出
    updater.idle()

if __name__ == "__main__":
    main()
