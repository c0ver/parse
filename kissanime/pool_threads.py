from lxml import html
import requests
from requests import session
import cfscrape
import os
import sys
import Queue
import threading
from multiprocessing import Pool as ThreadPool
from functools import partial
import time
import os.path
import copy

#create scraper to bypass cloudflare
scraper = cfscrape.create_scraper()

#a list of anime that had problems downloading
problem_anime = []

#the links of all the anime videos
download_link = []

anime_name = None

def create_scraper():
    payload = {
        'username': 'hirwo',
        'password': 'blueskies'
    }

    #check if cloudflare is successfully bypassed
    check_cloudflare = scraper.get('http://kissanime.to/Login', headers={ 'User-Agent': 'Mozilla/5.0' })
    if check_cloudflare.headers['Connection'] == 'keep-alive':
        print "Successfully Bypassed Cloudflare."
    else:
        print "Blocked by Cloudflare."
        print check_cloudflare.content
        sys.exit(0)

    #this line is needed to bypass cloudflare
    scraper.get('http://kissanime.to/Login')
    #login
    scraper.post('http://kissanime.to/Login', data=payload)

def download_url(file_names, episode_N):
    print len(download_link)
    print episode_N
    print download_link[0]
    file_name = file_names[episode_N - 1]
    url = download_link[episode_N - 1]
    file_name = file_name.replace('\r\n', '')
    name = (anime_name + '/' + file_name + '.mp4')
    response = scraper.get(url, stream=True)
    print "****Connected to " + file_name + "****"
    f = open(file_name,'wb')
    print "Downloading " + file_name + "....."
    for chunk in response.iter_content(chunk_size=1024 * 512): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()

    print "Finished " + file_name + "."

def get_anime_episodes():
    if not os.path.exists(anime_name):
        os.makedirs(anime_name)

    episode_list = scraper.get('http://kissanime.to/Anime/' + anime_url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246' })
    episode_tree = html.fromstring(episode_list.content)
    login_check = episode_tree.xpath('string(//*[@id="topHolderBox"]/span/text())')
    if login_check == "Hi":
        print "Successfully Logged In."
    else:
        print login_check
        print "Unsuccessful Login."
        print episode_list.content
        problem_anime.append(anime_name)
        return

    #ignore <tbody></tbody>
    episode_links = episode_tree.xpath('//table[@class="listing"]/tr/td/a/@href')
    file_names = episode_tree.xpath('//table[@class="listing"]/tr/td/a/text()')

    N_episodes = len(episode_links)
    if len(episode_links) != len(file_names):
        print "# of links does not match the # of episodes"
        print episode_links
        print file_names
        problem_anime.append(anime_name)
        return

    print "Number of Episodes: ", N_episodes
    if N_episodes == 0:
        problem_anime.append(anime_name)
        return

    #order episodes from first to last
    for x in range(N_episodes / 2):
        a, b = episode_links[x], episode_links[N_episodes - x - 1]
        c, d = file_names[x], file_names[N_episodes - x - 1]
        episode_links[x], episode_links[N_episodes - x - 1] = b, a
        file_names[x], file_names[N_episodes - x- 1] = d, c

    episode_N = []
    download_link = []

    for x in range(N_episodes):
        #skip if the file is already there
        if not os.path.exists(anime_name + '/' + file_names[x]):
            #keep going until the links are found
            successful = False
            while not successful:
                video_page = scraper.get('http://kissanime.to' + episode_links[x], headers={ 'User-Agent': 'Mozilla/5.0' })
                video_tree = html.fromstring(video_page.content)

                #check if the html page was good
                video_resolution = video_tree.xpath('string(//div[@id="divDownload"]/a[1]/text())')
                if not video_resolution:
                    continue
                else:
                    successful = True

                download_link.append(video_tree.xpath('string(//div[@id="divDownload"]/a[1]/@href)'))
                episode_N.append(x + 1)
                
                print "Acquired Episode: " + str(x + 1) + " Link Successfully."
                time.sleep(10)

    func = partial(download_url, file_names)
    pool.map(func, episode_N)

    pool.close()
    poil.join()

#set number of threads to 8
pool = ThreadPool(8)

#add attributes to scraper
create_scraper()

#open file to parse multiple animes
for x in open("anime.txt"):
    anime_name = copy.copy(x)
    anime_name = anime_name.replace('\n', '')
    anime_url = anime_name.replace(' ', '-')
    print "Downloading " + anime_name
    get_anime_episodes()
    print "Finished " + anime_name
    
print "Problems with Downloading These Anime: ", problem_anime