import http.client
from html.parser import HTMLParser
import os

def notify(title, message):
    print("test")
    os.system(f"terminal-notifier -title '{title}' -message '{message}' -timeout 0")
# Define a custom HTML parser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_mmi_value = False
        self.mmi_value = None
        self.img_alt_texts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and 'number' in value:
                    self.in_mmi_value = True
        if tag == 'img':
            for name, value in attrs:
                print(f"name{name}, value:{value}")
                if name == 'src' and value.startswith("indicator_parts/") and value.endswith(".svg"):
                    for name, value in attrs:
                        if name == 'alt':
                            self.img_alt_texts.append(value)

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
    mmi_region=None
    if parser.mmi_value:
        mmi_value=int(float(parser.mmi_value))
        print("Market Mood Index (MMI) value:", parser.mmi_value)
        for alt_text in parser.img_alt_texts:
            print(alt_text.split()[0])  # Extracting the first word ("Greed")  
            mmi_region=alt_text.split()[0] 
        if(mmi_value<=35 or mmi_value>=65):
            print(mmi_region)
            notify("Extremes on Market Mood Index (MMI) ", mmi_region)
    else:
        print("MMI value not found on the page.")

else:
    print("Failed to retrieve the webpage. Status code:", response.status)  