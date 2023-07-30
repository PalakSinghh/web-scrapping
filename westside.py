import uuid

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import ArcGIS
import json
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

nom = ArcGIS()


def fetch_store_details(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the store address elements and opening hours
        soup = BeautifulSoup(response.content, 'html.parser')
        p_elements = soup.select('div.storedetails p')
        address_element = soup.find('span', {'class': 'storedata'}).get_text(strip=True)
        phone_element = soup.find('span', {'class': 'storedata'}).find_next_sibling('span').get_text(strip=True)
        opening_hours_element = soup.find('span',{'class': 'storedata'}).find_next_sibling('span').find_next_sibling('span').find_next_sibling('span').get_text()
        print(opening_hours_element)
        ref=uuid.uuid4().hex

        operating_hours = opening_hours_element

        # Clean and process the addresses
        locations = []
        for p_element in p_elements:
            address = p_element.get_text(strip=True)
            location = geocode_with_retry(address)
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
                feature = {
                    'type': 'Feature',
                    'properties': {
                        'addr:full': address_element,
                        'addr:country':'India',
                        '@spider':'chain',
                        'phones': phone_element,
                        'chain_id':'301792',
                        'chain_name':'Westside',
                        'brand':'Westside',
                        'operatingHours': operating_hours,
                        'store_url':'https://www.westside.com/apps/s/storelocator/maharashtra/mumbai/cosmos-plaza-andheri-west-d-n-nagar-w111?type=Westside',
                        'website':'https://www.westside.com/apps/s/storelocator/maharashtra/mumbai/cosmos-plaza-andheri-west-d-n-nagar-w111?type=Westside',
                        'ref':ref,
                        'name':'Westside'

                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude]
                    }
                }
                locations.append(feature)

        save_to_geojson(locations)

    else:
        print("Failed to fetch the webpage:", response.status_code)


def geocode_with_retry(address, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            location = nom.geocode(address)
            return location
        except Exception as e:
            print(f"Geocoding failed: {e}")
            retries += 1
            time.sleep(2)  # Wait for a few seconds before retrying
    return None


def parse_operating_hours(element):
    operating_hours = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Splitting the element by '<br>' and iterating through each line
    lines = element.split('<br>')
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespaces

        # Check if the line contains a day and hours information
        for day in days:
            if day in line:
                day, hours = line.split('-', 1)
                day = day.strip()
                hours = hours.strip()
                operating_hours[day] = hours

    return operating_hours


def save_to_geojson(locations):
    filename = 'westside.geojson'
    with open(filename, 'w') as file:
        geojson_data = {
            'type': 'FeatureCollection',
            'features': locations
        }
        json.dump(geojson_data, file, indent=4)

    print(f'Saved data to {filename}')


if __name__ == "__main__":
    url = 'https://www.westside.com/apps/s/storelocator/maharashtra/mumbai/cosmos-plaza-andheri-west-d-n-nagar-w111?type=Westside'
    fetch_store_details(url)
