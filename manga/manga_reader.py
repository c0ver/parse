# to be used with http://www.mangareader.net/

import urllib2
from lxml import html
import requests
import os

manga_name = raw_input("Type the manga's name without capitals: " + '\n')
manga_name = manga_name.replace(' ', '-')

if not os.path.exists(manga_name):
    os.makedirs(manga_name)

manga_main_page = requests.get('http://www.mangareader.net/' + manga_name)
manga_main_page_t = html.fromstring(manga_main_page.content)

chapter_list = manga_main_page_t.xpath('//tr[@class="table_head"]/../tr/td/a/@href')

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

for chapter_N in range(len(chapter_list)):
    if not os.path.exists(manga_name + '/' + str(chapter_N + 1)):
        os.makedirs(manga_name + '/' + str(chapter_N + 1))
    
    chapter = chapter_list[chapter_N]
    chapter_page = requests.get('http://www.mangareader.net' + chapter)
    chapter_page_t = html.fromstring(chapter_page.content)

    N_pictures = chapter_page_t.xpath('//select[@id="pageMenu"]/option[last()]/text()')
    N = int(N_pictures[0])

    print manga_name + " Chapter: " + str(chapter_N + 1)

    for page in range(1, N+1):
        chapter_page = requests.get('http://www.mangareader.net' + chapter + '/' + str(page))
        chapter_page_t = html.fromstring(chapter_page.content)

        picture_url = chapter_page_t.xpath('//div[@id="imgholder"]/a/img/@src')
        file_name = manga_name + "/" + str(chapter_N + 1) + "/" + str(page) + ".jpg"

        response = opener.open(picture_url[0])
        jpgData = response.read()
        f = open(file_name, 'w')
        f.write(jpgData)
        f.close()

        print picture_url[0]
    
    print '\n'