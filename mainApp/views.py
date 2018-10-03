from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login
from django.template.defaultfilters import slugify
from mainApp.models import Post
from mainApp.forms import RegistrationForm, LoginForm, PostCreateForm

User = get_user_model()

# Create your views here.

class IndexView(View):

	template_name = 'mainApp/index.html'

	def get(self, request, *args, **kwargs):
		context = {'values':'Harry'}
		return render(self.request, self.template_name, context)

class PostListView(ListView):

	model = Post
	template_name = 'mainApp/posts.html'

	def get_context_data(self, *args, **kwargs):
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		context['posts'] = Post.objects.all()
		return context

class PostDetailView(DetailView):

	model = Post
	template_name = 'mainApp/post_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		context['post'] = self.get_object()
		return context

class RegistrationView(View):

	template_name = 'mainApp/registration.html'

	def get(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST or None)
		context = {'form':form}
		return render(self.request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			user = form.save(commit = False)
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = User.objects.create(username = username,
										email = email,
										first_name = first_name,
										last_name = last_name)
			user.set_password(password)
			user.save()

			return HttpResponseRedirect('/')

		return render(self.request, self.template_name, {'form':form})

class LoginView(View):

	template_name ='mainApp/login.html'

	def get(self, request, *args, **kwargs):
		form = LoginForm()
		context = {'form':form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST or None)
		
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username = username, password = password)

			if user:
				login(self.request, user) 
				return HttpResponseRedirect('/')

		return render(self.request, self.template_name, {'form':form})


class PostCreateView(View):

	template_name = 'mainApp/add_post.html'

	def get(self, request, *args, **kwargs):
		form = PostCreateForm(request.POST or None)
		return render(self.request, self.template_name, {'form':form})

	def post(self, request, *args, **kwargs):
		form = PostCreateForm(request.POST or None)

		if form.is_valid():
			post = form.save(commit = False)
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			post = Post.objects.create(title = title,
										slug = slugify(title),
										content = content,
										author = self.request.user)
			post.save()

			return HttpResponseRedirect('/posts/')
				
		return render(self.request, self.template_name, {'form':form})

class LikeDislikeView(View):

	template_name = 'mainApp/post_detail.html'

	def get(self, request, *args, **kwargs):
		post_detail_id = self.request.GET.get('post_detail_id')
		post = Post.objects.get(id = post_detail_id)
		like = self.request.GET.get('like')
		dislike = self.request.GET.get('dislike')
		
		if like and (request.user not in post.reaction.all()):
			post.likes += 1 
			post.reaction.add(request.user)
			post.save()
		
		if dislike and (request.user not in post.reaction.all()):
			post.dislikes += 1 
			post.reaction.add(request.user)
			post.save()
		
		data = {
			'like':post.likes,
			'dislike':post.dislikes 
		}

		return JsonResponse(data)















