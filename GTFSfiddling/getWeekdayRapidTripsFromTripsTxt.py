import csv

def getRouteIDList(type):
    routeIDs =[]

    if type == 'Rapid':
        for i in [704,705,710,720,728,733,734,740,741,745,750,751,754,757,760,761,762,770,780,794]:
            routeIDs.append(str(i) + '-13074')
    elif type == 'Transitway':
        for i in [901, 910]:
            routeIDs.append(str(i) + '-13074')
    elif type == 'Rail':
        for i in range(801, 807):
            routeIDs.append(str(i))

    return routeIDs


# returns a list of dicts from csv stuff
def getWeekdayTripsOfTypeFromFile(filename, type):

    csvfile = open(filename, newline='')

    thisReader = csv.DictReader(csvfile)

    typeRouteIDs = getRouteIDList(type)

    weekdayTypeTrips = []

    for entry in thisReader:
        if '1_Weekday' in entry['service_id']:
            if entry['route_id'] in typeRouteIDs:
                weekdayTypeTrips.append(entry)

    csvfile.close()

    return weekdayTypeTrips


def getTripIDs(trips):
    trip_ids = []
    for trip in trips:
        trip_ids.append(trip['trip_id'])
    return trip_ids


def stopsDict():
    csvfile = open("stops.csv")
    thisReader = csv.DictReader(csvfile)

    stops = []
    for entry in thisReader:
        newDict = {'stop_id' : entry['stop_id']}
        stops.append(newDict)

    csvfile.close()

    return stops


def getRouteID(tripID, trips):
    for trip in trips:
        if trip['trip_id'] == tripID:
            return trip['route_id']


def stopCounter(tripsOfInterest, allStops, stop_timesFilename):
    csvfile = open(stop_timesFilename)
    thisReader = csv.DictReader(csvfile)

    tripsOfInterest_id = getTripIDs(tripsOfInterest)

    for entry in thisReader:
        if entry['trip_id'] in tripsOfInterest_id:
            for stop in allStops:
                if stop['stop_id'] == entry['stop_id']:
                    routeAtStop = getRouteID(entry['trip_id'], tripsOfInterest)
                    if routeAtStop in stop.keys():
                        stop[routeAtStop] += 1
                    else:
                        stop[routeAtStop] = 1

    return allStops


def writeStopsCounted(allStopsCounted, filename, type):

    typeRouteIDs = getRouteIDList(type)

    fieldnames = []
    fieldnames.append('stop_id')
    for routeID in typeRouteIDs:
        fieldnames.append(routeID)

    csvfile = open(filename, 'w', newline='')
    thisWriter = csv.DictWriter(csvfile, fieldnames)
    thisWriter.writeheader()
    for item in allStopsCounted:
        if len(item) > 1:
            thisWriter.writerow(item)

    csvfile.close()


def main():
    # Replace 'Rapid' with 'Transitway' or 'Rail' in main() to generate counts for those modes.

    weekdayRapidTrips = getWeekdayTripsOfTypeFromFile(filename='trips.csv', type='Rapid')
    print(weekdayRapidTrips)  # for debugging/monitoring
    weekdayRapidTripIDs = getTripIDs(weekdayRapidTrips)
    print(weekdayRapidTripIDs)  # for debugging/monitoring
    allstops = stopsDict()
    print(allstops)  # for debugging/monitoring
    allStopsCounted = stopCounter(tripsOfInterest=weekdayRapidTrips, allStops=allstops, stop_timesFilename="stop_times.csv")
    print(allStopsCounted)  # for debugging/monitoring
    writeStopsCounted(allStopsCounted, 'rapidStopsCounted.csv', type='Rapid')


main()