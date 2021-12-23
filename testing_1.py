from bs4 import BeautifulSoup
import pandas as pd

#url provides a link for local html file for scraping.
url = r"INPUT_FILE.html"
page = open(url)

soup = BeautifulSoup(page.read(), "html.parser")

contact_name = soup.find_all("td", {"class": "contactName"})
contact_address = soup.find_all("td", {"class": "contactAddress"})
contact_number = soup.find_all("td", {"class": "phoneNumber"})

customer_details = {"First_name": [],
                    "Last_name": [],
                    "Address": [],
                    "Phone_Number": [],
                    "DNCR_IND": []}

for (nam, add, num) in zip(contact_name, contact_address, contact_number):
    name = nam.text.strip().split()
    fName = name[0]
    lName = name[1]
    address = add.text.strip()
    number = num.text.strip().split()
    number = "".join(number)

    if len(number) != 0:
        customer_details["First_name"].append(fName)
        customer_details["Last_name"].append(lName)
        customer_details["Address"].append(address)
        if number[0] == "^":
            customer_details["DNCR_IND"].append("Y")
        else:
            customer_details["DNCR_IND"].append("N")

        to_replace = ")^("
        for character in to_replace:
            number = number.replace(character, "")

        customer_details["Phone_Number"].append(number)

print(customer_details) # only for confirmation purposes
customer_details_df = pd.DataFrame(customer_details).to_excel("OUTPUT_FILE.xlsx", header=True) #prints an excel file from pandas DataFrame.
