This repository contains python scripts, that retrieves information from RP Data website.
<br><br>
Since accessing information requires logging into our account, a work-around was developed. After logging into the account, each page's sources code will be saved locally in a folder, with a specific string format, as a HTTP file.
<br><br>
Now when the script get executed, it will look for all the files with a pre-defined format and extract the customer and property data in a tabular form in another folder locally.
<br><br>
File ---> create_customer_data.py is used to scrape customer data from the html files saved locally in a folder. It has a class named "Scrape" whose object needs to be instantiated first and then a function defined ---> "scrape_contact_deatils_from_html(self, path, number_of_files=1)" is invoked. It takes path of the folder where we have all the files for a particular postal code, additionally it takes a parameter, number of files.
<br><br>
For now, we need to manually chance the postal code in the source code in order to run the code. In some days I'll udpate the script which will take an extra argument named postal code, for ease.
