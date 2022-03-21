import csv
import datetime
import json
import requests

# sending requests and querying for up-to-date data
# shift + option + f to format

API_URL = 'https://skyscanner44.p.rapidapi.com/search'
CSV_HEADERS = ['name', 'price', 'dep_day', 'dep_depart', 'dep_arrive',
               'dep_carrier', 'ret_day', 'ret_depart', 'ret_arrive', 'ret_carrier']
TODAYS_DATE = datetime.date.today().strftime("%m_%d")

with open('../data/input.json') as input:
    input_dict = json.load(input)
with open('../data/secrets.json') as secrets:
    headers = json.load(secrets)

def create_query(departureDate, returnDate, destination, origin='LHR', adults=2, currency='USD', cabinClass='economy'):
    return {
        'adults': adults,
        'origin': origin,
        'destination': destination,
        'departureDate': departureDate,
        'returnDate': returnDate,
        'cabinClass': cabinClass,
        'currency': currency
    }


def get_data_response(querystring, file):
    response = requests.request(
        'GET', API_URL, headers=headers, params=querystring).json()['itineraries']

    for bucket in response['buckets']:
        for flight in bucket['items']:
            result = []
            # add type of itinerary (Best, Cheapest, Fastest, etc.)
            result.append(bucket['name'])
            # add price
            result.append(str(flight['price']['raw']))
            for leg in flight['legs']:
                # add dates, times, and carrie`r
                result.append(leg['departure'][0:10])
                result.append(leg['departure'][11:])
                result.append(leg['arrival'][11:])
                result.append(leg['carriers']['marketing'][0]['name'])
            file.write(','.join(result) + '\n')


def main():
    for city in input_dict['cities']:
        file = open('../output/' + city + '.csv', 'w')
        file.write(','.join(CSV_HEADERS) + '\n')
        for datePair in input_dict['flightDatePairs']:
            query_string = create_query(datePair[0], datePair[1], city)
            response = get_data_response(query_string, file)
            break
        file.close()
        break


if __name__ == "__main__":
    main()
