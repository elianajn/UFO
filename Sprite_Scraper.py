from pkgutil import get_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re

class Sprite_Scraper():
    def __init__(self):
        self.driver = None
        self.link = "https://spaceweathergallery.com/index.php?title=sprite"
        self.list = []

    def scrape_pages(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("ignore-certificate-errors")
        chrome_options.add_argument("user-data-dir=selenium")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=chrome_options)
        self.driver = driver
        while self.link is not None:
            self.driver.get(self.link)
            self.get_data()
            print(self.list)
            try:
                self.link = self.driver.find_element_by_link_text('next').get_attribute('href')
            except:
                self.link = None
            


    def get_data(self):
        text = self.driver.page_source
        soup = BeautifulSoup(text, 'html.parser')
        entries = soup.find_all("div", {"class": "caption none"})
        c = 0
        lst = []
        for e in entries:
            text = str(e.findChildren('p'))
            title = re.search(r'(?<=tempImageTitleThumbText\"\>)(.*)(?=\<\/font)', text)
            split = text.split("<br/>")
            name = split[1]
            datetime = split[2]
            location = split[3][:-5]
            lst.append([title.group(0), name, datetime, location])  
        self.list.append(lst)


    def dump_data(self):
        pass


if __name__ == "__main__":
    scraper = Sprite_Scraper()
    scraper.scrape_pages()

