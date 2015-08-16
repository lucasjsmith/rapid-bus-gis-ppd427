import csv

csvfile = open("trips.csv", newline='')

thisReader = csv.DictReader(csvfile)

rapidRouteIDs = []
for i in range (700, 800):
    rapidRouteIDs.append(str(i))
    rapidRouteIDs.append(str(i) + '-13074')

print(rapidRouteIDs)

weekdayRapidTrips = []

for entry in thisReader:
    if '1_Weekday' in entry['service_id']:
        if entry['route_id'] in rapidRouteIDs:
            weekdayRapidTrips.append(entry)
            print(entry)

print(weekdayRapidTrips)


csvfile.close()