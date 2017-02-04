import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '{subscription key}',
    'Content-Type': 'application/octet-stream'
}

params = urllib.parse.urlencode({
    # Request parameters
    'outputStyle': 'aggregate',
})

data = open('seinfeld.mp4', 'rb').read()

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognizeinvideo?%s" % params, data, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
    from pdb import set_trace; set_trace()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
