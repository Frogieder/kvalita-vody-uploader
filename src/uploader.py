from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Uploader:
    def __init__(self, url, token, organization, bucket, location):
        self.bucket = bucket
        self.organization = organization
        self.token = token
        self.url = url
        self.location = location

    def upload(self, data: dict):
        # print(data)
        sequence = [
            Point("kvalita-vody")
                .tag("location", self.location)
                .field(key, data[key])
                .time(datetime.utcnow(), WritePrecision.NS)
            for key in data.keys()
        ]

        with InfluxDBClient(url=self.url, token=self.token, org=self.organization) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(self.bucket, self.organization, sequence)
            print("Uploading to database")
            print(sequence)
