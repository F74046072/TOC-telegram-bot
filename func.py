from selenium import webdriver
from bs4 import BeautifulSoup
import random

class TocFunction():
    def google(self, key, num):
        driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
        driver.get("http://www.google.com/xhtml") # google搜尋
        search_box = driver.find_element_by_name('q')
        search_box.send_keys(key)
        search_box.submit()
        pageSource = driver.page_source # 取得網頁原始碼
        soup = BeautifulSoup(pageSource, 'lxml') # 解析器接手
        # 二維list，前面放名稱，後面放網址
        result = [[0 for y in range(num)] for i in range(2)]
        for k in range(num):
            block = soup.select('h3[class="r"] a')[k] # 略過圖片搜尋結果
            result[0][k] = block.get_text() # 標題文字
            result[1][k] = block['href'] # 超連結
        driver.quit()
        return result

    def youtube(self, key, num):
        driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
        driver.get("https://www.youtube.com") # google搜尋
        search_box = driver.find_element_by_name('search_query')
        search_box.send_keys(key) # 關鍵字
        search_box.submit()
        pageSource = driver.page_source # 取得網頁原始碼
        soup = BeautifulSoup(pageSource, 'lxml') # 解析器接手
        # 二維list，前面放名稱，後面放網址
        result = [[0 for y in range(num)] for i in range(2)]
        for k in range(num):
            block = soup.select('h3 a')[k] # 略過廣告
            result[0][k] = block['title'] # 標題文字
            result[1][k] = "https://www.youtube.com" + block['href'] # 超連結
        driver.quit()
        return result

    def screenshot(self, site):
        try:
            driver = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")
            driver.get(site)
            driver.maximize_window()
            driver.save_screenshot("img/screenshot.png") # 保存截圖
            driver.quit()
        except:
            driver.quit()
            return False
        return True

    def slot(self):
        character = ["女帝（奧村春）", "女教皇（新島真）", "太陽（吉田寅之助）", "月（三島由輝）",
                "正義（明智吾郎）", "刑死者（岩井宗久）", "死神（武見妙）", "命運（御船千早）",
                "法王（佐倉惣治郎）", "星（東鄉一二三）", "皇帝（喜多川祐介）", "剛毅（雙子）",
                "惡魔（大宅一子）", "塔（織田信也）", "愚者（主角）", "節制（川上貞代）",
                "審判（新島冴）", "戰車（坂本龍司）", "隱者（佐倉雙葉）", "魔術師（摩爾加納）", "戀愛（高卷杏）"]
        num = random.randint(0,20)
        return character[num]
