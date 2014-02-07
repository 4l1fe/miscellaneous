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


# def common_code():
#     objs_list =


def test_bulk_create(db_engine_name):
    objs_list = []
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    for i in range(RECORDS_COUNT):
        obj = Author(name='author_'+str(i), mail='author_'+str(i)+'@djangomail.de')
        objs_list.append(obj)
    t1 = datetime.now()
    Author.objects.using(db_engine_name).bulk_create(objs_list)
    t2 = datetime.now()
    authors_bulk_create = str((t2-t1).total_seconds())
    test_result['Author'] = authors_bulk_create

    pprint('==========authors_bulk_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    objs_list.clear()
    authors = [a for a in Author.objects.using(db_engine_name).iterator()]
    for i in range(RECORDS_COUNT):
        obj = Book(author=authors[i], title='book_'+str(i), page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
        objs_list.append(obj)
    t1 = datetime.now()
    Book.objects.using(db_engine_name).bulk_create(objs_list)
    t2 = datetime.now()
    books_bulk_create = str((t2-t1).total_seconds())
    test_result['Book'] = books_bulk_create

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
    test_result['Publisher'] = publisher_bulk_create

    pprint('==========publisher_bulk_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    con = db.connections[db_engine_name]
    cur = con.cursor()
    cur.execute('''insert into app_main_publisher_book (publisher_id, book_id) select p.id, b.id
                from app_main_publisher p, app_main_book b where p.id = b.id;''')
    t2 = datetime.now()
    publisher_m2m_raw = str((t2-t1).total_seconds())
    test_result['Publisher cur.execute'] = publisher_m2m_raw

    pprint('==========publisher_m2m_cur.execute==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_filter_exclude(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = [a for a in Author.objects.using(db_engine_name).filter(name__startswith='aut').exclude(mail__contains='&')]
    t2 = datetime.now()
    authors_filter_exclude = str((t2-t1).total_seconds())
    test_result['Author'] = authors_filter_exclude

    pprint('==========authors_filter_exclude==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).filter(title__startswith='book').exclude(author__mail__contains='&')]
    t2 = datetime.now()
    books_filter_exclude = str((t2-t1).total_seconds())
    test_result['Book'] = books_filter_exclude

    pprint('==========books_filter_exclude==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).filter(name__startswith='publisher').exclude(book__title__contains='&')]
    t2 = datetime.now()
    publisher_filter_exclude = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_filter_exclude

    pprint('==========publisher_filter_exclude==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_order_by(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = [a for a in Author.objects.using(db_engine_name).order_by('-mail')]
    t2 = datetime.now()
    authors_order_by = str((t2-t1).total_seconds())
    test_result['Author'] = authors_order_by

    pprint('==========authors_order_by==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).order_by('-title')]
    t2 = datetime.now()
    books_order_by = str((t2-t1).total_seconds())
    test_result['Book'] = books_order_by

    pprint('==========books_order_by==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).order_by('-name')]
    t2 = datetime.now()
    publisher_order_by = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_order_by

    pprint('==========publisher_order_by==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_reverse(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = [a for a in Author.objects.using(db_engine_name).reverse()]
    t2 = datetime.now()
    authors_reverse = str((t2-t1).total_seconds())
    test_result['Author'] = authors_reverse

    pprint('==========authors_reverse==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).reverse()]
    t2 = datetime.now()
    books_reverse = str((t2-t1).total_seconds())
    test_result['Book'] = books_reverse

    pprint('==========books_reverse==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).reverse()]
    l = len(books)
    t2 = datetime.now()
    publisher_reverse = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_reverse

    pprint('==========publisher_reverse==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_distinct(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = [a for a in Author.objects.using(db_engine_name).distinct()]
    t2 = datetime.now()
    authors_distinct = str((t2-t1).total_seconds())
    test_result['Author'] = authors_distinct

    pprint('==========authors_distinct==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).distinct()]
    t2 = datetime.now()
    books_distinct = str((t2-t1).total_seconds())
    test_result['Book'] = books_distinct

    pprint('==========books_distinct==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).distinct()]
    t2 = datetime.now()
    publisher_distinct = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_distinct

    pprint('==========publisher_distinct==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_all(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    authors = [a for a in Author.objects.using(db_engine_name).all()]
    t2 = datetime.now()
    authors_all = str((t2-t1).total_seconds())
    test_result['Author'] = authors_all

    pprint('==========authors_all==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).all()]
    t2 = datetime.now()
    books_all = str((t2-t1).total_seconds())
    test_result['Book'] = books_all

    pprint('==========books_all==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).all()]
    t2 = datetime.now()
    publishers_all = str((t2-t1).total_seconds())
    test_result['Publishers'] = publishers_all

    pprint('==========publishers_all==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_select_related(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).select_related()]
    t2 = datetime.now()
    books_select_related = str((t2-t1).total_seconds())
    test_result['Book'] = books_select_related

    pprint('==========books_select_related==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_prefetch_related(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).prefetch_related('book').all()]
    t2 = datetime.now()
    publishers_prefetch_related = str((t2-t1).total_seconds())
    test_result['Publisher'] = publishers_prefetch_related

    pprint('==========publishers_prefetch_related==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_defer(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).defer('author', 'title')]
    t2 = datetime.now()
    book_defer = str((t2-t1).total_seconds())
    test_result['Book'] = book_defer

    pprint('==========book_defer==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).defer('name', 'book')]
    t2 = datetime.now()
    publishers_defer = str((t2-t1).total_seconds())
    test_result['Publisher'] = publishers_defer

    pprint('==========publishers_defer==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_only(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.using(db_engine_name).only('author', 'title')]
    t2 = datetime.now()
    book_defer = str((t2-t1).total_seconds())
    test_result['Book'] = book_defer

    pprint('==========book_defer==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    publishers = [p for p in Publisher.objects.using(db_engine_name).only('book')]
    t2 = datetime.now()
    publishers_defer = str((t2-t1).total_seconds())
    test_result['Publisher'] = publishers_defer

    pprint('==========publishers_defer==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_get(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).get(title='book_1')
    t2 = datetime.now()
    book_get = str((t2-t1).total_seconds())
    test_result['Book'] = book_get

    pprint('==========books_get==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    Publisher.objects.using(db_engine_name).get(name='publisher_1')
    t2 = datetime.now()
    publisher_get = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_get

    pprint('==========publisher_get==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_create(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    author = Author.objects.using(db_engine_name).first()
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).create(author=author, title='book_manual', page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
    t2 = datetime.now()
    book_create = str((t2-t1).total_seconds())
    test_result['Book'] = book_create

    pprint('==========book_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    Publisher.objects.using(db_engine_name).create(name='publisher_created')
    t2 = datetime.now()
    publisher_create = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_create

    pprint('==========publisher_create==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_in_bulk(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    books_id = Book.objects.using(db_engine_name).values_list('id', flat=True)
    publishers_id = Publisher.objects.using(db_engine_name).values_list('id', flat=True)
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).in_bulk(books_id)
    t2 = datetime.now()
    book_in_bulk = str((t2-t1).total_seconds())
    test_result['Book'] = book_in_bulk

    pprint('==========book_in_bulk==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    Publisher.objects.using(db_engine_name).in_bulk(publishers_id)
    t2 = datetime.now()
    publishers_in_bulk = str((t2-t1).total_seconds())
    test_result['Publisher'] = publishers_in_bulk

    pprint('==========publishers_in_bulk==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()


    return test_result


def test_first(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).first()
    t2 = datetime.now()
    book_first = str((t2-t1).total_seconds())
    test_result['Book'] = book_first

    pprint('==========book_first==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    Publisher.objects.using(db_engine_name).first()
    t2 = datetime.now()
    publisher_first = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_first

    pprint('==========publisher_first==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_last(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).last()
    t2 = datetime.now()
    book_last = str((t2-t1).total_seconds())
    test_result['Book'] = book_last

    pprint('==========book_last==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    db.reset_queries()

    t1 = datetime.now()
    Publisher.objects.using(db_engine_name).last()
    t2 = datetime.now()
    publisher_last = str((t2-t1).total_seconds())
    test_result['Publisher'] = publisher_last

    pprint('==========publisher_last==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_earliest(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).earliest('wrote')
    t2 = datetime.now()
    book_earliest = str((t2-t1).total_seconds())
    test_result['Book'] = book_earliest

    pprint('==========book_earliest==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_latest(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).latest('wrote')
    t2 = datetime.now()
    book_latest = str((t2-t1).total_seconds())
    test_result['Book'] = book_latest

    pprint('==========book_latest==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_aggregate(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).aggregate(Count('author'), Max('published'),
                                                 Min('published'), Avg('cost'), Sum('chars_count'),
                                                 Variance('cost'), StdDev('sale_cost'))
    t2 = datetime.now()
    book_aggregate = str((t2-t1).total_seconds())
    test_result['Book'] = book_aggregate

    pprint('==========book_aggregate==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_update(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    Book.objects.using(db_engine_name).update(wrote=now().date(), published=now())
    t2 = datetime.now()
    book_update = str((t2-t1).total_seconds())
    test_result['Book'] = book_update

    pprint('==========book_update==========', file)
    pprint(db.connections[db_engine_name].queries, file)
    file.close()

    return test_result


def test_q_lookups(db_engine_name):
    test_result = {'db_engine_name': db_engine_name.upper()}
    file = open(db_engine_name+'_sql', 'a')
    db.reset_queries()

    t1 = datetime.now()
    books = [b for b in Book.objects.filter(Q(author__name__istartswith='author') & Q(title__contains='book') &
                                            Q(page_count__gte=200) & Q(cost__range=(200.00, 400.00)), exists__isnull=False)]
    t2 = datetime.now()
    book_q_lookups = str((t2-t1).total_seconds())
    test_result['Book'] = book_q_lookups

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
    all_testes = [test_bulk_create, test_filter_exclude, test_order_by, test_reverse, test_distinct, test_all,
                  test_select_related, test_prefetch_related, test_defer, test_only, test_get, test_create,
                  test_in_bulk, test_first, test_last, test_earliest, test_latest, test_aggregate, test_update,
                  test_q_lookups]
    #all_testes = [test_bulk_create]

    for test in all_testes:
        print('='*50)
        print(test.__name__)
        test_result = test('mysql')
        pprint(test_result)
        test_result = test('postgres')
        pprint(test_result)


if __name__ == '__main__':
    main()
