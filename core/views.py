from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from core.models import Article
from core.serializers import ArticleSerializer, TagSerializer, ContactSerializer
from core.tasks import send_feedback


class PageNumberSetPaginator(pagination.PageNumberPagination):
    page_size = 1
    page_query_param = 'page_size'  # allows the client to set the page size for each request. This means that we can control the page size through a request.
    ordering = 'time_created'


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'  # The model field that should be used for performing object lookup of individual model instances
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPaginator


class TagDetailView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = PageNumberSetPaginator
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Article.objects.filter(tags=tag)


class AsideView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('-id')[:2]
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class ContactView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_feedback.delay(name, email, message, subject)
            return Response({'success': 'Sent'})
