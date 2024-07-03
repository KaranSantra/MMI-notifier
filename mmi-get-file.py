import http.client

conn = http.client.HTTPSConnection("market-mood-index.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "70222154eamsh474d2974c131b58p13435ajsn6d5bc8910821",
    'x-rapidapi-host': "market-mood-index.p.rapidapi.com"
}

conn.request("GET", "/mmi", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))