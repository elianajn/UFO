import pickle
import re
from datetime import datetime
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

geolocator = Nominatim(user_agent='e_neurohr@coloradocollege.edu', timeout=5)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("ignore-certificate-errors")
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_argument("--headless")
s = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=s,options=chrome_options)

failed_data = pickle.load(open('failed_cleaned_sprites.p', 'rb'))
data = pickle.load(open('sprites.p', 'rb'))
for f in failed_data:
    if failed_data[f].get('Lat') == None: # Need to geocode
        try:
            location = failed_data[f]['Location']
            geo = geolocator.geocode(location, addressdetails=True)
            failed_data[f]['Lat'] = geo.raw['lat']
            failed_data[f]['Long'] = geo.raw['lon']
        except:
            print("ENTRY THAT FAILED: {}".format(location))
    driver.get(f)
    photoLocation = driver.find_element(By.CLASS_NAME, 'photoLocationText').text
    year = re.findall(r'([0-9]{4})', photoLocation)[0]
    month = failed_data[f].pop('month')
    day = failed_data[f].pop('day')
    date = str(datetime.strptime("{} {} {}".format(month, day, year), '%b %d %Y')).split(" ")[0]
    failed_data[f]['Date'] = date
    data[f] = failed_data[f]
    # print('{} {}'.format(f, failed_data[f]))
# print(len(data))
pickle.dump(data, open("sprites.p", "wb"))