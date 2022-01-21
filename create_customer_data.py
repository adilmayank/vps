import pandas as pd
from bs4 import BeautifulSoup

class Scrape:
    def __init__(self):
        pass
    def scrape_contact_deatils_from_html(self, path, number_of_files=1):

        def scrape_details(file=None, header=None):

            opened_file = open(file)

            customer_details = {"First Name": [],
                                "Last Name": [],
                                "Address": [],
                                "Phone Number": [],
                                "DNCR_IND": []}

            soup = BeautifulSoup(opened_file, "html.parser")

            summary_list_items = soup.find_all("div", {"class": "summaryListItem"})

            for item in summary_list_items:
                data_table = item.find("table")
                if data_table is not None:
                    number_of_rows = len(data_table.find_all("tr")) - 1
                    for i in range(number_of_rows):

                        contact_number = data_table.find_all("td", {"class": "phoneNumber"})[i].text.strip().split()
                        if len(contact_number) != 0:
                            contact_number_proper = "".join(contact_number)
                            to_replace = "()"
                            for character in to_replace:
                                contact_number_proper = contact_number_proper.replace(character, "")            # removes paranthesis from the contact number
                        else:
                            continue                                                                            # passes the iteration if contact number field is empty

                        contact_name= data_table.find_all("td", {"class": "contactName"})[i].text.split()
                        contact_address = data_table.find_all("td", {"class": "contactAddress"})[i].text.split()
                        DNCR_IND = ""

                        first_name = contact_name[0]
                        last_name = contact_name[1]
                        contact_address_proper = " ".join(contact_address)

                        if (contact_number_proper[0] == "^"):
                            DNCR_IND = "Y"
                            contact_number_proper = contact_number_proper.replace("^", "")
                        else:
                            DNCR_IND = "N"

                        customer_details["First Name"].append(first_name)
                        customer_details["Last Name"].append(last_name)
                        customer_details["Address"].append(contact_address_proper)
                        customer_details["Phone Number"].append(contact_number_proper)
                        customer_details["DNCR_IND"].append(DNCR_IND)

            pd.DataFrame(customer_details).to_csv(f"E:/rp_scraping/test.csv",
                                                  header=header,
                                                  index=False,
                                                  mode="a")

        
        # first_file and subsequent_file name should be updated with the current postal_code in the source code.
        
        first_file = path + rf"\3340_customer_{1}.html"                             # creates a csv with first file with headers.
        scrape_details(first_file, header=True)
        if (number_of_files > 1):                                                   # append data from subsequent files if number of files is greater than 1.
            for file_number in range(2, number_of_files + 1):
                subsequent_file = path + rf"\3340_customer_{file_number}.html"
                scrape_details(subsequent_file, header=False)
