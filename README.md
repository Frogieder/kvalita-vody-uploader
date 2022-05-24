# Uploader for the water quality monitor

This code is supposed to run on a RPi that's listening to an Arduino.
It recieves data from 2.4GHz radio module and uploads them to an InfluxDB server.

## Usage
### Install

This script only runs on recent versions of Raspbian with Python>=3.6.
The recommended version is 3.9.5 - the most recent one as of writing this.

Clone this repository to your desired location:
``` shell
$ cd [DESIRED LOCATION]
$ git clone https://github.com/Frogieder/kvalita-vody-uploader.git
```
This program requires the `influxdb` library.
You can install it by running:
```shell
$ python3 -m pip install influxdb
```
 ### Configure
To configure this, you'll need to edit the `config.json` file.
Replace the placeholder values with your own, real values

### Run
Inside a clone of this repository, execute the following command:
```shell
$ ./start_uploader
```