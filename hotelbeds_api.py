import requests
import json
import time
import hashlib
import argparse
import os


API_KEY = 'cb83bb3999659ddf0ba33e36601958b1'
API_SECRET = '19a056b3ea'
BASE_URL = 'https://api.test.hotelbeds.com/hotel-api/1.0/'


def generate_signature(api_key, api_secret):
    timestamp = str(int(time.time()))
    raw_signature = api_key + api_secret + timestamp
    signature = hashlib.sha256(raw_signature.encode()).hexdigest()
    return signature

def get_hotel_availability(destination_code, check_in, check_out, adults=1, rooms=1):
    signature = generate_signature(API_KEY, API_SECRET)
    headers = {
        'Api-Key': API_KEY,
        'X-Signature': signature,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        'stay': {
            'checkIn': check_in,
            'checkOut': check_out,
        },
        'occupancies': [
            {
                'rooms': rooms,
                'adults': adults,
                'children': 0
            }
        ],
        'destination': {
            'code': destination_code
        }
    }

    try:
        response = requests.post(BASE_URL + 'hotels', headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {response.status_code} - {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    parser = argparse.ArgumentParser(description='Fetch hotel availability from Hotelbeds API.')
    parser.add_argument('destination_code', type=str, help='The destination code (e.g., DEL for Delhi)')
    parser.add_argument('check_in', type=str, help='Check-in date (YYYY-MM-DD)')
    parser.add_argument('check_out', type=str, help='Check-out date (YYYY-MM-DD)')
    parser.add_argument('--adults', type=int, default=1, help='Number of adults')
    parser.add_argument('--rooms', type=int, default=1, help='Number of rooms')

    args = parser.parse_args()

    hotel_data = get_hotel_availability(
        args.destination_code,
        args.check_in,
        args.check_out,
        adults=args.adults,
        rooms=args.rooms
    )

    output_dir = 'hotelbeds'
    os.makedirs(output_dir, exist_ok=True)

    if hotel_data:
        timestamp = int(time.time())
        filename = os.path.join(output_dir, f"hotel_availability_{args.destination_code}_{args.check_in}_{args.check_out}_{timestamp}.json")
        with open(filename, 'w') as f:
            json.dump(hotel_data, f, indent=4)
        print(f"Data saved to {filename}")
    else:
        print("No data received.")

if __name__ == "__main__":
    main()













