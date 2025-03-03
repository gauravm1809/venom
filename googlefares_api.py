import requests
import pandas as pd
from datetime import datetime
import argparse
import os
import json



def fetch_hotels_data(location, check_in, check_out, currency, adults, rooms, max_results=50):
    url = "https://serpapi.com/search"
    all_hotels = []
    start = 0

    while len(all_hotels) < max_results:
        params = {
            "engine": "google_hotels",
            "q": location,
            "check_in_date": check_in,
            "check_out_date": check_out,
            "currency": currency,
            "adults": adults,
            "rooms": rooms,
            "start": start,
            "api_key": "5b9dacadb29888663d586554c1ec3c0a52ce1672492324cbec1d4117c0c3e0ca"
        }
        response = requests.get(url, params=params)
        data = response.json()

        properties = data.get("properties", [])
        if not properties:
            break

        all_hotels.extend(properties)
        start += len(properties)

    return all_hotels[:max_results]


def process_hotels_data(raw_data):
    hotels = []
    for property in raw_data:
        rating = property.get("overall_rating", 0)
        price_info = property.get("rate_per_night", {})
        price = price_info.get("extracted_lowest", "N/A")
        total_cost = property.get("total_rate", {}).get("lowest", "N/A")

        hotel = {
            "Name": property.get("name"),
            "Location": f"{property['gps_coordinates'].get('latitude')}, {property['gps_coordinates'].get('longitude')}",
            "Rating": rating,
            "Price/Night": price_info.get("lowest", "N/A"),
            "Total Cost": total_cost,
            "Amenities": ", ".join(property.get("amenities", [])),
            "Link": property.get("link", "N/A")
        }
        hotels.append(hotel)

    df = pd.DataFrame(hotels)
    return df


def save_to_json(hotels_df, location):
    timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    file_name = f"{location}_hotels_{timestamp}.json"
    directory = "googlefares"

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)
    hotels_data = hotels_df.to_dict(orient="records")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(hotels_data, f, ensure_ascii=False, indent=4)

    print(f"Hotel data saved to {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Fetch Google Hotel fares")
    parser.add_argument("location", type=str, help="Location to search hotels")
    parser.add_argument("check_in", type=str, help="Check-in date (YYYY-MM-DD)")
    parser.add_argument("check_out", type=str, help="Check-out date (YYYY-MM-DD)")
    parser.add_argument("currency", type=str, help="Currency (e.g., INR, USD)")
    parser.add_argument("--adults", type=int, default=2, help="Number of adults")
    parser.add_argument("--rooms", type=int, default=1, help="Number of rooms")
    parser.add_argument("--max_results", type=int, default=50, help="Maximum number of hotels to fetch")
    args = parser.parse_args()


    raw_data = fetch_hotels_data(args.location, args.check_in, args.check_out, args.currency, args.adults, args.rooms, args.max_results)
    df = process_hotels_data(raw_data)


    save_to_json(df, args.location)

if __name__ == "__main__":
    main()
