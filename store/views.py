from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

from .models import Book
from .serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']


def auth(request):
    return render(request, 'store/oauth.html')
