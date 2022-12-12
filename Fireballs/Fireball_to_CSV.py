import pickle
import csv

data = pickle.load(open("fireball_data.p", "rb"))
sum = 0
invalid = 0
columns = ['Event', 'Lat', 'Long', 'Date', 'Time', 'Report']
with open('Fireballs.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=',', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
    writer.writeheader()
    for event in data:
        if data[event]['lat'] == []:
            invalid += 1
            continue
        row = {'Event':event, 'Lat':data[event]['lat'][0], 'Long':data[event]['long'][0], 'Date':data[event]['date'], 'Time':data[event]['time'], 'Report':data[event]['link']}
        writer.writerow(row)
        sum += 1
    csvfile.close()
    print("Sum: {}, Invalid: {}".format(sum, invalid))
