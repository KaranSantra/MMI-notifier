import http.client
from html.parser import HTMLParser
import os
import re

def notify(title, message):
    command = f"""osascript -e 'display notification "{message}" with title "{title}" sound name "Submarine" '"""
    os.system(command)    
# Define a custom HTML parser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_mmi_value = False
        self.mmi_value = None
        self.img_alt_texts = []

    def handle_starttag(self, tag, attrs):
        mood_type_pattern = r'.*indicator_parts/.*\.svg$'
        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and 'number' in value:
                    self.in_mmi_value = True
        if tag == 'img':
            for name, value in attrs:
                if name == 'src' and re.match(mood_type_pattern,value):
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
    # Parse the HTML content d
    parser = MyHTMLParser()
    parser.feed(html_content)
    mmi_region=None
    if parser.mmi_value:
        mmi_value=int(float(parser.mmi_value))
        print("\nMarket Mood Index (MMI) value:", mmi_value)
        for alt_text in parser.img_alt_texts:
            print(alt_text)
            if(mmi_value<=35 or mmi_value>=65):                
                notify(alt_text, f"MMI Value: {mmi_value}!!!")
    else:
        print("MMI value not found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status)  