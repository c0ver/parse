from lxml import html
import requests
from requests import session
import cfscrape
payload = {
    'username': 'hirwo',
    'password': 'blueskies'
}
s = requests.session()
scraper = cfscrape.create_scraper(s)


#this line is needed to bypass cloudflare; most important line!!!!!!!!!!!
scraper.get('http://kissanime.to/Login')


#login
scraper.post('http://kissanime.to/Login', data=payload)
episode_list = scraper.get('http://kissanime.to/Anime/Shigatsu-wa-Kimi-no-Uso', headers={ 'User-Agent': 'Mozilla/5.0' })
episode_tree = html.fromstring(episode_list.content)
episode_links = episode_tree.xpath('//a[@class="episodeVisited"]/@href')
for episode in episode_links:
    video_page = scraper.get('http://kissanime.to' + episode, headers={ 'User-Agent': 'Mozilla/5.0' })
    video_tree = html.fromstring(video_page.content)
    download_link = video_tree.xpath('string(//div[@id="divDownload"]/a[1]/@href)')
    resolution = video_tree.xpath('string(//div[@id="divDownload"]/a[1]/text())')
    print download_link, resolution
