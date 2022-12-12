from pkgutil import get_data
from socket import timeout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re
from geopy.geocoders import Nominatim
import geocoder
from geopy.geocoders import ArcGIS
import pickle
import traceback
from datetime import datetime

class Sprite_Scraper():
    def __init__(self):
        self.driver = None
        self.link = "https://spaceweathergallery.com/index.php?title=sprite"
        self.data = {}
        self.failed_geopy = {}
        # self.list = pickle.load(open("sprites.p", "rb"))

    def scrape_pages(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("ignore-certificate-errors")
        chrome_options.add_argument("user-data-dir=selenium")
        chrome_options.add_argument("--headless")
        s = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=s,options=chrome_options)
        self.driver = driver
        while self.link is not None:
            self.driver.get(self.link)
            self.get_data()
            # print(self.list)
            try:
                self.link = self.driver.find_element(By.LINK_TEXT, 'next').get_attribute('href')
            except:
                self.link = None
        print("LENGTH BEFORE REMOVING NON-US: {}".format(len(self.data)))
        self.geopy()
        self.get_year_data()
        pickle.dump(self.failed_geopy, open('failed_sprites.p', 'wb'))
        
            


    def get_data(self):
        text = self.driver.page_source
        soup = BeautifulSoup(text, 'html.parser')
        # entries = soup.find_all("div", {"class": "caption none"})
        rows = self.driver.find_elements(By.ID, 'sidebar')
        
        for row in rows:
            entries = row.find_elements(By.TAG_NAME, 'td')
            for entry in entries:
                if entry.text == '':
                    return
                sprite = {}
                text = entry.text.split('\n')
                sprite['Title'] = text[0]
                # title = text[0]
                sprite['Name'] = text[1]
                sprite['month'] = text[2].split(" ")[0]
                sprite['day'] = text[2].split(" ")[1]
                sprite['Time']= text[2].split(" ")[2]
                sprite['Location'] = text[3]
                # print(entry.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                # entry.find_element(By.TAG_NAME, 'a').click()
                link = entry.find_element(By.TAG_NAME, 'a').get_attribute('href')
                self.data[link] = sprite
                # print(link)
        

        # return
        # for sprite in self.data: # Need to go to the individual page for the year

        #         print(sprite)
        #         self.driver.get(sprite)
        #         photoLocation = self.driver.find_element(By.CLASS_NAME, 'photoLocationText').text
        #         # print(photoLocation)
        #         year = re.findall(r'([0-9]{4})', photoLocation)[0]
        #         print(self.data[sprite])
        #         month = self.data[sprite].pop('month')
        #         day = self.data[sprite].pop('day')
        #         date = str(datetime.strptime("{} {} {}".format(month, day, year), '%b %d %Y')).split(" ")[0]
        #         print(date)

    def get_year_data(self):
        for sprite in self.data:
            self.driver.get(sprite)
            photoLocation = self.driver.find_element(By.CLASS_NAME, 'photoLocationText').text
            year = re.findall(r'([0-9]{4})', photoLocation)[0]
            month = self.data[sprite].pop('month')
            day = self.data[sprite].pop('day')
            date = str(datetime.strptime("{} {} {}".format(month, day, year), '%b %d %Y')).split(" ")[0]
            self.data[sprite]['Date'] = date
            pickle.dump(self.data, open("sprites.p", "wb"))


    def data_to_csv(self):
        with open ('Sprites.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Title'] + ['Name'] + ['Datetime'] + ['Location'])
            for row in range(len(self.only_US)):
                spamwriter.writerows(self.only_US[row])
        pickle.dump(self.only_US, open("sprites.p", "wb"))


    def geopy(self):
        geolocator = Nominatim(user_agent='e_neurohr@coloradocollege.edu', timeout=5)
        keys = list(self.data.keys())
        for sprite in keys:
            location = self.data[sprite]['Location']
            location = location.replace('South German', 'Germany')
            try:
                geo = geolocator.geocode(location, addressdetails=True)
                if geo.raw['address']['country_code'] != 'us':
                    self.data.pop(sprite)
                else:
                    self.data[sprite]['Lat'] = geo.raw['lat']
                    self.data[sprite]['Long'] = geo.raw['lon']
            except:
                    print("ENTRY THAT FAILED: \"{}\", Added to failed_geopy dictionary".format(location))
                    self.failed_geopy[sprite] = self.data.pop(sprite)



if __name__ == "__main__":
    scraper = Sprite_Scraper()
    scraper.scrape_pages()
    print(len(scraper.data))
    

