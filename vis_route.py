#!/usr/bin/env python3

import getopt
import json
import os
import platform
import subprocess
import sys

import requests


GEO_IP_API = "https://geolocation-db.com/json/"


def get_loc(IP):
    """Turn a string representing an IP address into a lat long pair"""

    request = requests.get(GEO_IP_API + IP)
    if request.status_code != 200:
        return
    data = request.json()
    print(data)

    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])
        if lat == 0.0 and lon == 0.0:
            return (None, None)
        return (lat, lon)
    except:
        return (None, None)


def print_help():
    print("./vis_route.py IPv4Address")
    print(" e.g. ./vis_route.py 213.138.111.222")


try:
    opts, args = getopt.getopt(sys.argv, "h")
except getopt.GetoptError:
    print_help()
    sys.exit()
for opt, arg in opts:
    if opt == "-h":
        print_help()
        sys.exit()
if len(args) != 2:
    print_help()
    sys.exit()
IP = args[1]

# OS detection Linux/Mac or Windows
if platform.system() == "Linux" or platform.system() == "Darwin":
    # Start traceroute command
    proc = subprocess.Popen(
        ["traceroute -m 25 -n " + IP],
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True,
    )

    lastLon = None
    lastLat = None
    # Parse individual traceroute command lines
    for line in proc.stdout:
        print(line, end="")
        hopIP = line.split()[1]

        if hopIP in ("*", "to"):
            continue
        (lat, lon) = get_loc(hopIP)
        if lat is None:
            continue
        if lastLat is not None and (lastLat - lat + lastLon - lon) != 0.0:
            print(lastLat,lastLon,lat,lon)
        lastLat = lat
        lastLon = lon

# elif platform.system() == "Windows":
#     proc = subprocess.Popen(
#         "C:\\Windows\\System32\\TRACERT.exe -h 25 -d -4 " + IP,
#         stdout=subprocess.PIPE,
#         shell=True,
#         universal_newlines=True,
#     )
#     fig = plt.figure(figsize=(10, 6), edgecolor="w")
#     m = Basemap(projection="mill", lon_0=0, resolution="l")
#     m.shadedrelief(scale=0.05)
#     lastLon = None
#     lastLat = None

#     for line in proc.stdout:
#         print(line, end="")
#         if len(line.split()) != 8:
#             continue
#         else:
#             hopIP = line.split()[7]
#             if hopIP in ("*", "to"):
#                 continue
#             (lat, lon) = get_loc(hopIP)
#             if lat is None:
#                 continue
#             if lastLat is not None and (lastLat - lat + lastLon - lon) != 0.0:
#                 x, y = m(lon, lat)
#                 m.scatter(x, y, 10, marker="o", color="r")
#                 (line,) = m.drawgreatcircle(lastLon, lastLat, lon, lat, color="b")
#             lastLat = lat
#             lastLon = lon

#     plt.tight_layout()
#     plt.show()
else:
    print(
        "Sorry, this python program does not have support for your current operating system!"
    )
    sys.exit(-1)
