from udpatedCustomerScrapingScript import Scrape
from bs4 import BeautifulSoup
import pandas as pd

scraper = Scrape()
path = r"E:\rp_scraping\input\3023\burnside"                  #change postalcode\suburb name to appropriate entries during scraping
scraper.scrape_contact_deatils_from_html(path, 30)
