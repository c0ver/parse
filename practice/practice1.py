from lxml import html
import requests

page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)

#<div title="buyer-name">Carson Busses</div> data points
#<span class="item-price">$29.95</span>

#This will create a list of buyers:
buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')
links = tree.xpath('//@href');

#print links

for link in links:
    page = requests.get(link)
    tree = html.fromstring(page.content)

    buyers.extend(tree.xpath('//div[@title="buyer-name"]/text()'))
    prices.extend(tree.xpath('//span[@class="item-price"]/text()'))

print 'Buyers: ', buyers, '\n'
print 'Prices: ', prices, '\n'