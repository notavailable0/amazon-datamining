from ResearchItems import *
from CatalogueItems import *
from multiprocessing import Manager 
from data1 import *

Catalogue = GetCatalogue('https://www.amazon.co.uk/s?bbn=560798&rh=n%3A310193011&fs=true&ref=lp_310193011_sar')
Catalogue.get_1() 
catalogued_items = Catalogue.get_2()
print(catalogued_items)

multiprocess_info_parsing(data_list)
print(final_data_list)
