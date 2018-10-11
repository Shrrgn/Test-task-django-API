import random
import requests
from datetime import datetime
from lxml import html
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.db.models import Max
from mainApp.models import Post
from testingAPI.settings import BOT_INFO

User = get_user_model()

LOGINS_FILE = "D:\\ZProgramming\\Python\\dj\\testingAPI\\static\\logins.txt"
URL = "https://www.livejournal.com/media/razvlecheniya/?page=1"
#url2 = "https://www.livejournal.com/media/nauka/?page=1"


class Bot:
	'''Automated bot for making users, posts and give likes'''

	def __init__(self, number_of_users = BOT_INFO['NUMBER_OF_USERS'], 
						max_posts_per_user = BOT_INFO['MAX_POSTS_PER_USER'], 
						max_likes_per_user = BOT_INFO['MAX_LIKES_PER_USER']):
		
		self.number_of_users = number_of_users 
		self.max_posts_per_user = max_posts_per_user
		self.max_likes_per_user = max_likes_per_user
		self.url = URL

	def __str__(self):
		return f"Bot creates {self.number_of_users} users, {self.max_posts_per_user} posts per user {self.max_posts_per_user} likes per user for posts"


	def get_usernames(self, file):
		usernames = []
		
		try:
			f = open(file, 'r')
			data = f.readlines()
		
			while len(usernames) != self.number_of_users: 
				user = data[random.randint(0, len(data))][:-1]
		
				if not User.objects.filter(username = user).exists():
					usernames.append(user)
		
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

	def get_posts_data(self):
		url = self.url
		posts_data = {}

		while len(posts_data) != self.max_posts_per_user:
			links = self.get_html(url).xpath("//h3/a/@href")

			for i in self.get_html(url).xpath("//h3/a"):
				if i.items()[0][1]: 
					data = self.get_html(i.items()[0][1]).xpath("//title/text() | //div[starts-with(@class, 'mdspost-text-cont')]/div")
					
					if not Post.objects.filter(title = data[0]).exists():
						posts_data[str(data[0])] = data[1].text_content()
					
					if len(posts_data) == self.max_posts_per_user:
						return posts_data
			else:
				position = url.find('=') + 1
				url = url.replace(url[position:], str(int(url[position:]) + 1))

	def make_posts(self, user):
		for title,text in self.get_posts_data().items():
			p = Post.objects.create(
					title = title,
					content = text,
					author = User.objects.get(username = user)
			)
			p.slug = f"unreadable-title-{p.id}"
			print(f"{p}")
			p.save()

	def make_likes(self, user):
		max_post_id = Post.objects.all().aggregate(Max('id'))
		counter = 0
		
		while counter != self.max_likes_per_user:
			try:
				post = Post.objects.get(id = random.randint(0, max_post_id['id__max']))
			
			except Post.DoesNotExist as e:
				pass
			
			else:
				if user not in post.reaction.all():
					print(f"{post} liked")
					post.likes += 1
					post.reaction.add(user)
					post.save()
					counter += 1


	def creation(self):
		users = self.get_usernames(LOGINS_FILE)
		
		for i in users:
			user = User.objects.create(username = i, email = f"{i}@i.ua")
			user.set_password(f"{i}777+")
			user.save()
			print(user)
			
			self.make_posts(user)
			self.make_likes(user)
			
			user.save()

		print('Done!')

	def main(self):
		start = datetime.now()
		self.creation()
		print(f"Time:{datetime.now() - start}")
