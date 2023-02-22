from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ArticleViewSet

app_name = 'api'

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls))
]
