from django.contrib import admin

from core.models import Article, Comment


# Register your models here.

class CommentAdmin(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (CommentAdmin,)
