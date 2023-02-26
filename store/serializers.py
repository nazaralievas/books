from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import IntegerField, DecimalField, CharField
from django.contrib.auth.models import User

from .models import Book, UserBookRelation


class BookReadersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    # likes_count = SerializerMethodField()
    annotated_likes = IntegerField(read_only=True)
    rating = DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = CharField(source='owner.username', default='', read_only=True)
    readers = BookReadersSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'annotated_likes',
                  'rating', 'owner_name', 'readers')
    
    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
