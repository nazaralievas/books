from django.db.models import Avg

from .models import UserBookRelation


def set_rating(book):
    rating = UserBookRelation.objects.filter(book=book).aggregate(rating_of_book=Avg('rate')).get('rating_of_book')
    book.rating = rating
    book.save()