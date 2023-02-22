from django.shortcuts import render
from rest_framework import viewsets

from core.models import Article
from core.serializers import ArticleSerializer


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'

