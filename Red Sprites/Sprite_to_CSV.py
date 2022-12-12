import pickle
import csv

data = pickle.load(open("sprites.p", "rb"))
columns = ['Title', 'Name', 'Date', 'Time', 'Location', 'Lat', 'Long', 'Report']
with open('Sprites.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=',', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
    writer.writeheader()
    for sprite in data:
        row = {'Title':data[sprite]['Title'], 'Name':data[sprite]['Name'], 'Date':data[sprite]['Date'], 'Time':data[sprite]['Time'], 'Location':data[sprite]['Location'], 'Lat':data[sprite]['Lat'], 'Long':data[sprite]['Long'], 'Report':sprite}
        writer.writerow(row)
        print(row)
    csvfile.close()
        