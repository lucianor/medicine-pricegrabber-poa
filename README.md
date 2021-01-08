# medicine-pricegrabber-poa
Grab prices from pharmacies in Porto Alegre

This is a custom code to grab prices from Panvel, DrogaRaia and Pague Menos pharmacies in Brazil.
It will show in console the lowest price at the moment, and export it to Excel.

You can specify the product pages, and it will automatically grab the price and even compare unit price between different 
product quantities.

Example: 

20 pills with a price of BRL 70, costs 3.5 BRL for each pill

40 pills with a price of BRL 130, costs 3.25 BRL for each pill

*TODO LIST*

-separate grabbing for each pharmacy

-create global grabbing methods and classes

Requirements
------------
Python 3

Pandas 

BeautifulSoup4 

$ pip install bs4 pandas
