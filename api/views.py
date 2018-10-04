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

from rest_framework import permissions

# Create your views here.

#class UserIsAuth(permissions.BasePermission):
#    def has_permission(self, request, view):
#        return request.user.is_authenticated() # request.user.is_authenticated

class PostListAPIView(ListAPIView):

	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]


class PostDetailAPIView(RetrieveAPIView):

	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsAuthenticated]

class PostCreateAPIView(CreateAPIView):

	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer
	permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):

	#queryset = User.objects.all()
	serializer_class = UserCreateSerializer
	permission_classes = [IsAuthenticated]
