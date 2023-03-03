from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.rating_process import set_rating


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='Tom', last_name='TT')
        user2 = User.objects.create(username='user2', first_name='Bill', last_name='BB')
        user3 = User.objects.create(username='user3', first_name='John', last_name='JJ')

        self.book_1 = Book.objects.create(name='Test Book 1', price=100,
                                     author_name='Author 1', owner=user1)

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=False, rate=4)
    
    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('3.50', str(self.book_1.rating))
