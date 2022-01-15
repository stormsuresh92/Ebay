from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm

s = HTMLSession()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer':'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=laptop&_sacat=0',
    'Connection':'keep-alive'
}

Productdata = []

def page(x):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={query}&_sacat=0&_pgn={x}'
    r = s.get(url, headers=headers)
    contents = r.html.find('li.s-item.s-item__pl-on-bottom.s-item--watch-at-corner')
    for item in tqdm(contents):
        try:
            ti = item.find('h3.s-item__title', first=True).text.replace('New Listing', '')
        except:
            ti = ''
        try:
            brand = item.find('div.s-item__subtitle', first=True).text
        except:
            brand = ''
        try:
            price = item.find('span.s-item__price', first=True).text
        except:
            price = ''
        try:
            scost = item.find('span.s-item__shipping.s-item__logisticsCost', first=True).text.replace('shipping', '')
        except:
            scost = ''
        try:
            scountry = item.find('span.s-item__location.s-item__itemLocation', first=True).text.replace('from', '').strip()
        except:
            scountry = ''
        try:
            rating = item.find('span.clipped', first=True).text.replace(' out of 5 stars.', '')
        except:
            rating = ''
        try:
            bid = item.find('span.s-item__bids.s-item__bidCount', first=True).text
        except:
            bid = ''
        try:
            timeleft = item.find('span.s-item__time-left', first=True).text
        except:
            timeleft = ''
        try:
            purl = item.find('a.s-item__link', first=True).attrs['href']
        except:
            purl = ''
        
        dic = {
            'Product':ti,
            'Subtitle':brand,
            'Price':price,
            'Shipping_Cost':scost,
            'Shipping_Country':scountry,
            'Rating':rating,
            'Bids':bid,
            'Bid_Time_Left':timeleft,
            'Product_Url':purl
        }

        Productdata.append(dic)

query = input('Enter your product name:')
endpage = int(input('How many pages you want to scrape:'))
for x in range(1, endpage):
    page(x)


df = pd.DataFrame(Productdata)
df.to_csv(f'{query}.csv', index=False)
print('fin')