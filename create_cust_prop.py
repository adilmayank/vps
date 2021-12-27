from bs4 import BeautifulSoup
import pandas as pd


def create_customer_property_details_table(customer_input_file, property_input_file, output_file):
    """This function will create two DataFrames, one for customer_data, other one for property data.
       Then it will join these two DataFrames using property address and customer address as a key."""

    """ Creating a pandas DataFrame for Customer Data.
    """
    url_cust = r"D:/rp_scraping/input/{}.html".format(customer_input_file)
    file_cust = open(url_cust)

    customer_details = {"First Name": [],
                        "Last Name": [],
                        "Address": [],
                        "Address(abrv.)": [],
                        "Phone Number": [],
                        "DNCR_IND": [],
                        "Bedrooms": [],
                        "Bathrooms": [],
                        "Car Space": [],
                        "Est. Land Area(m2)": []}

    soup = BeautifulSoup(file_cust, "html.parser")

    summaryListItems_cust = soup.find_all("div", {"class": "summaryListItem"})
    for i in range(len(summaryListItems_cust)):
        content = summaryListItems_cust[i].find("div", {"class": "content"})
        iconContainer = summaryListItems_cust[i].find("ul", {"class": "iconContainer"})
        heading = summaryListItems_cust[i].find("h2")
        attribute_list = iconContainer.text.strip().split()
        content_text = content.text

        if content_text.strip() != "No information available.":

            contact_name = content.find_all("td", {"class": "contactName"})
            contact_address_abrv = content.find_all("td", {"class": "contactAddress"})
            contact_address = (" ".join(heading.text.strip().split()).replace(",", "")).upper()
            contact_number = content.find_all("td", {"class": "phoneNumber"})

            for (nam, num, add) in zip(contact_name, contact_number, contact_address_abrv):
                name = nam.text.strip().split()
                fName = name[0]
                lName = name[1]
                address_abrv = " ".join(add.text.strip().split())
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

                    customer_details["Address(abrv.)"].append(address_abrv)
                    customer_details["Phone Number"].append(number)
                    customer_details["Bedrooms"].append(contact_bedroom)
                    customer_details["Bathrooms"].append(contact_bathroom)
                    customer_details["Car Space"].append(contact_car_space)
                    customer_details["Est. Land Area(m2)"].append(contact_lot_area)

    customer_details_df = pd.DataFrame(customer_details)

    """Creating a pandas DataFrame for Property Data."""
    url_prop = r"D:/rp_scraping/input/{}.html".format(property_input_file)
    file_prop = open(url_prop)

    soup_prop = BeautifulSoup(file_prop.read(), "html.parser")

    summaryListItem_prop = soup_prop.find_all("div", {"class": "summaryListItem"})

    property_details = {"Address": [],
                        "Sale Price": [],
                        "Sale Date": [],
                        "Lot Plan": [],
                        "Category": [],
                        "Zoning": [],
                        "Land Use": [],
                        "Eq. Building Area": []}

    for i in range(len(summaryListItem_prop)):
        heading = summaryListItem_prop[i].find("h2")
        summaryListItemContent = summaryListItem_prop[i].find_all("ul", {"class": "summaryListItemContent"})

        address = (" ".join(heading.text.strip().split()).replace(",", "")).upper()

        lists = summaryListItemContent[0].find_all("li")

        property_details["Address"].append(address)

        sale_price = lists[0].text.strip().split("$")
        sale_date = lists[1].text.strip().split(":\n")
        lot_plan = lists[2].text.strip().split(":\n")
        category = lists[3].text.strip().split(":\n")
        zoning = lists[4].text.strip().split(":\n")
        land_use = lists[5].text.strip().split(":\n")

        try:
            building_area = lists[6].text.strip().split(":\n")
        except:
            building_area = None

        if len(sale_price) == 2:
            property_details["Sale Price"].append(sale_price[1])  # append sale price for a property
        else:
            property_details["Sale Price"].append("-")  # if no sale price, append "-"

        if len(sale_date) == 2:
            property_details["Sale Date"].append(sale_date[1])  # append sale date for a property
        else:
            property_details["Sale Date"].append("-")  # if no sale date, append "-"

        if len(lot_plan) == 2:
            property_details["Lot Plan"].append(lot_plan[1])  # append lot_plan for a property
        else:
            property_details["Lot Plan"].append("-")  # if no lot_plan, append "-"

        if len(category) == 2:
            property_details["Category"].append(category[1])  # append category of a property
        else:
            property_details["Category"].append("-")  # if no property, append "-"

        if len(zoning) == 2:
            property_details["Zoning"].append(zoning[1])  # append zoning for a property
        else:
            property_details["Zoning"].append("-")  # if no zoning, append "-"

        if len(land_use) == 2:
            property_details["Land Use"].append(land_use[1])  # append land use to a property
        else:
            property_details["Land Use"].append("-")  # if no land use, append "-"

        if (building_area is not None) and (len(building_area) == 2):
            property_details["Eq. Building Area"].append(building_area[1].replace("m2", ""))
        else:  # append building_area to a property
            property_details["Eq. Building Area"].append("-")  # if no building area, append "-"

    property_details_df = pd.DataFrame(property_details)

    cust_prop_df = pd.merge(customer_details_df, property_details_df, how="left", on="Address")

    cust_prop_df.to_csv(f"D:/rp_scraping/output/{output_file}.csv", header=True, index=False, mode="a")


create_customer_property_details_table("3021_customer_1", "3021_property_1", "3021_cust_prop_1")
