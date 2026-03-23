# Team Name   : Bisaya Bytes
# Members     : RJ Alenton, Eduard Philippe Tojong, Alshier Ahmad, Johnb Benedict Canon
# Subject     : SYSARCH32 - LABWORKS 4.9.3
# Base Code   : Lab 4.9.2 - Graphhopper Directions Application
# Feature     : Enhanced application with Multi-Stop, Location History & Favorites


import requests
import urllib.parse
import json
import os

route_url = "https://graphhopper.com/api/1/route?"
key = "5e387e03-6111-4cff-9033-31db3ede05a5"

# ── Ahmad's Feature: Location History & Favorites ──────────────────────────
HISTORY_FILE = "location_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "favorites": []}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_to_history(location_name):
    data = load_history()
    if location_name not in data["history"]:
        data["history"].insert(0, location_name)
        data["history"] = data["history"][:10]  # keep last 10
    save_history(data)

def show_saved_locations():
    data = load_history()
    print("\n=== SAVED LOCATIONS ===")
    if data["history"]:
        print("Recent History:")
        for i, loc in enumerate(data["history"], 1):
            print(f"  {i}. {loc}")
    else:
        print("  No history yet.")
    if data["favorites"]:
        print("Favorites:")
        for i, loc in enumerate(data["favorites"], 1):
            print(f"  F{i}. {loc}")
    else:
        print("  No favorites yet.")
    print("=======================")

def add_to_favorites(location_name):
    data = load_history()
    if location_name not in data["favorites"]:
        data["favorites"].append(location_name)
        save_history(data)
        print(f"  '{location_name}' added to favorites!")
    else:
        print(f"  '{location_name}' is already in favorites.")

def pick_from_saved():
    data = load_history()
    all_locs = data["history"] + [f for f in data["favorites"] if f not in data["history"]]
    if not all_locs:
        return None
    show_saved_locations()
    choice = input("Pick a number from saved locations (or press Enter to type manually): ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(all_locs):
            return all_locs[idx]
    return None
# ───────────────────────────────────────────────────────────────────────────


def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)

    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])

    return json_status, lat, lng, new_loc

# ---- EDUARD'S FEATURE: Trip Logging ----
def log_trip(origin, destination, vehicle, km, duration):
    import datetime
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('trip_log.txt', 'a') as f:
        f.write(f"[{ts}] {origin} -> {destination} | {vehicle} | {km:.1f}km | {duration}\n")
    print("  [Trip saved to trip_log.txt]")

# ── RJ's Feature: Multi-Stop Trip Planner ──────────────────────────────────
def multi_stop_trip(key, vehicle):
    stops = []
    print("\n=== MULTI-STOP TRIP PLANNER ===")
    print("Enter locations one by one. Type 'done' when finished.")
    while True:
        saved = pick_from_saved()
        if saved:
            loc = saved
            print(f"  Using saved location: {loc}")
        else:
            loc = input(f"Enter Stop {len(stops)+1} (or 'done'): ")
        if loc.lower() == 'done':
            if len(stops) < 2:
                print("Need at least 2 stops!")
                continue
            break
        r = geocoding(loc, key)
        if r[0] == 200:
            stops.append(r)
            add_to_history(r[3])
            print(f"  Added: {r[3]}")
            fav = input("  Add to favorites? (y/n): ").strip().lower()
            if fav == 'y':
                add_to_favorites(r[3])
    print("\nFull Route: " + " -> ".join([s[3] for s in stops]))
    for i in range(len(stops) - 1):
        print(f"\n--- Leg {i+1}: {stops[i][3]} to {stops[i+1][3]} ---")
# ───────────────────────────────────────────────────────────────────────────



#  Alenton FEATURE: Multi-Stop Trip Planner 
def multi_stop_trip(key, vehicle):
    stops = []
    print("\n=== MULTI-STOP TRIP PLANNER ===")
    print("Enter locations one by one. Type 'done' when finished.")
    while True:
        loc = input(f"Enter Stop {len(stops)+1} (or 'done'): ")
        if loc.lower() == 'done':
            if len(stops) < 2:
                print("Need at least 2 stops!")
                continue
            break
        r = geocoding(loc, key)
        if r[0] == 200:
            stops.append(r)
            print(f"  Added: {r[3]}")
    print("\nFull Route: " + " -> ".join([s[3] for s in stops]))
    for i in range(len(stops) - 1):
        print(f"\n--- Leg {i+1}: {stops[i][3]} to {stops[i+1][3]} ---")



while True:

    # ---- CANON'S FEATURE: Unit Toggle ----
    unit = input("Units — (1) Miles first  (2) KM first  [press Enter for Miles]: ").strip()
    use_miles = (unit != '2')

    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    profile = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")
    
        

    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    mode = input("Normal trip (n) or Multi-stop (m)? ").strip().lower()
    if mode == 'm':
        multi_stop_trip(key, vehicle)
        continue

    # ── Ahmad's Feature: offer saved locations for normal trip ──
    print("\nStarting Location:")
    saved = pick_from_saved()
    if saved:
        loc1 = saved
        print(f"  Using saved location: {loc1}")
    else:
        loc1 = input("Starting Location: ")
    # ────────────────────────────────────────────────────────────

    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    if orig[0] == 200:
        add_to_history(orig[3])

    # ── Ahmad's Feature: offer saved locations for destination ──
    print("\nDestination:")
    saved = pick_from_saved()
    if saved:
        loc2 = saved
        print(f"  Using saved location: {loc2}")
    else:
        loc2 = input("Destination: ")
    # ────────────────────────────────────────────────────────────

    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    if dest[0] == 200:
        add_to_history(dest[3])

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")

        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            if use_miles:
                print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
            else:
                print("Distance Traveled: {0:.1f} km / {1:.1f} miles".format(km, miles))
                
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=============================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance / 1000, distance / 1000 / 1.61))

            log_trip(orig[3], dest[3], vehicle, km, '{:02d}:{:02d}:{:02d}'.format(hr, min, sec))

            print("=============================================")

        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")
            
            