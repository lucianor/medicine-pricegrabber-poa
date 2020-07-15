from bs4 import BeautifulSoup
import requests
import unicodedata
import pandas as pd
from datetime import datetime
import re

# execution time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def addPriceData(data, vendor, unit_price, price, qty):
      new_row = pd.DataFrame({'name':vendor, 
                              'unit_price': unit_price,
                              'price': price,
                              'qty': qty,
                              'date': current_time},index=[0])
      dfOut = pd.DataFrame.append(data, new_row, ignore_index=True)
      return dfOut

def stripPrice(price_text):
      price_text = unicodedata.normalize("NFKD", price_text) # utf-8 normalization required for some sites
      price_text = re.sub(r"\s+", "", price_text) # remove all spaces with a regex
      price_text = price_text.strip("R$").replace(",",".") # remove R$ and replace decimal sign for casting 
      price = float(price_text)
      return price

def grabPrice(vendor, url, component, qty , data):
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')
      products = soup.findAll('span', class_=component)
      if ((len(products) >= 1) and (len(products) <= 2)):
            price = stripPrice(products[0].get_text())
            unit_price = float(price / qty)
            data = addPriceData(data, vendor,unit_price,price,qty);
      if (len(products) == 3): #drogaraia
            # combo promo price
            price = stripPrice(products[2].get_text())
            unit_price = float(price / qty)
            data = addPriceData(data, vendor,unit_price,price,qty);
      if (len(products) >= 2): #drogaraia
            # combo promo price
            price = stripPrice(products[1].get_text())
            unit_price = float(price / qty)
            data = addPriceData(data, vendor,unit_price,price,qty);
      if (len(products) == 0):
            print("Product unavailable or unable to obtain price for ",vendor)
            print("URL: ",url)
            
      return data;

if __name__ == '__main__':
      #COLIDS
      # create initial dataframe with column naming
      data = pd.DataFrame(columns=['name','unit_price','price','qty','date'])

      #start grabing data
      data = grabPrice("PagueMenos","https://www.paguemenos.com.br/colidis-gotas-5ml-colidis-gotas-5ml-colikids/p","vtex-store-components-3-x-sellingPriceValue",1,data)
      data = grabPrice("Panvel","https://www.panvel.com/panvel/colidis-gotas-5ml/p-118734","item-price__value",1,data)
      data = grabPrice("DrogaRaia","https://www.drogaraia.com.br/colidis-5ml.html",["price","regular-price"],1,data)
      #sort so that lowest price can be displayed
      data = data.sort_values(by=['unit_price'])
      #print lowest price
      print(data.iloc[0]['date'],": COLIDIS -",data.iloc[0]['name'], " R$", data.iloc[0]['price'])
      try:
            # open existing excel file
            filename='C:\\Users\\Luciano_M_Rodrigues\\Documents\\Colids.xlsx'
            xlsL = pd.ExcelFile(filename)
            dfOriginal = pd.read_excel(xlsL, 'Sheet1')
      except:
            dfOriginal = pd.DataFrame(columns=['name','unit_price','price','qty','date'])

      #append to the excel file
      dfOutput = pd.DataFrame.append(dfOriginal,data,sort=False)
      #sort by lowest unit price
      dfOutput = dfOutput.sort_values(by=['unit_price'])
      #save excel
      try:
            dfOutput.to_excel(filename, sheet_name='Sheet1',encoding='utf-8',index=False)
      except:
            print("Unable to save file. Maybe it's open?")