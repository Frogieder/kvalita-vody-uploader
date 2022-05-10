class Uploader:
    def __init__(self, url, token, organization, bucket):
        self.bucket = bucket
        self.organization = organization
        self.token = token
        self.url = url

    def upload(self, data):
        print(data)
