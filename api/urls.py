from django.urls import path
from api.views import (PostListAPIView,
						PostDetailAPIView,
						PostCreateAPIView,
						UserCreateAPIView)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token 

urlpatterns = [
	path('api/token-verify/', verify_jwt_token),
	path('api/token-refresh/', refresh_jwt_token),
	path('api/token-auth/', obtain_jwt_token),

	path('api/u/create/', UserCreateAPIView.as_view(), name = 'api_user_create'),
	path('api/posts/create/', PostCreateAPIView.as_view(), name = 'api_post_create'),
	path('api/posts/<slug>/', PostDetailAPIView.as_view(), name = 'api_post_detail'),
	path('api/posts/', PostListAPIView.as_view(), name = 'api_posts'),
]