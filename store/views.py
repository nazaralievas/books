from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django.shortcuts import render

from .models import Book
from .serializers import BooksSerializer
from .permissions import IsOwnerOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def auth(request):
    return render(request, 'store/oauth.html')
