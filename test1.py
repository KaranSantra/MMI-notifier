import http.client
from html.parser import HTMLParser

# Define a custom HTML parser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_mmi_value = False
        self.mmi_value = None

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and 'number' in value:
                    self.in_mmi_value = True

    def handle_endtag(self, tag):
        if tag == 'span' and self.in_mmi_value:
            self.in_mmi_value = False

    def handle_data(self, data):
        if self.in_mmi_value:
            self.mmi_value = data

# Make an HTTP request
conn = http.client.HTTPSConnection("www.tickertape.in")
conn.request("GET", "/market-mood-index")
response = conn.getresponse()

if response.status == 200:
    html_content = response.read().decode()
    # Parse the HTML content
    parser = MyHTMLParser()
    parser.feed(html_content)

    if parser.mmi_value:
        print("Market Mood Index (MMI) value:", parser.mmi_value)
    else:
        print("MMI value not found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status)