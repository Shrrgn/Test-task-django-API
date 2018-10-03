from django.urls import path, include
from mainApp.views import (IndexView, 
							PostListView, 
							PostDetailView,
							RegistrationView,
							LoginView,
							PostCreateView,
							LikeDislikeView)
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [

	path('', include('api.urls')),

	path('like_dislike/', LikeDislikeView.as_view(), name = 'like_dislike'),
	path('posts/add/', PostCreateView.as_view(), name = 'add_post'),
	path('logout/', LogoutView.as_view(next_page = reverse_lazy('index')), name = 'logout_action'),
	path('login/', LoginView.as_view(), name = 'login_action'),
	path('registration/', RegistrationView.as_view(), name = 'registration'),
	path('posts/<slug>/', PostDetailView.as_view(), name = 'post_detail'),
	path('posts/', PostListView.as_view(), name = 'posts'),
    path('', IndexView.as_view(), name = 'index'),
]