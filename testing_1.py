from bs4 import BeautifulSoup
import pandas as pd

url = r"C:\IPNUT_FILE.html"
file = open(url)

customer_details = {"First Name": [],
                    "Last Name": [],
                    "Address": [],
                    "Phone Number": [],
                    "DNCR_IND": [],
                    "Bedrooms": [],
                    "Bathrooms": [],
                    "Car Space": []}

soup = BeautifulSoup(file, "html.parser")

summaryListItems = soup.find_all("div", {"class": "summaryListItem"})
for i in range(len(summaryListItems)):
    content = summaryListItems[i].find("div", {"class": "content"})
    heading = summaryListItems[i].find("ul", {"class": "iconContainer"})
    attribute_list = heading.text.strip().split()
    content_text = content.text

    if content_text.strip() != "No information available.":

        contact_name = content.find_all("td", {"class": "contactName"})
        contact_address = content.find_all("td", {"class": "contactAddress"})
        contact_number = content.find_all("td", {"class": "phoneNumber"})


        for (nam, add, num) in zip(contact_name, contact_address, contact_number):
            name = nam.text.strip().split()
            fName = name[0]
            lName = name[1]
            address = add.text.strip()
            number = num.text.strip().split()
            number = "".join(number)
            contact_bedroom = attribute_list[0]
            contact_bathroom = attribute_list[1]
            contact_car_space = attribute_list[2]

            if len(number) != 0:

                customer_details["First Name"].append(fName)
                customer_details["Last Name"].append(lName)
                customer_details["Address"].append(address)
                if number[0] == "^":
                    customer_details["DNCR_IND"].append("Y")
                else:
                    customer_details["DNCR_IND"].append("N")

                to_replace = ")^("
                for character in to_replace:
                    number = number.replace(character, "")

                customer_details["Phone Number"].append(number)
                customer_details["Bedrooms"].append(contact_bedroom)
                customer_details["Bathrooms"].append(contact_bathroom)
                customer_details["Car Space"].append(contact_car_space)

customer_details_df = pd.DataFrame(customer_details).to_csv("OUTPUT_FILE.csv", header=True, index=False)

