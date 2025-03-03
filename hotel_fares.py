import requests
import json
import time
from datetime import datetime
import argparse
import os


AMADEUS_API_KEY = 'SBPrSEolMcuumLz3lZWjZGnc3wxLQOYp'
AMADEUS_API_SECRET = '6fAINGYmshNgguRn'


def get_access_token():
    for attempt in range(3):
        try:
            response = requests.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"grant_type": "client_credentials", "client_id": AMADEUS_API_KEY,
                      "client_secret": AMADEUS_API_SECRET},
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Failed to get access token: {e}")
            if attempt < 2:
                print("Retrying access token request...")
                time.sleep(2 ** attempt)
            else:
                print("Max retries reached for access token.")
                return None


def main(city_code, check_in, check_out):
    access_token = get_access_token()
    if not access_token:
        print("Failed to authenticate.")
        return

    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        hotel_ids_response = requests.get(
            "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city",
            headers=headers,
            params={"cityCode": city_code},
            timeout=10
        )
        hotel_ids_response.raise_for_status()
        hotel_ids = [hotel['hotelId'] for hotel in hotel_ids_response.json().get("data", [])]
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve hotel IDs: {e}")
        return

    offers, errors = [], []
    for i in range(0, len(hotel_ids), 20):
        batch = hotel_ids[i:i + 20]
        params = {"hotelIds": ','.join(batch), "checkInDate": check_in, "checkOutDate": check_out, "adults": 2}

        for attempt in range(3):
            try:
                response = requests.get(
                    "https://test.api.amadeus.com/v3/shopping/hotel-offers",
                    headers=headers,
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()
                if "errors" in result:
                    errors.append({"batch": i // 20 + 1, "error_details": result["errors"]})
                else:
                    offers.extend(result.get("data", []))
                break
            except requests.exceptions.RequestException as e:
                print(f"Failed to get hotel offers for batch {i // 20 + 1}: {e}")
                if attempt < 2:
                    print("Retrying...")
                    time.sleep(2 ** attempt)
                else:
                    errors.append({"batch": i // 20 + 1, "error_details": str(e)})

    output = {
        "hotel_offers": [
            {
                "hotel_name": offer['hotel']['name'],
                "city_code": offer['hotel']['cityCode'],
                "check_in": detail['checkInDate'],
                "check_out": detail['checkOutDate'],
                "total_price": detail['price'].get('total', "N/A"),
                "currency": detail['price'].get('currency', "N/A"),
                "room_category": detail['room'].get('typeEstimated', {}).get('category', "N/A")
            }
            for offer in offers for detail in offer['offers']
        ],
        "errors": errors
    }

    output_dir = 'amadeusfares'
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"hotel_offers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
    print(f"Results saved to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch hotel offers from Amadeus API")
    parser.add_argument("city_code", type=str, help="City code (e.g., DXB for Dubai)")
    parser.add_argument("check_in", type=str, help="Check-in date (YYYY-MM-DD)")
    parser.add_argument("check_out", type=str, help="Check-out date (YYYY-MM-DD)")

    args = parser.parse_args()
    main(args.city_code, args.check_in, args.check_out)
