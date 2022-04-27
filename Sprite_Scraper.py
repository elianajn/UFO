from pkgutil import get_data
from socket import timeout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re
from geopy.geocoders import Nominatim
import geocoder
from geopy.geocoders import ArcGIS
import pickle

class Sprite_Scraper():
    def __init__(self):
        self.driver = None
        self.link = "https://spaceweathergallery.com/index.php?title=sprite"
        self.list = []
        # self.list = pickle.load(open("sprites.p", "rb"))

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
            # print(self.list)
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
        with open ('sprites.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Title'] + ['Name'] + ['Datetime'] + ['Location'])
            for row in range(len(self.list)):
                spamwriter.writerows(self.list[row])
        pickle.dump(self.list, open("sprites.p", "wb"))


    def geopy(self):
        # geolocator = Nominatim(user_agent="e_neurohr@coloradocollge.edu")
        # location = geolocator.geocode("Cabo Rojo, Puerto Rico", exactly_one=True)
        # print(geolocator.reverse(location.latitude, location.longitude).address)
        # print(geolocator.reverse(location.latitude, location.longitude))
        geolocator = ArcGIS(scheme="https")
        # location = geocoder.google('Cabo Rojo, Puerto Rico')
        # location = geolocator.geocode('Cabo Rojo, Puerto Rico', out_fields='Country')
        # print(location.raw['attributes']['Country'])
        # for l in location:
        #     print(l)
        for e in self.list:
            for l in e:
                # print(l[-1])
                location = geolocator.geocode(l[-1], out_fields='Country')
                # print(location.raw['attributes']['Country'])
                l.append(location.raw['attributes']['Country'])
                # print(l)

    
    def remove_non_US(self):
        for e in self.list:
            for l in self.list:
                print(l[-1])
                if l[-1] is not 'USA':
                    self.list.remove(l)
        print(self.list)



if __name__ == "__main__":
    scraper = Sprite_Scraper()
    scraper.scrape_pages()
    scraper.geopy()
    scraper.dump_data()
    scraper.remove_non_US()

