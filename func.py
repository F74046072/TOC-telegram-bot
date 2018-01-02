from selenium import webdriver
from bs4 import BeautifulSoup

class TocFunction():
    def google(self, key, num):
        driver = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe')
        driver.get('http://www.google.com/xhtml') # google搜尋
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
        driver = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe')
        driver.get('https://www.youtube.com') # google搜尋
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
        driver = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe')
        driver.get(site)
        driver.maximize_window()
        driver.save_screenshot('img/screenshot.png') # 保存截圖
        driver.quit()
        return True
