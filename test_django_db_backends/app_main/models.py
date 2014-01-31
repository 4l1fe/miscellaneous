from django.db import models


class Book(models.Model):
    author = models.ForeignKey('Author')
    title = models.CharField(max_length=100)
    page_count = models.IntegerField()
    exists = models.BooleanField()
    chars_count = models.BigIntegerField()
    digit_version = models.BinaryField()
    important_pages = models.CommaSeparatedIntegerField(max_length=1000)
    wrote = models.DateField(auto_now=True)
    published = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=65, decimal_places=2)  # 65 - максимум для MySql
    sale_cost = models.FloatField()
    image = models.ImageField(upload_to='media')
    book_addition = models.FileField(upload_to='media')

    class Meta:
        ordering = ['author']


class Author(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=254)


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    book = models.ManyToManyField('Book')