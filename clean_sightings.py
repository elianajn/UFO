import csv
from geopy.geocoders import ArcGIS
import traceback


class Clean_sightings():
    def __init__(self):
        self.header = []
        self.rows = []
        self.cleaned = []

    def read(self):
        file = open('raw_data/scrubbed.csv', 'r')
        csvreader = csv.reader(file)
        self.header = next(csvreader)
        print(self.header)
        for row in csvreader:
            self.rows.append(row)
        # print(self.rows)
        file.close()

    def clean(self):
        geolocator = ArcGIS(scheme="https")
        for e in self.rows:
            # print(e[3])
            if e[3] == "": # if there is no country code, must reverse geocode using lat/long
                # try:
                lat = str(e[9])
                long = str(e[10])
                print((lat, long))
                location = geolocator.reverse((lat, long), timeout=5)
                # except:
                #     traceback.print_exc()
                # print(location.raw['CountryCode'])
                if location.raw['CountryCode'] == "USA":
                    self.cleaned.append(e)
            elif e[3] == "us":
                self.cleaned.append(e)
        print(self.cleaned)


    def write(self):
        with open ('raw_data/cleaned_scrubbed.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(self.header)
            for row in range(len(self.cleaned)):
                spamwriter.writerows(self.cleaned[row])
        csvfile.close()

if __name__ == "__main__":
    clean = Clean_sightings()
    clean.read()
    clean.clean()
    clean.write()
