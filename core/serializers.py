from rest_framework import serializers
from taggit.models import Tag

from .models import Article
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Article
        fields = '__all__'
        lookup_field = 'slug'  # The model field that should be used for performing object lookup of individual model instances. Defaults to 'pk'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
        lookup_field = ('name',)
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()
