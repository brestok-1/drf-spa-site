from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ArticleViewSet, TagDetailView, AsideView, TagView, ContactView, RegisterView, ProfileView, \
    CommentView

app_name = 'api'

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagView.as_view()),
    path('tags/<slug:tag_slug>/', TagDetailView.as_view()),
    path('aside/', AsideView.as_view()),
    path('contacts', ContactView.as_view()),
    path('register', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<slug:article_slug>/', CommentView.as_view()),
]
