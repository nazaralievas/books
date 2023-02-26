from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField, IntegerField

from .models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    likes_count = SerializerMethodField()
    annotated_likes = IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotated_likes')
    
    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
