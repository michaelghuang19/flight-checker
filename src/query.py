import json
import requests

# sending requests and querying for up-to-date data
# shift + option + f to format

api_url = 'https://skyscanner44.p.rapidapi.com/search'

with open('../data/input.json') as input:
  input_dict = json.load(input)
with open('../data/secrets.json') as secrets:
  headers = json.load(secrets)

def create_query(departureDate, returnDate, destination, origin="LHR", adults=2, currency="USD"):
  querystring = {
    "adults": adults,
    "origin": origin,
    "destination": destination,
    "departureDate": departureDate,
    "returnDate": returnDate,
    "currency": currency
  }

  return querystring

def get_data_response(querystring):
  response = requests.request("GET", api_url, headers=headers, params=querystring)

  print(response)

def main():
  print("Hello world")
  
  # parse in responses

if __name__ == "__main__":
  main()
