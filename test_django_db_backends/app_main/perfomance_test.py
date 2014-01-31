import sys
import os
from pprint import pprint
from datetime import datetime
from io import StringIO

import pymysql
pymysql.install_as_MySQLdb()
sys.path.append(r'D:\SCRIPTS\WORK\test_django_db_backends')
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_django_db_backends.settings'

from app_main.models import Author, Book, Publisher
from django import db
from django.core.management import call_command
from django.db.models import Count, Avg, Max, Min, Variance, Sum, StdDev, Q
from django.utils.timezone import now


RECORDS_COUNT = 10000
#db_engine_name = 'mysql'


def test_bulk_create(db_engine_name):
    objs_list = []
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    for i in range(RECORDS_COUNT):
        obj = Author(name='author_'+str(i), mail='author_'+str(i)+'@djangomail.de')
        objs_list.append(obj)
    t1 = datetime.now()
    Author.objects.using(db_engine_name).bulk_create(objs_list)
    t2 = datetime.now()
    authors_bulk_create = str((t2-t1).total_seconds())
    test_result['authors_bulk_create'] = authors_bulk_create

    pprint('==========authors_bulk_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    objs_list.clear()
    authors = Author.objects.using(db_engine_name).all()
    #authors = Author.objects.using(db_engine_name).values_list('id')
    for i in range(RECORDS_COUNT):
        obj = Book(author=authors[i], title='book_'+str(i), page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
        objs_list.append(obj)
    t1 = datetime.now()
    Book.objects.using(db_engine_name).bulk_create(objs_list)
    t2 = datetime.now()
    books_bulk_create = str((t2-t1).total_seconds())
    test_result['books_bulk_create'] = books_bulk_create

    pprint('==========books_bulk_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    objs_list.clear()
    for i in range(RECORDS_COUNT):
        obj = Publisher(name='publisher_'+str(i))
        objs_list.append(obj)
    t1 = datetime.now()
    Publisher.objects.using(db_engine_name).bulk_create(objs_list)
    t2 = datetime.now()
    publisher_bulk_create = str((t2-t1).total_seconds())
    test_result['publisher_bulk_create'] = publisher_bulk_create

    pprint('==========publisher_bulk_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    for p, b in zip(Publisher.objects.using(db_engine_name).iterator(), Book.objects.using(db_engine_name).values_list('id', flat=True)):
        p.book.add(b)
    t2 = datetime.now()
    publisher_m2m_add = str((t2-t1).total_seconds())
    test_result['publisher_m2m_add'] = publisher_m2m_add

    pprint('==========publisher_m2m_add==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_filter_exclude(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = Author.objects.using(db_engine_name).filter(name__startswith='aut').exclude(mail__contains='&')
    l = len(authors)
    t2 = datetime.now()
    authors_filter_exclude = str((t2-t1).total_seconds())
    test_result['authors_filter_exclude'] = authors_filter_exclude

    pprint('==========authors_filter_exclude==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).filter(title__startswith='book').exclude(author__mail__contains='&')
    l = len(books)
    t2 = datetime.now()
    books_filter_exclude = str((t2-t1).total_seconds())
    test_result['books_filter_exclude'] = books_filter_exclude

    pprint('==========books_filter_exclude==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_order_by(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = Author.objects.using(db_engine_name).order_by('mail')
    l = len(authors)
    t2 = datetime.now()
    authors_order_by = str((t2-t1).total_seconds())
    test_result['authors_order_by'] = authors_order_by

    pprint('==========authors_order_by==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).order_by('author__name')
    l = len(books)
    t2 = datetime.now()
    books_order_by = str((t2-t1).total_seconds())
    test_result['books_order_by'] = books_order_by

    pprint('==========books_order_by==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_reverse(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = Author.objects.using(db_engine_name).reverse()
    l = len(authors)
    t2 = datetime.now()
    authors_reverse = str((t2-t1).total_seconds())
    test_result['authors_reverse'] = authors_reverse

    pprint('==========authors_reverse==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).reverse()
    l = len(books)
    t2 = datetime.now()
    books_reverse = str((t2-t1).total_seconds())
    test_result['books_reverse'] = books_reverse

    pprint('==========books_reverse==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_distinct(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = Author.objects.using(db_engine_name).distinct()
    l = len(authors)
    t2 = datetime.now()
    authors_distinct = str((t2-t1).total_seconds())
    test_result['authors_distinct'] = authors_distinct

    pprint('==========authors_distinct==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).distinct()
    l = len(books)
    t2 = datetime.now()
    books_distinct = str((t2-t1).total_seconds())
    test_result['books_distinct'] = books_distinct

    pprint('==========books_distinct==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_all(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = Author.objects.using(db_engine_name).all()
    l = len(authors)
    t2 = datetime.now()
    authors_all = str((t2-t1).total_seconds())
    test_result['authors_all'] = authors_all

    pprint('==========authors_all==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).defer('author').all()
    l = len(books)
    t2 = datetime.now()
    books_all = str((t2-t1).total_seconds())
    test_result['books_all'] = books_all

    pprint('==========books_all==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_select_related(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).select_related()
    l = len(books)
    t2 = datetime.now()
    books_select_related = str((t2-t1).total_seconds())
    test_result['books_select_related'] = books_select_related

    pprint('==========books_select_related==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_prefetch_related(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.using(db_engine_name).prefetch_related()
    l = len(books)
    t2 = datetime.now()
    books_prefetch_related = str((t2-t1).total_seconds())
    test_result['books_prefetch_related'] = books_prefetch_related

    pprint('==========books_prefetch_related==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_defer(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    b = Book.objects.using(db_engine_name).defer('author').last()
    b.author.id
    t2 = datetime.now()
    book_defer = str((t2-t1).total_seconds())
    test_result['book_defer'] = book_defer

    pprint('==========book_defer==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_only(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    b = Book.objects.using(db_engine_name).only('author').first()
    p = b.published
    t2 = datetime.now()
    book_only = str((t2-t1).total_seconds())
    test_result['book_only'] = book_only

    pprint('==========book_only==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_get(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).get(title='book_1')
    t2 = datetime.now()
    book_get = str((t2-t1).total_seconds())
    test_result['book_get'] = book_get

    pprint('==========books_get==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_create(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    author = Author.objects.using(db_engine_name).first()
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).create(author=author, title='book_manual', page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
    t2 = datetime.now()
    book_create = str((t2-t1).total_seconds())
    test_result['book_create'] = book_create

    pprint('==========book_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_in_bulk(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    books_id = Book.objects.using(db_engine_name).values_list('id', flat=True)
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).in_bulk(books_id)
    t2 = datetime.now()
    book_in_bulk = str((t2-t1).total_seconds())
    test_result['book_in_bulk'] = book_in_bulk

    pprint('==========book_in_bulk==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_first(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).first()
    t2 = datetime.now()
    book_first = str((t2-t1).total_seconds())
    test_result['book_first'] = book_first

    pprint('==========book_first==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_last(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).last()
    t2 = datetime.now()
    book_last = str((t2-t1).total_seconds())
    test_result['book_last'] = book_last

    pprint('==========book_last==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_earliest(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).earliest('wrote')
    t2 = datetime.now()
    book_earliest = str((t2-t1).total_seconds())
    test_result['book_earliest'] = book_earliest

    pprint('==========book_earliest==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_latest(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).latest('wrote')
    t2 = datetime.now()
    book_latest = str((t2-t1).total_seconds())
    test_result['book_latest'] = book_latest

    pprint('==========book_latest==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_aggregate(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).aggregate(Count('author'), Max('published'),
                                                 Min('published'), Avg('cost'), Sum('chars_count'),
                                                 Variance('cost'), StdDev('sale_cost'))
    t2 = datetime.now()
    book_aggregate = str((t2-t1).total_seconds())
    test_result['book_aggregate'] = book_aggregate

    pprint('==========book_aggregate==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_update(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).update(wrote=now().date(), published=now())
    t2 = datetime.now()
    book_update = str((t2-t1).total_seconds())
    test_result['book_update'] = book_update

    pprint('==========book_update==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_q_lookups(db_engine_name):
    test_result = {'db_engine_name': db_engine_name}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = Book.objects.filter(Q(author__name__istartswith='author') & Q(title__contains='book') & Q(page_count__gte=200) & Q(cost__range=(200.00, 400.00)), exists__isnull=False)
    print(len(books))
   #Book(author=authors[i], title='book_'+str(i), page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
    t2 = datetime.now()
    book_q_lookups = str((t2-t1).total_seconds())
    test_result['book_q_lookups'] = book_q_lookups

    pprint('==========book_q_lookups==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def clean_db():
    Author.objects.using('mysql').all().delete()
    Book.objects.using('mysql').all().delete()
    Publisher.objects.using('mysql').all().delete()
    Author.objects.using('postgres').all().delete()
    Book.objects.using('postgres').all().delete()
    Publisher.objects.using('postgres').all().delete()

    cursor = db.connection.cursor()
    sql_commands = StringIO()
    call_command('sqlsequencereset', 'app_main', database='postgres', stdout=sql_commands)
    cursor.execute(sql_commands.getvalue())


def main():
    clean_db()
    #all_testes = [test_bulk_create, test_filter_exclude, test_order_by, test_reverse, test_distinct, test_all,
    #              test_select_related, test_prefetch_related]
    all_testes = []

    for test in all_testes:
        print('='*50)
        print(test.__name__)
        #test_result = test('mysql')
        #pprint(test_result)
        test_result = test('postgres')
        pprint(test_result)


if __name__ == '__main__':
    main()
