from lxml import html
import requests
from requests import session
import cfscrape
import os
import sys
import Queue
import threading

q = Queue.Queue()
threads = []

#anime_name = raw_input("Type the anime's name without capitals: " + '\n')
anime_name = "fate-zero"
anime_name = anime_name.replace(' ', '-')

if not os.path.exists(anime_name):
    os.makedirs(anime_name)

payload = {
    'username': 'hirwo',
    'password': 'blueskies'
}

#create scraper to bypass cloudflare
s = requests.session()
scraper = cfscrape.create_scraper(s)

#check if cloudflare is successfully bypassed
check_cloudflare = scraper.get('http://kissanime.to/Login', headers={ 'User-Agent': 'Mozilla/5.0' })
check_cloudflare_tree = html.fromstring(check_cloudflare.content)
login_name = check_cloudflare_tree.xpath('string(//a[@href="http://kissanime.to/Login"]/text())')
if login_name == "login":
    print "Successfully Bypassed Cloudflare."
else:
    print login_name
    print "Blocked by Cloudflare."
    print check_cloudflare.content
    sys.exit(0)

#this line is needed to bypass cloudflare
scraper.get('http://kissanime.to/Login')
#login
scraper.post('http://kissanime.to/Login', data=payload)

episode_list = scraper.get('http://kissanime.to/Anime/' + anime_name, headers={ 'User-Agent': 'Mozilla/5.0' })
episode_tree = html.fromstring(episode_list.content)

login_check = episode_tree.xpath('string(//*[@id="topHolderBox"]/span/text())')
if login_check == "Hi":
    print "Successfully Logged In."
else:
    print login_check
    print "Unsuccessful Login."
    print episode_list.content
    sys.exit(0)

episode_links = episode_tree.xpath('//a[@class="episodeVisited"]/@href')
N_episodes = len(episode_links)

print "Number of Episodes: ", N_episodes
if N_episodes == 0:
    print "Possible error with internet connection."
    sys.exit(0)

#order episodes from first to last
for x in range(N_episodes / 2):
    a, b = episode_links[x], episode_links[N_episodes - x - 1]
    episode_links[x] = b
    episode_links[N_episodes - x - 1] = a

def download_url(q, url, name):
    response = scraper.get(url, stream=True)
    print "****Connected****"
    f = open(name,'wb')
    print "Downloading....."
    for chunk in response.iter_content(chunk_size=1024 * 512): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

    print "Done", '\n'


for x in range(N_episodes):
    print "Episode " + str(x+1) + ":"
    video_page = scraper.get('http://kissanime.to' + episode_links[x], headers={ 'User-Agent': 'Mozilla/5.0' })
    video_tree = html.fromstring(video_page.content)

    download_link = video_tree.xpath('string(//div[@id="divDownload"]/a[1]/@href)')
    resolution = video_tree.xpath('string(//div[@id="divDownload"]/a[1]/text())')
    print resolution
    print download_link

    file_name = anime_name + "/" + str(x + 1) + '.mp4'
    print file_name

    download_link_size = scraper.head(download_link)
    print "Size:", download_link_size.headers['content-length']

    t = threading.Thread(target = download_url, args = (q, download_link, file_name))
    t.daemon = True
    threads.append(t)
    print '\n'

for x in threads:
    x.start()

for x in threads:
    x.join()