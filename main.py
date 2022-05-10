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


try:
    if os.path.isfile("./config.json"):
        with open("config.json", "r") as file:
            config = json_load(file)
            _ = [config["InfluxDB URL"], config["Token"], config["Organization"], config["Bucket"]]
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
                    organization=config["Organization"], bucket=config["Bucket"])

try:
    while True:
        data = receiver.read_blocking()

except KeyboardInterrupt:
    pass
finally:
    print("Stopping application")
