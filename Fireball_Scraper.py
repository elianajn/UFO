from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback
import pickle

class Fireball_Scraper:
    def __init__(self):
        self.link = "https://fireball.amsmeteors.org/members/imo_view/browse_events?country=236%7CUnited+States&year=2022&num_report_select=&event=&event_id=&event_year=&num_report=5"
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("ignore-certificate-errors")
        chrome_options.add_argument("user-data-dir=selenium")
        s = Service('/usr/local/bin/chromedriver')
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=s,options=chrome_options)
        self.data_to_collect = {}
        self.data = {}
        self.links = []


    def get_events(self):
        next_page = True
        while(next_page):
            next_page = False
            text = self.driver.page_source
            soup = BeautifulSoup(text, 'html.parser')
            self.link = None
            for link in soup.find_all('a'):
                # print(link)
                if link.get('href') is not None:
                    if "/members/imo_view/event/" in link['href']:
                        # self.data[link.text[1:]] = {}
                        # self.data[link.text[1:]]["event"] = link.text[1:]
                        # self.data[link.text[1:]]["link"] = "https://fireball.amsmeteors.org/{}".format(link['href'])
                        self.data_to_collect[link.text[1:]] = "https://fireball.amsmeteors.org/{}".format(link['href'])
                    if "next" in link.text:
                        element = self.driver.find_element(By.PARTIAL_LINK_TEXT, "next")
                        element.click()
                        next_page = True
                        break


    def get_pages(self):
        main_page = 'https://www.amsmeteors.org/fireballs/fireball-report/'
        self.driver.get(main_page)
        logs = self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Fireball Sightings Log')
        links = {}
        for year in logs:
            links[year.text] = year.get_attribute('href')
        for year in links:
            self.driver.get(links[year])
            dropdown = self.driver.find_element(By.CLASS_NAME, 'form-group')
            for option in dropdown.find_elements(By.TAG_NAME, 'option'):
                if option.text == 'United States':
                    option.click()
                    break
            self.get_events()
            self.collect_data()
            self.data_to_collect = {}
            # pickle.dump(self.data, open("fireball_data.p", "wb"))
            print("{} completed and dumped".format(year))
            # break
        self.driver.quit()


    def collect_data(self):
        for item in self.data_to_collect:
            link = self.data_to_collect[item]
            self.driver.get(link)
            text = self.driver.page_source
            try:
                lat = re.findall(r'impact_lat":([0-9]*\.[0-9]*),', text)
                long = re.findall(r'impact_long":(-*[0-9]*\.[0-9]*),', text)
                tstamp = (re.findall(r'on ([A-Z][a-z]*, [A-Z][a-z]* [0-9]{1,2}[a-z]{2} [0-9]{4}) around ([0-9]{2}:[0-9]{2} UT)', text))
                day = str(tstamp[0][0])
                date = day[day.find(", ")+2:]
                date = re.findall(r'([a-z]* [0-9]{1,2})[a-z]{2}( [0-9]{4})', date, re.I)
                date = "{}{}".format(date[0][0], date[0][1])
                date = str(datetime.strptime(date, '%B %d %Y')).split(" ")[0]
                time = str(tstamp[0][1])
                self.data[item] = {}
                self.data[item]["link"] = self.data_to_collect[item]
                self.data[item]["lat"] = lat
                self.data[item]["long"] = long
                self.data[item]["date"] = date
                self.data[item]["time"] = time
                pickle.dump(self.data, open("fireball_data.p", "wb"))
            except:
                traceback.print_exc()
                print(len(self.data))
                print(link)
        # self.driver.quit()

        

if __name__ == "__main__":
    scraper = Fireball_Scraper()
    try:
        scraper.get_pages()
        print(len(scraper.data))
    except:
        traceback.print_exc()
        print(scraper.driver.current_url)
        scraper.driver.quit()
    
