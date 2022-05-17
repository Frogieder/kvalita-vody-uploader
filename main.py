#
#     Uploader for the water quality monitor
#     Copyright (C) 2022  Martin Marcinčák
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License

from src.receiver import Receiver
from src.uploader import Uploader
import time
import os
from json import load as json_load
from json.decoder import JSONDecodeError


def average_over_list(data: list[dict]):
    keys = data[0].keys()
    result = {}
    for dictionary in data:
        for key in keys:
            result[key] = result.get(key, 0) + dictionary[key]
    length = len(data)
    for key in keys:
        result[key] /= length
    return result


try:
    if os.path.isfile("./config.json"):
        with open("config.json", "r") as file:
            config = json_load(file)
            # Test if all required keys are present in the file
            _ = [config["InfluxDB URL"], config["Token"], config["Organization"], config["Bucket"], config["Location"]]
except FileNotFoundError:
    print("Config file not found")
    exit(1)
except JSONDecodeError:
    print("Couldn't decode config file")
    exit(1)
except KeyError:
    print("Invalid json file.\nPlease check the github repo to see propperly configured json")
    exit(1)

receiver = Receiver()
uploader = Uploader(url=config["InfluxDB URL"], token=config["Token"],
                    organization=config["Organization"], bucket=config["Bucket"],
                    location=config["Location"])

try:
    next_upload = time.time() + 60
    next_get = 0
    data = []
    while True:
        # perform measurement each second
        if time.time() >= next_get:
            next_get = time.time() + 1
            data.append(receiver.read_blocking())
        # upload average of measurements every minute
        if time.time() >= next_upload:
            next_upload += + 60
            if len(data) < 20:
                print("WARNING: Data receiving too slow:", len(data), "values/min\nSkipping upload")
                data = []
                continue
            uploader.upload(average_over_list(data))
            data = []
except KeyboardInterrupt:
    pass
finally:
    print("\n\nStopping application")
