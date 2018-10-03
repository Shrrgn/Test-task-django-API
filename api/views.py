from django.shortcuts import render
from rest_framework.generics import (ListAPIView, 
									RetrieveAPIView,
									CreateAPIView)

from api.serializers import (PostListSerializer, 
							PostDetailSerializer,
							PostCreateSerializer,
							UserCreateSerializer)

from rest_framework.permissions import (AllowAny, 
										IsAuthenticated, 
										IsAdminUser, 
										IsAuthenticatedOrReadOnly)
from mainApp.models import Post


# Create your views here.

class PostListAPIView(ListAPIView):

	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]


class PostDetailAPIView(RetrieveAPIView):

	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [AllowAny]

class PostCreateAPIView(CreateAPIView):

	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer


class UserCreateAPIView(CreateAPIView):

	#queryset = User.objects.all()
	serializer_class = UserCreateSerializer
