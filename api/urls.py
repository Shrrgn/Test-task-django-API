from django.urls import path
from api.views import (PostListAPIView,
						PostDetailAPIView,
						PostCreateAPIView,
						UserCreateAPIView)

urlpatterns = [
	path('api/u/add', UserCreateAPIView.as_view(), name = 'api_user_add'),
	path('api/posts/add/', PostCreateAPIView.as_view(), name = 'api_post_add'),
	path('api/posts/<slug>/', PostDetailAPIView.as_view(), name = 'api_post_detail'),
	path('api/posts/', PostListAPIView.as_view(), name = 'api_posts'),
]