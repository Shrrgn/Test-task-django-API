from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#Using standart User model 

class Post(models.Model):

	title = models.CharField(max_length = 50, unique = True)
	slug = models.SlugField()
	published = models.DateTimeField(auto_now_add = True)
	content = models.TextField()
	likes = models.PositiveIntegerField(default = 0)
	dislikes = models.PositiveIntegerField(default = 0)
	author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
	reaction = models.ManyToManyField('auth.User', blank = True, related_name = 'user_reaction_for_post')

	class Meta:
		ordering = ["-published"]

	def __str__(self):
		return self.title

	def get_author(self):
		return self.author.username

	def get_absolute_url(self):
		return reverse('post_detail', kwargs = {'slug': self.slug})
	