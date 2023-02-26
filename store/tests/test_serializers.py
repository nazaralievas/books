from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.serializers import BooksSerializer
from store.models import Book, UserBookRelation


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        book_1 = Book.objects.create(name='Test Book 1', price=100,
                                     author_name='Author 1')
        book_2 = Book.objects.create(name='Test Book 2', price=200,
                                     author_name='Author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False, rate=4)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
            ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test Book 1',
                'price': '100.00',
                'author_name': 'Author 1',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '5.00'
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '200.00',
                'author_name': 'Author 2',
                'likes_count': 0,
                'annotated_likes': 0,
                'rating': '4.00'
            }
        ]
        self.assertEqual(expected_data, data)
