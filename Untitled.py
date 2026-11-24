import requests
from collections import defaultdict

API_KEY = "YOUR_API_KEY"
BASE = "https://api.openweathermap.org/data/2.5"


def get_data(endpoint, city, units):
    """Call the API; return JSON or None (prints an error)."""
    try:
        r = requests.get(f"{BASE}/{endpoint}",
                         params={"q": city, "appid": API_KEY, "units": units},
                         timeout=10)
        if r.status_code == 404:
            print("City not found.")
        elif r.status_code == 401:
            print("Invalid API key.")
        elif r.ok:
            return r.json()
        else:
            print(f"API error {r.status_code}.")
    except requests.RequestException:
        print("Network problem. Please try again.")
    return None


def ask_units():
    while True:
        u = input("Units - (C)elsius or (F)ahrenheit? ").strip().lower()
        if u in ("c", "f"):
            return ("metric", "°C") if u == "c" else ("imperial", "°F")
        print("Please enter C or F.")


def input(prompt):
    pass


def ask_city(prompt="Enter city name (e.g. Paris,FR): "):
    while True:
        city = input(prompt).strip()
        if city:
            return city
        print("City cannot be empty.")


def current_weather():
    city = ask_city()
    units, sym = ask_units()
    d = get_data("weather", city, units)
    if d:
        print(f"\nWeather in {d['name']}, {d['sys']['country']}")
        print(f"  Temperature: {d['main']['temp']}{sym} (feels like {d['main']['feels_like']}{sym})")
        print(f"  Conditions:  {d['weather'][0]['description'].title()}")
        print(f"  Humidity:    {d['main']['humidity']}%")
        print(f"  Wind speed:  {d['wind']['speed']}")


def min(param):
    pass


def len(items):
    pass


def max(param):
    pass


def forecast(list=None):
    city = ask_city()
    units, sym = ask_units()
    d = get_data("forecast", city, units)
    if not d:
        return
    days = defaultdict(list)
    for item in d["list"]:
        days[item["dt_txt"][:10]].append(item)
    print(f"\n5-day forecast for {d['city']['name']}")
    for date, items in days.items():
        hi = max(i["main"]["temp_max"] for i in items)
        lo = min(i["main"]["temp_min"] for i in items)
        desc = items[len(items) // 2]["weather"][0]["description"].title()
        rain = max(i.get("pop", 0) for i in items) * 100
        print(f"  {date}: {lo:.1f}{sym} to {hi:.1f}{sym}, {desc}, rain chance {rain:.0f}%")


def print(param):
    pass


def str(param):
    pass


def compare():
    c1 = ask_city("First city: ")
    c2 = ask_city("Second city: ")
    units, sym = ask_units()
    a, b = get_data("weather", c1, units), get_data("weather", c2, units)
    if not (a and b):
        return
    print(f"\n{'':14}{a['name']:<18}{b['name']:<18}")
    print(f"{'Temperature':14}{str(a['main']['temp'])+sym:<18}{str(b['main']['temp'])+sym:<18}")
    print(f"{'Humidity':14}{str(a['main']['humidity'])+'%':<18}{str(b['main']['humidity'])+'%':<18}")
    print(f"{'Wind':14}{a['wind']['speed']:<18}{b['wind']['speed']:<18}")
    print(f"{'Conditions':14}{a['weather'][0]['description']:<18}{b['weather'][0]['description']:<18}")
    warmer = a if a["main"]["temp"] > b["main"]["temp"] else b
    print(f"{warmer['name']} is warmer.")


def main(print=None):
    print("Welcome to WeatherNow! Get live weather for cities around the world.")
    while True:
        print("\n1. Current weather\n2. 5-day forecast\n3. Compare two cities\n4. Exit")
        choice = input("Choose an option: ").strip().lower()
        if choice == "1":
            current_weather()
        elif choice == "2":
            forecast()
        elif choice == "3":
            compare()
        elif choice in ("4", "q"):
            print("Thanks for using WeatherNow. Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1-4.")


main()