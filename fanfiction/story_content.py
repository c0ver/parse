from lxml import html
import requests

def get_category():
	choices = ['book', 'game', 'anime']
	print choices
	return raw_input()

#get top 30 stories
def download_story_links(category):
	main_page = requests.get('https://www.fanfiction.net/' + category)
	main_page_tree = html.fromstring(main_page.content)

	story_links = main_page_tree.xpath('//td[@valign="TOP"]/div/a/@href')
	story_name = main_page_tree.xpath('//td[@valign="TOP"]/div/a/text()')
	print '\n'.join(story_name)

category = get_category()
download_stories(category)