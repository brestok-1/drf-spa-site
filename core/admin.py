from django.contrib import admin

from core.models import Article


# Register your models here.

@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}

