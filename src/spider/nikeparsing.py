from httpx import Client
from bs4 import BeautifulSoup
import json
import time 

class NikeparsingSpider(object):
    def __init__(self,listLink) -> None:
        self.listLink = listLink
        self.client : Client = Client()
        self.user_agent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        
    def get_color(self, soup):
        """
        Getting All Colour of Product
        """
        colorTags = soup.css.select(".colorways img")
        colors = [color.get("alt") for color in colorTags]
        return colors

        

    def req_page(self):
        listProduct = []
        headers = self.user_agent
        for item in self.listLink:
            # request ke website
            response = self.client.get(item, headers=headers)
            soup = BeautifulSoup(response, "html.parser")

            #Parsing Data Product
            try:
                productDataDetail = soup.css.select_one("script[type='application/ld+json']").getText()
                jsonData = json.loads(productDataDetail)

                try:
                    name = jsonData["name"]
                except:
                    name = None
                
                try:
                    price = jsonData["offers"]["price"]
                except:
                    price = jsonData["offers"]["highPrice"]
                
                try:
                    img = jsonData["image"]
                except:
                    img = None
                
                try:
                    color = jsonData["color"]
                except:
                    color = self.get_color(soup)
                
                #Add data into object then store in array
                data = {
                "Name" : name,
                "Price" : price,
                "Img" : img,
                "color" : color
                }
                listProduct.append(data)
            except AttributeError as err:
                print(f"Error Message: {err}")
                print(f"Error Link: {item}")
                continue

        result = {
            "Product" : listProduct
        }
        with open("result.json", "w") as file:
            json.dump(result, file)

        return listProduct