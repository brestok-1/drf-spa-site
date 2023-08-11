from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from taggit.models import Tag

from core.models import Article, Comment
from core.serializers import ArticleSerializer, TagSerializer, ContactSerializer, RegisterSerializer, UserSerializer, \
    CommentSerializer
from core.tasks import send_feedback


class PageNumberSetPaginator(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'  # allows the client to set the page size for each request. This means that we can control the page size through a request.
    ordering = 'time_created'


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = PageNumberSetPaginator
    lookup_field = 'slug'  # The model field that should be used for performing object lookup of individual model instances
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['content', 'h1']

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User has created successfully'
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data
        })


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        article_slug = self.kwargs['article_slug'].lower()
        article = Article.objects.get(slug=article_slug)
        return Comment.objects.filter(article=article)
