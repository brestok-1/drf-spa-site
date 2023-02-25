from rest_framework import serializers
from taggit.models import Tag

from .models import Article, Comment
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


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': "Password fields didn't match"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    article = serializers.SlugRelatedField(slug_field="slug", queryset=Article.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "article", "username", "text", "time_created")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
