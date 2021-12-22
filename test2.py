from bs4 import BeautifulSoup
import pandas as pd

url = r"C:\demo.html"
page = open(url)
soup = BeautifulSoup(page.read(),  "html.parser")

dictionary = []

content_container = soup.find_all("div", {"class": "contentContainer"})
for item in content_container:
    content = item.find_all("tbody")

    if len(content) > 0:

        for tdata in content:

            td = tdata.find_all("td")

            for i in td:

                single_record = {"fname": [],
                                 "lname": [],
                                 "address": [],
                                 "mobile_num": []}

                fname = i[0]
                lname = i[1]
                address = " ".join(i[2])
                mobile_num = "".join(i[3].text.strip().split())

                if len(mobile_num) != 0 and mobile_num[0] != "^":

                    single_record["fname"].append(fname)
                    single_record["lname"].append(lname)
                    single_record["address"].append(address)
                    single_record["mobile_num"].append(mobile_num)

                dictionary.append(single_record)

            print("-------")
            print("       ")
            print("-------")

print(len(dictionary))
customer_data = pd.DataFrame(dictionary)
customer_data.to_csv("E:/customer_data_test.csv", mode="a", index=False, header=True)