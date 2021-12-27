from bs4 import BeautifulSoup
import pandas as pd


def create_customer_details_table(input_file, output_file):

    url = r"D:/rp_scraping/input/{}.html".format(input_file)
    file = open(url)

    customer_details = {"First Name": [],
                        "Last Name": [],
                        "Address": [],
                        "Phone Number": [],
                        "DNCR_IND": [],
                        "Bedrooms": [],
                        "Bathrooms": [],
                        "Car Space": [],
                        "Est. Land Area(m2)": []}

    soup = BeautifulSoup(file, "html.parser")

    summaryListItems = soup.find_all("div", {"class": "summaryListItem"})
    for i in range(len(summaryListItems)):
        content = summaryListItems[i].find("div", {"class": "content"})
        iconContainer = summaryListItems[i].find("ul", {"class": "iconContainer"})
        heading = summaryListItems[i].find("h2")
        attribute_list = iconContainer.text.strip().split()
        content_text = content.text

        if content_text.strip() != "No information available.":

            contact_name = content.find_all("td", {"class": "contactName"})
            #contact_address = content.find_all("td", {"class": "contactAddress"})
            contact_address = (" ".join(heading.text.strip().split()).replace(",", "")).upper()
            contact_number = content.find_all("td", {"class": "phoneNumber"})


            for (nam, num) in zip(contact_name, contact_number):
                name = nam.text.strip().split()
                fName = name[0]
                lName = name[1]
                address = contact_address
                number = num.text.strip().split()
                number = "".join(number)
                contact_bedroom = attribute_list[0]
                contact_bathroom = attribute_list[1]
                contact_car_space = attribute_list[2]
                contact_lot_area = attribute_list[4].replace("m2", "")

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
                    customer_details["Est. Land Area(m2)"].append(contact_lot_area)

    customer_details_df = pd.DataFrame(customer_details).to_csv(f"D:/rp_scraping/output/{output_file}.csv",
                                                                header=True,
                                                                index=False,
                                                                mode="a")
