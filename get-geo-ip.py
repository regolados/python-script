import argparse
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Define the rate limit and calculate the delay per request
MAX_REQUESTS_PER_MINUTE = 20
SECONDS_IN_A_MINUTE = 60
REQUEST_DELAY = SECONDS_IN_A_MINUTE / MAX_REQUESTS_PER_MINUTE  # 3 seconds

def get_location(ip):
    # Replace with any free or paid IP geolocation API
    url = f"http://ip-api.com/json/{ip}?fields=country,city,regionName,lat,lon"
    
    # Introduce a delay to avoid throttling based on the rate limit
    time.sleep(REQUEST_DELAY)
    
    response = requests.get(url)
    data = response.json()
    
    # Directly access the values
    country = data.get('country', 'Unknown')
    city = data.get('city', 'Unknown')
    region = data.get('regionName', 'Unknown')
    latitude = data.get('lat', 'Unknown')
    longitude = data.get('lon', 'Unknown')

    return f"IP: {ip} - Country: {country}, City: {city}, Region: {region}, Latitude: {latitude}, Longitude: {longitude}"

def process_file(file_path):
    with open(file_path, 'r') as file:
        ips = [line.strip() for line in file.readlines() if line.strip()]  # Read and strip newlines

    # Use ThreadPoolExecutor to process multiple IP addresses concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_location, ips)
        
        # Print results
        for result in results:
            print(result)

def main():
    parser = argparse.ArgumentParser(description="Get the country and location of a list of IP addresses.")
    parser.add_argument("--file", required=True, help="Path to the file containing the list of IP addresses.")
    args = parser.parse_args()

    file_path = args.file
    process_file(file_path)

if __name__ == "__main__":
    main()

