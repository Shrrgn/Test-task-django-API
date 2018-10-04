from rest_framework import serializers
from django.template.defaultfilters import slugify
from mainApp.models import Post
from mainApp.utils import checking_password
from django.contrib.auth import get_user_model

User = get_user_model()

class PostListSerializer(serializers.ModelSerializer):

	url = serializers.HyperlinkedIdentityField(
			view_name = 'api_post_detail',
			lookup_field = 'slug'
	)
	
	class Meta:

		model = Post
		fields = [
			'title',
			'url',
			'published',
		]


class PostDetailSerializer(serializers.ModelSerializer):

	author = serializers.SerializerMethodField()

	class Meta:

		model = Post
		fields = [
			'title',
			'slug',
			'published',
			'likes',
			'dislikes',
			'author',
			'content',
		]

	def get_author(self, obj):
		return str(obj.author.username)

class PostCreateSerializer(serializers.ModelSerializer):

	user = serializers.HiddenField(default = serializers.CurrentUserDefault())

	class Meta:

		model = Post
		fields = [
			'title',
			'content',
			'user',
		]

	def create(self, validated_data):
		post = Post.objects.create(title = validated_data['title'],
									slug = slugify(validated_data['title']),
									content = validated_data['content'],
									author = validated_data['user'])
		post.save()

		return validated_data


class UserCreateSerializer(serializers.ModelSerializer):

	username = serializers.CharField(max_length = 30,
									help_text = 'Required. 6-30 characters or fewer. Letters, digits and @/./+/-/_ only.')
	password = serializers.CharField(max_length = 30,
									help_text = 'Required. 8-30 characters. Must consist one or bigger capital letters, \
											one or bigger digits and @/./+/-/_ only')

	class Meta:

		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'password',
		]
		extra_kwargs = {'password':{'write_only': True}}

	def create(self, validated_data):
		user = User.objects.create(username = validated_data['username'],
									first_name = validated_data['first_name'],
									last_name = validated_data['last_name'],
									email = validated_data['email'])
		user.set_password(validated_data['password'])
		user.save()

		return validated_data


	def validate(self, data):
		username = data['username']
		if User.objects.filter(username = username).exists():
			raise serializers.ValidationError('This user already exists!')

		if len(username) < 6 or len(username) > 30:
			raise serializers.ValidationError('Username should be 6-30 characters or fewer. Letters, digits and @/./+/-/_ only')

		if User.objects.filter(email = data['email']).exists():
			raise serializers.ValidationError('User with this email already exists!')

		if not checking_password(data['password']):
			raise serializers.ValidationError('Password should be 8-30 characters and consist one or \
											bigger capital letters, \
											one or bigger digits and @/./+/-/_ only')

		return data
			