import sys

import requests

NAME = "Vadym Soltys"
GROUP = "IT-32"
URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10

# --- ЗАМІНІТЬ НА СВОЄ МІСТО ---
CITY = "Kyiv"
LATITUDE = 50.45
LONGITUDE = 30.52
# ------------------------------


def main():
    print(f"{NAME}, {GROUP}")
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,wind_speed_10m",
    }
    try:
        response = requests.get(URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        units = data["current_units"]
        temperature = current["temperature_2m"]
        wind = current["wind_speed_10m"]
    except requests.RequestException as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
    except KeyError as error:
        print(f"error: unexpected response, no key {error}", file=sys.stderr)
        sys.exit(1)

    print(f"{CITY} ({LATITUDE}, {LONGITUDE}): "
          f"{temperature} {units['temperature_2m']}, "
          f"wind {wind} {units['wind_speed_10m']}")


if __name__ == "__main__":
    main()
