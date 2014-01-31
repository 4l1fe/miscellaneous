from django.test import TestCase
from app_main.models import Book, Author, Publisher


class QuerySetTests(TestCase):

    def setUp(self):
        for i in range(200000):
            Author.objects.create(name='author_'+str(i), mail='author_'+str(i)+'@mail.de')
        for i in range(200000):
            author = Author.objects.get(name='author_'+str(i))
            Book.objects.create(author=author, title='book_'+str(i), page_count=300, exists=True, chars_count=3000000, cost=344.77, sale_cost=240.06)
            Publisher.objects.create(name='publish_'+str(i))

    def test_get(self):
        a1 = Author.objects.get(name='author_1')
        b1 = Book.objects.get(title='book_1')
        p1 = Publisher.objects.get(name='publish_1')
        self.assertEqual(a1.name, 'author_1')
        self.assertEqual(b1.name, 'book_1')
        self.assertEqual(p1.name, 'publish_1')