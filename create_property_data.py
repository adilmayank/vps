from bs4 import BeautifulSoup
import pandas as pd


def create_property_details_table(input_file, output_file):

    url = r"D:/rp_scraping/input/{}.html".format(input_file)
    page = open(url)

    soup = BeautifulSoup(page.read(), "html.parser")

    summaryListItem = soup.find_all("div", {"class": "summaryListItem"})

    property_details = {"Address": [],
                        "Sale Price": [],
                        "Sale Date": [],
                        "Lot Plan": [],
                        "Category": [],
                        "Zoning": [],
                        "Land Use": [],
                        "Eq. Building Area": []}

    for i in range(len(summaryListItem)):
        heading = summaryListItem[i].find("h2")
        summaryListItemContent = summaryListItem[i].find_all("ul", {"class": "summaryListItemContent"})

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
            building_area = lists[6].text.strip().split(":\n")              # just in case an exception occurs.
                                                                             
        except:
            building_area = None                                            # in case of error, we assign building_area to None.

        if len(sale_price) == 2:
            property_details["Sale Price"].append(sale_price[1])            # append sale price for a property
        else:
            property_details["Sale Price"].append("-")                      # if no sale price, append "-"

        if len(sale_date) == 2:
            property_details["Sale Date"].append(sale_date[1])              # append sale date for a property
        else:
            property_details["Sale Date"].append("-")                       # if no sale date, append "-"

        if len(lot_plan) == 2:
            property_details["Lot Plan"].append(lot_plan[1])                # append lot_plan for a property
        else:
            property_details["Lot Plan"].append("-")                        # if no lot_plan, append "-"

        if len(category) == 2:
            property_details["Category"].append(category[1])                # append category of a property
        else:
            property_details["Category"].append("-")                        # if no property, append "-"

        if len(zoning) == 2:
            property_details["Zoning"].append(zoning[1])                    # append zoning for a property
        else:
            property_details["Zoning"].append("-")                          # if no zoning, append "-"

        if len(land_use) == 2:
            property_details["Land Use"].append(land_use[1])                # append land use to a property
        else:
            property_details["Land Use"].append("-")                        # if no land use, append "-"

        if (building_area is not None) and (len(building_area) == 2):
            property_details["Eq. Building Area"].append(building_area[1].replace("m2", ""))
        else:                                                               # append building_area to a property
            property_details["Eq. Building Area"].append("-")               # if no building area, append "-"

    print(property_details)

    customer_details_df = pd.DataFrame(property_details).to_csv(f"D:/rp_scraping/output/{output_file}.csv",
                                                                    header=True,
                                                                    index=False,
                                                                    mode="a")


# Call the function here with proper arguments to create a .csv file
# Make nessesary changes in the input and output directory strings, that loads and save files from local system.
