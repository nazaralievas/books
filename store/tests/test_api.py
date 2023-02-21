from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from store.models import Book
from store.serializers import BooksSerializer


class BookApiTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Test Book 1', price=100)
        book_2 = Book.objects.create(name='Test Book 2', price=200)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([book_1, book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
