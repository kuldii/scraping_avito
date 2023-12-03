from bs4 import BeautifulSoup
import requests 

# Page available => 1 - 100
for page in range(1,2):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.avito.ru/ekaterinburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p=88&s=1"
    print(url)
    req = requests.get(url, headers=headers)
    print(req.status_code)
    
    if(req.status_code == 200):
        bs = BeautifulSoup(req.content, "lxml")
        
        container = bs.find_all("div", attrs={"elementtiming":"bx.catalog.container"})
        rawItems = container[0].find_all(attrs={"data-marker":"item"})
        
        for rawItem in rawItems:
            product = dict()
            product["id"] = rawItem["id"]
            product["itemId"] = rawItem["data-item-id"]
            product["detailUrl"] = "https://www.avito.ru" + rawItem.a["href"]
            product["meta"] = rawItem.meta["content"].replace("\n", "").strip()
            
            ulFoto = rawItem.find("ul")
            liFoto = ulFoto.li
            
            try:
                product["thumbnail"] = str(liFoto["data-marker"]).replace("slider-image/image-", "").strip()
            except:
                product["thumbnail"] = "https://www.avito.ru/dstatic/build/assets/1495ba76817384db.svg"
            
            product["title"] = rawItem.h3.text
            product["price"] = rawItem.p.text.replace(" ", "").replace("₽", "").strip()
            
            print(product)