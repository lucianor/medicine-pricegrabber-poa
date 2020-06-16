from bs4 import BeautifulSoup
import requests
import unicodedata
import numpy as np
import pandas as pd
from datetime import datetime
import re

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")


def grabPrice(vendor, url, component, qty , dataArr):
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')
      products = soup.findAll('span', class_=component)
      if (len(products) == 1):
            product = products[0]
            price_text = unicodedata.normalize("NFKD", product.get_text())
            price_text = re.sub(r"\s+", "", price_text)
            price_text = price_text.strip("R$").replace(",",".")
            price = float(price_text)
            unit_price = float(price / qty)
            data = np.append(dataArr, np.array( [(vendor,unit_price,price,qty,current_time)], dtype=dtype))
            return data;
      
      if (len(products) == 3): #drogaraia
            # combo promo price
            product = products[2]
            price_text = unicodedata.normalize("NFKD", product.get_text())
            price_text = re.sub(r"\s+", "", price_text)
            price_text = price_text.strip("R$").replace(",",".")
            price = float(price_text)
            unit_price = float(price / qty)
            data = np.append(dataArr, np.array( [(vendor,unit_price,price,qty,current_time)], dtype=dtype))
            
            # price without combo
            product = products[1]
            price_text = unicodedata.normalize("NFKD", product.get_text())
            price_text = re.sub(r"\s+", "", price_text)
            price_text = price_text.strip("R$").replace(",",".")
            price = float(price_text)
            unit_price = float(price / qty)
            data = np.append(data, np.array( [(vendor,unit_price,price,qty,current_time)], dtype=dtype))
            
            return data;
      
      if (len(products) == 2): #drogaraia
            # combo promo price
            product = products[1]
            price_text = unicodedata.normalize("NFKD", product.get_text())
            price_text = re.sub(r"\s+", "", price_text)
            price_text = price_text.strip("R$").replace(",",".")
            price = float(price_text)
            unit_price = float(price / qty)
            data = np.append(dataArr, np.array( [(vendor,unit_price,price,qty,current_time)], dtype=dtype))
            
            # price without combo
            product = products[0]
            price_text = unicodedata.normalize("NFKD", product.get_text())
            price_text = re.sub(r"\s+", "", price_text)
            price_text = price_text.strip("R$").replace(",",".")
            price = float(price_text)
            unit_price = float(price / qty)
            data = np.append(data, np.array( [(vendor,unit_price,price,qty,current_time)], dtype=dtype))
            
            return data;

      if (len(products) == 0):
            print("Produto indisponivel ou nao foi possivel encontrar preço para ",vendor)
            print("URL: ",url)
            return dataArr;

if __name__ == '__main__':
      dtype = [('name', 'S10'), ('unit_price', float),('price', float),('qty', int),('date','S20')]
      data = np.array([],dtype=dtype)
      data = grabPrice("PagueMenos","https://www.paguemenos.com.br/losec-mups-10mg-com-14-comprimidos/p","vtex-store-components-3-x-sellingPriceValue",14,data)
      data = grabPrice("PagueMenos","https://www.paguemenos.com.br/losec-mups-10mg-com-28-comprimidos/p","vtex-store-components-3-x-sellingPriceValue",28,data)
      data = grabPrice("Panvel","https://www.panvel.com/panvel/losec-mups-10mg-14-capsulas/p-396745","item-price__value",14,data)
      data = grabPrice("DrogaRaia","https://www.drogaraia.com.br/losec-mups-10-mg-14-comprimidos-revestidos.html",["price","regular-price"],14,data)

      #sort so that lowest price can be displayed
      np.sort(data, order='unit_price')

      #print lowest price
      print(current_time,": ",data[0][0], " R$", data[0][2]," - Caixa com ",data[0][3],"cp")
      
      try:
            # open existing excel file
            filename='C:\\Users\\Luciano_M_Rodrigues\\Documents\\LosecMups.xlsx'
            xlsL = pd.ExcelFile(filename)
            dfOriginal = pd.read_excel(xlsL, 'Sheet1')
      except:
            dfOriginal = pd.DataFrame()
     
      #create panda dataframe
      dfNew = pd.DataFrame(data)
      
      #append to the excel file
      dfOutput = pd.DataFrame.append(dfOriginal,dfNew,sort=False)
      #sort by lowest unit price
      dfOutput = dfOutput.sort_values(by=['unit_price'])

      #save excel
      dfOutput.to_excel(filename, sheet_name='Sheet1',encoding='utf-8',index=False)
