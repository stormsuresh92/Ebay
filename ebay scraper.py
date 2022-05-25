from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm

s = HTMLSession()

data = []

keyword = input('ENTER YOUR KEYWORD HERE: ')

urls = ['https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_pgn={}'.format(keyword, x) for x in range(1, 6)]
for url in tqdm(urls):
	r = s.get(url.strip())
	content = r.html.find('div.s-item__info.clearfix')
	for items in tqdm(content):
		title = items.find('h3.s-item__title', first=True).text
		subtitle = items.find('div.s-item__subtitle span', first=True).text
		price = items.find('span.s-item__price', first=True).text
		try:
			discountprice = items.find('span.s-item__discount.s-item__discount', first=True).text
		except:
			discountprice = ''
		try:
			shippingprice = items.find('span.s-item__shipping.s-item__logisticsCost', first=True).text.replace('shipping', '')
		except:
			shippingprice = ''
		try:
			shippingfrom = items.find('span.s-item__location.s-item__itemLocation', first=True).text.replace('from', '')
		except:
			shippingfrom = ''

		url = items.find('a.s-item__link', first=True).attrs['href']

		
		data.append([title, subtitle, price, discountprice, shippingprice, shippingfrom, url])

df = pd.DataFrame(data, columns=['Title', 'Sub Title', 'Price', 'Discount Price', 'Shipping Price', 'Shipping From', 'Url'])
df.to_csv(f'{keyword}.csv', index=False)