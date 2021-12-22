from bs4 import BeautifulSoup
import re

url = r"C:\tesst.html"
page = open(url)
soup = BeautifulSoup(page.read(),"html.parser")

content_container = soup.find_all("div", {"class": "contentContainer"})
clickable = content_container[0].find_all("a", {"class": "clickable"})
table_data = content_container[0].find_all("div", {"class": "content"})

ots = {}

print(len(content_container))
print(clickable)
print(table_data[0].find("span"))

"""for i in range(len(clickables)):
    address = clickables[i].text.strip()
    print(address)"""



