from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.serializers import BooksSerializer
from store.models import Book, UserBookRelation


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='Tom', last_name='TT')
        user2 = User.objects.create(username='user2', first_name='Bill', last_name='BB')
        user3 = User.objects.create(username='user3', first_name='John', last_name='JJ')

        book_1 = Book.objects.create(name='Test Book 1', price=100,
                                     author_name='Author 1', owner=user1)
        book_2 = Book.objects.create(name='Test Book 2', price=200,
                                     author_name='Author 2')

        user_book_1 = UserBookRelation.objects.create(user=user1, book=book_1, like=False)
        user_book_1.rate = 5
        user_book_1.save()

        UserBookRelation.objects.create(user=user2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False, rate = 4)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
            ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test Book 1',
                'price': '100.00',
                'author_name': 'Author 1',
                'annotated_likes': 1,
                'rating': '5.00',
                'owner_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Tom',
                        'last_name': 'TT'
                    },
                    {
                        'first_name': 'Bill',
                        'last_name': 'BB'
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test Book 2',
                'price': '200.00',
                'author_name': 'Author 2',
                'annotated_likes': 0,
                'rating': '4.00',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'John',
                        'last_name': 'JJ'
                    }
                ]
            }
        ]
        print('********expect', expected_data)
        print('********data', data)
        self.assertEqual(expected_data, data)
