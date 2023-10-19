from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time 



class Nike2Spider():
    def __init__(self, search_query) -> None:
        self.search_query = search_query
        self.base_url : str = 'https://www.nike.com/id/w/'
       

    def GetProductLink(self,html_url):
            soup = BeautifulSoup(html_url, "html.parser")
            productCard = soup.find_all("a", attrs={"class": "product-card__link-overlay", "data-testid" : "product-card__link-overlay"})
            linkProduct = [item.get("href") for item in productCard]

            return linkProduct

    def get_pages(self) :
        params= {
            "q": self.search_query.replace(" ","%20"),
            "vst" : self.search_query.replace(" ","%20")
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_viewport_size(
                {"width": 1280, "height": 1080}
            )
            full_url = f"{self.base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"

            page.goto(full_url)
            time.sleep(2)

            #Scrolling
            keep_scroll = True
            while keep_scroll:
                page.keyboard.press("End")
                print("Scrolling key press")
                time.sleep(1)
                if page.evaluate('window.scrollY + window.innerHeight >= document.body.scrollHeight'):
                    keep_scroll = False

            html = page.inner_html("#skip-to-products")
            linkProduct = self.GetProductLink(html)
            browser.close()
            return linkProduct
            
           
        
            
            

    
        


   