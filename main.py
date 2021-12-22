from bs4 import BeautifulSoup
import re

url = r"C:\tesst.html"
page = open(url)
soup = BeautifulSoup(page.read(),"html.parser")

clickables = soup.find_all("a", {"class": "clickable"})

addresses = []

for i in range(len(clickables)):
    address = clickables[i].text.strip()
    print(address)



