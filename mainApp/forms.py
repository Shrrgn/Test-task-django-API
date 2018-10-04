from django import forms
from django.contrib.auth import get_user_model
from mainApp.models import Post
from mainApp.utils import checking_password
from pyhunter import PyHunter

User = get_user_model()
hunter = PyHunter('4be2d3f192d024c353cb0bf14356cd6de53b0a02')

class RegistrationForm(forms.ModelForm):

	password = forms.CharField(widget = forms.PasswordInput, required = True)
	repeat_password = forms.CharField(widget = forms.PasswordInput, required = True)

	class Meta:

		model = User
		fields = [
			'first_name',
			'last_name',
			'username',
			'email',
			'password',
			'repeat_password',
		]

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = 'Required. 6-30 characters or fewer. Letters, digits and @/./+/-/_ only.'
		self.fields['password'].help_text = 'Required. 8-30 characters. Must consist one or bigger capital letters, \
											one or bigger digits and @/./+/-/_ only'
		self.fields['email'].required = True

	def clean(self):
		password = self.cleaned_data['password']
		repeat_password = self.cleaned_data['repeat_password']

		if password != repeat_password:
			raise forms.ValidationError('Passwords do not equal!')

		if not checking_password(password):
			raise forms.ValidationError('Password must consist one or bigger capital letters, \
											one or bigger digits and @/./+/-/_ only')

	def clean_username(self):
		username = self.cleaned_data['username']

		if User.objects.filter(username = username).exists():
			raise forms.ValidationError('User with that username already exists!')

		if len(username) < 6 or len(username) > 30:
			raise forms.ValidationError('Username length should be 6-30 charaters!')

		return username

	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email = email):
			raise forms.ValidationError('User with that email already exists!')

		#It works really bad so using that API is risky
		verify = hunter.email_verifier(email)
		if verify['result'] == 'invalid':
			raise forms.ValidationError('This email does not exist!')

		return email


class LoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		if not User.objects.filter(username = username).exists():
			raise forms.ValidationError('User with that username doesnt exist')

		user = User.objects.get(username = username)
		
		if not user.check_password(password):
			raise forms.ValidationError('Password is not right')

class PostCreateForm(forms.ModelForm):

	content = forms.CharField(widget = forms.Textarea, required = True, initial = 'Your text...')

	class Meta:

		model = Post
		fields = ['title', 'content']