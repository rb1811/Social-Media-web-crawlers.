import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

f =  open('booklikes_books_urls.txt','r')
book_list = []
for line in f:
	if line:
		book_list.append(line[:-2]+'/reviews')


# book_list = ['http://booklikes.com/trigger-warning-short-fictions-and-disturbances-neil-gaiman/book,12993075/reviews','http://booklikes.com/the-shadow-of-the-wind-lucia-graves-carlos-ruiz-zafon/book,17306/reviews', 'http://booklikes.com/book/book,6253210/reviews']
booklikes_reviews, done_urls = [],{}

g = open('booklikes_reviews.json', 'r')
for line in g:
	try:
		done_urls[json.loads(line[:-2]).keys()[0]] = None
	except:
		pass

g2 = open('booklikes_reviews2.json', 'r')
for line in g2:
	try:
		done_urls[json.loads(line[:-2]).keys()[0]] = None
	except:
		pass
		
g.close()
print "The number of books to be scraped", len(book_list)
print "The number of books already done", len(done_urls.keys())

for urlStr in tqdm(book_list[50001:80000]):
	if urlStr in done_urls:
		# print "This is done : ", urlStr
		continue
	

	if len(booklikes_reviews)!=0:
		print "@@@@@@@@@@@@@@@@@@@@@@@@@"
		print "Writing in batches"
		print "@@@@@@@@@@@@@@@@@@@@@@@@@"
		f = open('booklikes_reviews2.json','a')
		for ele in booklikes_reviews:
			json.dump(ele,f)
			f.write(','+'\n')
		f.close()
		booklikes_reviews = []
	
	reviews = []	
	next_page = urlStr
	page_count  = 0
	while True:
		page_count +=1
		if page_count == 500: #This is to filter out the urls that are community reviews which are never ending reviews
			# reviews = []
			break
			
		# print "%%%%%%%%%%%%%%%%%%%%%%%%%%"
		# print "This is the next page of the same book: ", next_page
		# print "This is the len of current reviews: ", len(reviews)
		# print "%%%%%%%%%%%%%%%%%%%%%%%%%%"

		response =  requests.get(next_page)
		soup =  BeautifulSoup(response.content, 'lxml')
		# if 'Community Reviews' in str(soup.find('h1', attrs={'class':'set-clearfix'})):
			# print "Community reviews"
			# break
		for rev in soup.find('div', attrs={'class':'container content'}).find_all('div',attrs={'class':'book-page-review'}):
			full_star,half_star  = 0,0
			user_url = rev.find('div',attrs = {'class':'book-page-review-user'}).find('a')['href']
			user_name  = rev.find('div',attrs = {'class':'book-page-review-user'}).find('a').string

	 		for tag in 	rev.find_all('span'):
	 			if 'star' in str(tag):
	 				for star_img in tag.find_all('img'):
	 					if 'star_a' in star_img['src']:
	 						full_star+=1
	 					elif 'star_h' in star_img['src']:
	 						half_star+=1
	 					else:
	 						pass
	 			else:
	 				pass
	 		rating = full_star + 0.5*half_star
	 		reviews.append({"name" : user_name, "user_url":user_url, "rating": rating})

	 	if 'next' in str(soup.find('nav')): 
	 	 	for tag in soup.find('nav').find_all('a'):
	 	 		if 'next' in str(tag):
	 	 			next_page =  tag['href']
	 	else:
	 		break
	booklikes_reviews.append({urlStr :reviews})

if booklikes_reviews:
	f = open('booklikes_reviews2.json','a')
	for ele in booklikes_reviews:
		json.dump(ele,f)
		f.write(','+'\n')
	f.close()