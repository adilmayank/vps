from bs4 import BeautifulSoup
import pandas as pd

url = r"C:/tesst.html"
page = open(url)

soup = BeautifulSoup(page.read(), "html.parser")

contact_name = soup.find_all("td", {"class": "contactName"})
contact_address = soup.find_all("td", {"class": "contactAddress"})
contact_number = soup.find_all("td", {"class": "phoneNumber"})

customer_details = {"fName": [],
                    "lName": [],
                    "address": [],
                    "phoneNumber": []}

for (nam, add, num) in zip(contact_name, contact_address, contact_number):
    name = nam.text.strip().split()
    fName = name[0]
    lName = name[1]
    address = add.text.strip()
    number = num.text.strip().split()
    number = "".join(number)

    if len(number) != 0 and number[0] != "^":
        customer_details["fName"].append(fName)
        customer_details["lName"].append(lName)
        customer_details["address"].append(address)
        customer_details["phoneNumber"].append(number)

#print(customer_details)
customer_details_df = pd.DataFrame(customer_details).to_csv("D:/Customer_data.csv", mode="a", header=True)