from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as  url
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, UserBookRelationView ,auth

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView, basename='user-book-relation')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
]

urlpatterns += router.urls
