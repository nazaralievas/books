from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Book, UserBookRelation
from .serializers import BooksSerializer, UserBookRelationSerializer
from .permissions import IsOwnerOrStaffOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj


def auth(request):
    return render(request, 'store/oauth.html')
