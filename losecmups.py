from bs4 import BeautifulSoup
import requests
import unicodedata
import pandas as pd
from datetime import datetime
import re

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

def addPriceData(data, vendor,unit_price,price,qty):
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
            print("Produto indisponivel ou nao foi possivel encontrar preço para ",vendor)
            print("URL: ",url)
            
      return data;

if __name__ == '__main__':
      # create initial dataframe with column naming
      data = pd.DataFrame(columns=['name','unit_price','price','qty','date'])
      #start grabing data
      data = grabPrice("PagueMenos","https://www.paguemenos.com.br/losec-mups-10mg-com-14-comprimidos/p","vtex-store-components-3-x-sellingPriceValue",14,data)
      data = grabPrice("PagueMenos","https://www.paguemenos.com.br/losec-mups-10mg-com-28-comprimidos/p","vtex-store-components-3-x-sellingPriceValue",28,data)
      data = grabPrice("Panvel","https://www.panvel.com/panvel/losec-mups-10mg-14-capsulas/p-396745","item-price__value",14,data)
      data = grabPrice("DrogaRaia","https://www.drogaraia.com.br/losec-mups-10-mg-14-comprimidos-revestidos.html",["price","regular-price"],14,data)
      #sort so that lowest price can be displayed
      data = data.sort_values(by=['unit_price'])
      #print lowest price
      print(data.iloc[0]['date'],": ",data.iloc[0]['name'], " R$", data.iloc[0]['price']," - Caixa com ",data.iloc[0]['qty'],"cp")
      try:
            # open existing excel file
            filename='C:\\Users\\Luciano_M_Rodrigues\\Documents\\LosecMups.xlsx'
            xlsL = pd.ExcelFile(filename)
            dfOriginal = pd.read_excel(xlsL, 'Sheet1')
      except:
            dfOriginal = pd.DataFrame(columns=['name','unit_price','price','qty','date'])

      #append to the excel file
      dfOutput = pd.DataFrame.append(dfOriginal,data,sort=False)
      #sort by lowest unit price
      dfOutput = dfOutput.sort_values(by=['unit_price'])
      #save excel
      dfOutput.to_excel(filename, sheet_name='Sheet1',encoding='utf-8',index=False)