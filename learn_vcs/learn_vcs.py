#libraries needed for parsing
from lxml import html
import requests
from requests import session

#libraries needed to get the date
import time
from datetime import date, timedelta

#insert username and password here
payload = {
    'username': 'henry.zhang',
    'password': '@Vcs5701'
}

#get yesterday's date
homework_date = date.today() - timedelta(1)

#get today's date
#homework_date = date.today()

#get month and day
month = homework_date.strftime("%b")
day = homework_date.strftime("%d")

day_type = raw_input("Enter either 'A' or 'B': ")
if day_type == 'A':
    A_day = True

A_class = ['AP Computer Science A - Mr. Sutterlin - 2016-17', 'Guitar II - Mr. Coates - 2016-17', 'AP English Literature & Composition - Mrs. Wilson - 2016-17', 'AP Economics - Mr. Sisson - 2016-17']
B_class = ['Multi-Variable Calculus - Mrs. Shak - 2016-17', 'Ceramics II - Mrs. Dequine - 2016-17', 'AP Physics C - Mr. Cronquist - 2016-17', 'Community Outreach - Mrs. Nardi - 2016-17']

#use session to log in
with session() as scraper:
    #log in
    scraper.post('http://learn.vcs.net/courses/login/index.php', data=payload)

    main_page = scraper.get('http://learn.vcs.net/courses/')
    main_page_t = html.fromstring(main_page.content)

    class_url_list = main_page_t.xpath('//li[position()>4]/div[@class="column c1"]/a/@href')
    class_name_list = main_page_t.xpath('//li[position()>4]/div[@class="column c1"]/a/@title')

    for z in range(0, 4):
        for x in range(len(class_url_list)):
            if A_day == True:
                if A_class[z] != class_name_list[x]:
                    continue
            else:
                if B_class[z] != class_name_list[x]:
                    continue
            class_front_page = scraper.get(class_url_list[x])
            class_front_page_t = html.fromstring(class_front_page.content)

            #get to the class day pages
            class_day_pages = class_front_page_t.xpath('//li[@class="activity lesson modtype_lesson "]//div[@class="mod-indent mod-indent-2"]/..//a/@href')
            url = class_day_pages[0]
            dates_page = scraper.get(url)
            dates_page_t = html.fromstring(dates_page.content)

            #use distance from top
            """
            homework_url = dates_page_t.xpath('//ul/li[10]/a/@href')
            date = dates_page_t.xpath('//ul/li[10]/a/text()')
            url = homework_url[0]
            homework_page = scraper.get(url)
            homework_page_t = html.fromstring(homework_page.content)
            """

            #use month/day to find correct page in list
            date = dates_page_t.xpath('//ul/li[@class="notselected"]/a/text()')
            correct_month = filter(lambda m: month in m, date)
            correct_date = filter(lambda d: day in d, correct_month)

            #find url that matches correct month/day
            homework_url = dates_page_t.xpath('//ul/li[@class="notselected"]/a/@href')
            for y in range(len(date)):
                #check if correct_date is empty because of A/B day classes
                if not correct_date:
                    break
                    
                if date[y] == correct_date[0]:
                    url = homework_url[y]
                    homework_page = scraper.get(url)
                    homework_page_t = html.fromstring(homework_page.content)

                    class_name = homework_page_t.xpath('//ul[@class="breadcrumb"]/li[2]/a/@title')
                    homework = homework_page_t.xpath('//div[@class="no-overflow"]//ul[last()]/li/text()')

                    #get rid of extra unnecessary lines
                    for xline in range(len(homework)):
                        if homework[xline] == '\r\n' or homework[xline] == '\r' or homework[xline] == '\n':
                            homework[xline] = ''

                    #start printing useful information        
                    print class_name[0], ' ', month, day
                    print url
                    #print len(homework)
                    print homework
                    for assignment in homework:
                        if not assignment:
                            continue
                        print assignment 
                    print '\n'
                    break

"""
Problems with program:
Select only A or B day Classes
Some classes only have one date ex: 'Sept 12' instead of 'Sept 12/13'
AP Microeconomics sometimes uses <p></p> instead of the normal <ul></ul> http://learn.vcs.net/courses/mod/lesson/view.php?id=101899&pageid=191697
"""