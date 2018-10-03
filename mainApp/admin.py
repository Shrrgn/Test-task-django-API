from django.contrib import admin
from django.contrib.auth import get_user_model
from mainApp.models import Post

User = get_user_model()

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	ordering = ['-date_joined']
	list_display = ['username', 'date_joined', 'is_staff']

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_display = ('title', 'author')

admin.site.register(Post, PostAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)