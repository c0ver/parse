#use keep-alive if parsing from the same server

import urllib2
from urlgrabber.keepalive import HTTPHandler
from lxml import html
import requests
import os
import time
import threading
import Queue
if not os.path.exists('witch-craft-works'):
    os.makedirs('witch-craft-works')

def run_parallel_in_threads(target, args_list):
    result = Queue.Queue()
    # wrapper to collect return value in a Queue
    def task_wrapper(*args):
        result.put(target(*args))
    threads = [threading.Thread(target=task_wrapper, args=args) for args in args_list]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

def dummy_task(n):
    for i in xrange(n):
        time.sleep(0.1)
    return n

manga_main_page = requests.get('http://www.mangareader.net/witch-craft-works')
manga_main_page_t = html.fromstring(manga_main_page.content)

chapter_list = manga_main_page_t.xpath('//tr[@class="table_head"]/../tr/td/a/@href')

keepalive_handler = HTTPHandler()
opener = urllib2.build_opener(keepalive_handler)
opener.addheaders = [('User-Agent', 'Chrome/53.0.2785.116')]
urllib2.install_opener(opener)

def fetch(url):
    response = urllib2.urlopen(url)
    jpgData = response.read()
    f = open(file_name, 'w')
    f.write(jpgData)
    f.close()

for chapter_N in range(len(chapter_list)):
    if not os.path.exists('witch-craft-works/' + str(chapter_N + 1)):
        os.makedirs('witch-craft-works/' + str(chapter_N + 1))

    chapter = chapter_list[chapter_N]
    chapter_page = requests.get('http://www.mangareader.net' + chapter)
    chapter_page_t = html.fromstring(chapter_page.content)

    N_pictures = chapter_page_t.xpath('//select[@id="pageMenu"]/option[last()]/text()')
    N = int(N_pictures[0])
    picture_url = []

    for page in range(0, 2):
        chapter_page = requests.get('http://www.mangareader.net' + chapter + '/' + str(page + 1))
        chapter_page_t = html.fromstring(chapter_page.content)

        url = chapter_page_t.xpath('string(//div[@id="imgholder"]/a/img/@src)')
        url = tuple([url])
        picture_url.append(url)
        file_name = "witch-craft-works/" + str(chapter_N + 1) + "/" + str(page + 1) + ".jpg"
    
    urls = [
        ('http://www.google.com/',),
        ('http://www.lycos.com/',),
        ('http://www.bing.com/',),
        ('http://www.altavista.com/',),
        ('http://achewood.com/',),
    ]

    run_parallel_in_threads(fetch, picture_url)

        
        