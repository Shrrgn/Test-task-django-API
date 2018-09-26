from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.

class IndexView(View):

	template_name = 'mainApp/index.html'

	def get(self, request, *args, **kwargs):
		context = {'values':'Harry'}
		return render(self.request, self.template_name, context)