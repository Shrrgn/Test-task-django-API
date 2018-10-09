import random
import requests
from datetime import datetime
from lxml import html
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.db.models import Max
from mainApp.models import Post


User = get_user_model()

NUMBER_OF_USERS = 3
MAX_POSTS_PER_USER = 2
MAX_LIKES_PER_USER = 3

LOGINS_FILE = "D:\\ZProgramming\\Python\\dj\\testingAPI\\static\\logins.txt"
URL = "https://www.livejournal.com/media/razvlecheniya/?page=1"
#url2 = "https://www.livejournal.com/media/nauka/?page=1"


class Bot:

	def __init__(self, number_of_users = NUMBER_OF_USERS, 
						max_posts_per_user = MAX_POSTS_PER_USER, 
						max_likes_per_user = MAX_LIKES_PER_USER):
		
		self.number_of_users = number_of_users 
		self.max_posts_per_user = max_posts_per_user
		self.max_likes_per_user = max_likes_per_user
		self.url = URL

	def __str__(self):
		return f"Bot create {self.number_of_users} users, max posts per user {self.max_posts_per_user} \
							max likes per user for posts {self.max_likes_per_user}"


	def get_usernames(self, file):
		usernames = []
		
		try:
			f = open(file, 'r')
			data = f.readlines()
		
			while len(usernames) != self.number_of_users: 
				user = data[random.randint(0, len(data))][:-1]
		
				if not User.objects.filter(username = user).exists():
					usernames.append(user)
				else:
					continue
		
		except (NameError, EOFError, OSError) as e:
			print(e)
		
		finally:
			f.close()

		return usernames

	def get_html(self, url):
		response = None
		try:
			response = requests.get(url)
		except requests.exceptions.MissingSchema as e:
			print(e)

		return html.fromstring(response.text)

	def get_posts_links(self):
		url = self.url
		posts_data = {}

		while len(posts_data) != self.max_posts_per_user:
			links = self.get_html(url).xpath("//h3/a/@href")

			for i in self.get_html(url).xpath("//h3/a"):
				if i.items()[0][1]: #doesn't work on server shell
					data = self.get_html(i.items()[0][1]).xpath("//title/text() | //div[starts-with(@class, 'mdspost-text-cont')]/div")
					#if everything is ok
					if not Post.objects.filter(title = data[0]).exists():
						posts_data[data[0]] = data[1].text_content()
					if len(posts_data) == self.max_posts_per_user:
						return posts_data
				else:
					continue
			else:
				position = url.find('=') + 1
				url = url.replace(url[position:], str(int(url[position:]) + 1))

	def get_posts_data(self):
		posts = {}
		for i in self.get_posts_links():
			html = self.get_html(i)
			posts[html.title.string] = html.find(attrs = {'class':'mdspost-text'}).get_text()

		return posts


	def creation(self):
		users = self.get_usernames(LOGINS_FILE)
		for i in users:
			u = User.objects.create(username = i, email = f"{i}@i.ua")
			u.set_password(f"{i}777+")
			u.save()
			self.make_likes(u)
			u.save()

		'''
		for i in users:
			for title,text in self.get_posts_data().items():
				p = Post.objects.create(title = title,
										slug = slugify(title),
										content = text,
										author = User.objects.get(username = i))
				p.save()
		'''
		print('Done!')

	def make_likes(self, user):
		max_post_id = Post.objects.all().aggregate(Max('id'))
		counter = 0
		while counter != self.max_likes_per_user:
			try:
				post = Post.objects.get(id = random.randint(0, max_post_id['id__max']))
			except Post.DoesNotExist as e:
				continue
			else:
				if user not in post.reaction.all():
					print(post)
					post.likes += 1
					post.reaction.add(user)
					post.save()
					counter += 1


	def main(self):
		start = datetime.now()
		self.creation()
		print(f"Time:{datetime.now() - start}")
