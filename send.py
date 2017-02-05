import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import sys
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

base_headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': os.environ.get("MS_API_KEY")
}

def start_processing(data):
    headers = base_headers.copy()
    headers['Content-Type'] = 'application/octet-stream'

    params = urllib.parse.urlencode({
        # Request parameters
        'outputStyle': 'aggregate',
    })

    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognizeinvideo?%s" % params, data, headers)
    response = conn.getresponse()
    conn.close()
    if response.status != 202:
        raise Exception('Non-success status code returned')
    status_url = response.getheader('Operation-Location')
    return status_url

def check_status(url):
    while True:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", url, "", base_headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if response.status != 200:
            raise Exception('Non-success status code' + str(response.status) + 'returned')
        result = json.loads(data.decode('ascii'))
        if result['status'] == 'Succeeded' or result['status'] == 'Failed':
            return result
        else:
            print('Waiting 60 seconds, current result is: ' + str(result['status']))
            time.sleep(60)


raw_data = open(sys.argv[1], 'rb').read()

url = start_processing(raw_data)
print('Uploaded, status URL is ' + str(url))
result = check_status(url)
print('Finished processing, writing result')

with open('result.json', 'w') as outfile:
    json.dump(result, outfile)
