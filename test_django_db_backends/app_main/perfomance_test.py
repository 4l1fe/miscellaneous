import sys
import os
from pprint import pprint
from datetime import datetime
from io import StringIO

#import pymysql
#pymysql.install_as_MySQLdb()
sys.path.append(r'D:\SCRIPTS\WORK\test_django_db_backends')
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_django_db_backends.settings'

from app_main.models import Author, Book, Publisher
from django import db
from django.core.management import call_command
from django.db.models import Count, Avg, Max, Min, Variance, Sum, StdDev, Q
from django.utils.timezone import now


class GeneratePerfomanceSql:

    def __init__(self, db_engine_names=[], records_count=10000):
        self.db_engine_names = db_engine_names
        self.records_count = records_count

    def clean_db(self, db_engine_names):
        for name in db_engine_names:
            if 'SQLITE' in name:
                while Author.objects.using(name).count():
                    ids = Author.objects.using(name).values_list('id', flat=True)[:500]
                    Author.objects.using(name).filter(pk__in=ids).delete()
                    ids = Book.objects.using(name).values_list('id', flat=True)[:500]
                    Book.objects.using(name).filter(pk__in=ids).delete()
                    ids = Publisher.objects.using(name).values_list('id', flat=True)[:500]
                    Publisher.objects.using(name).filter(pk__in=ids).delete()
            Author.objects.using(name).all().delete()
            Book.objects.using(name).all().delete()
            Publisher.objects.using(name).all().delete()

        if any(['postgres' in dben.lower() for dben in db_engine_names]):
            cursor = db.connections['POSTGRES'].cursor()
            sql_commands = StringIO()
            call_command('sqlsequencereset', 'app_main', database='POSTGRES', stdout=sql_commands)
            cursor.execute(sql_commands.getvalue())

        if any(['mysql' in dben.lower() for dben in db_engine_names]):
            cursor = db.connections['MYSQL'].cursor()
            cursor.execute("""ALTER TABLE `django_db_backends_tests`.`app_main_author`AUTO_INCREMENT = 1 ;""")

    def test01_bulk_create(self, db_engine_name):
        objs_list = []
        test_result = {'db_engine_name': db_engine_name}
        file = open(db_engine_name+'_sql', 'a')
        db.reset_queries()

        for i in range(self.records_count):
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
        for i in range(self.records_count):
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
        for i in range(self.records_count):
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

    def test02_filter_exclude(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test03_order_by(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test04_reverse(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test05_distinct(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test06_all(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

        # t1 = datetime.now()
        # publishers = [p for p in Publisher.objects.using(db_engine_name).all()]
        # t2 = datetime.now()
        # publishers_all = str((t2-t1).total_seconds())
        # test_result['Publishers'] = publishers_all

        # pprint('==========publishers_all==========', file)
        # pprint(db.connections[db_engine_name].queries, file)
        file.close()

        return test_result

    def test07_select_related(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    #def test08_prefetch_related(self, db_engine_name):
    #    test_result = {'db_engine_name': db_engine_name}
    #    file = open(db_engine_name+'_sql', 'a')
    #    db.reset_queries()
    #
    #    t1 = datetime.now()
    #    publishers = [p for p in Publisher.objects.using(db_engine_name).prefetch_related('book').all()]
    #    t2 = datetime.now()
    #    publishers_prefetch_related = str((t2-t1).total_seconds())
    #    test_result['Publisher'] = publishers_prefetch_related
    #
    #    pprint('==========publishers_prefetch_related==========', file)
    #    pprint(db.connections[db_engine_name].queries, file)
    #    file.close()
    #
    #    return test_result

    def test09_defer(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test10_only(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
        file = open(db_engine_name+'_sql', 'a')
        db.reset_queries()

        t1 = datetime.now()
        books = [b for b in Book.objects.using(db_engine_name).only('author', 'title')]
        t2 = datetime.now()
        book_defer = str((t2-t1).total_seconds())
        test_result['Book'] = book_defer

        pprint('==========book_only==========', file)
        pprint(db.connections[db_engine_name].queries, file)
        db.reset_queries()

        t1 = datetime.now()
        publishers = [p for p in Publisher.objects.using(db_engine_name).only('book')]
        t2 = datetime.now()
        publishers_defer = str((t2-t1).total_seconds())
        test_result['Publisher'] = publishers_defer

        pprint('==========publishers_only==========', file)
        pprint(db.connections[db_engine_name].queries, file)
        file.close()

        return test_result

    def test11_get(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test12_create(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test13_in_bulk(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test14_first(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test15_last(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test16_earliest(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test17_latest(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    #def test18_aggregate(self, db_engine_name):
    #    test_result = {'db_engine_name': db_engine_name}
    #    file = open(db_engine_name+'_sql', 'a')
    #    db.reset_queries()
    #
    #    t1 = datetime.now()
    #    Book.objects.using(db_engine_name).aggregate(Count('author'), Max('published'),
    #                                                 Min('published'), Avg('cost'), Sum('chars_count'),
    #                                                 Variance('cost'), StdDev('sale_cost'))
    #    t2 = datetime.now()
    #    book_aggregate = str((t2-t1).total_seconds())
    #    test_result['Book'] = book_aggregate
    #
    #    pprint('==========book_aggregate==========', file)
    #    pprint(db.connections[db_engine_name].queries, file)
    #    file.close()
    #
    #    return test_result

    def test19_update(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
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

    def test20_q_lookups(self, db_engine_name):
        test_result = {'db_engine_name': db_engine_name}
        file = open(db_engine_name+'_sql', 'a')
        db.reset_queries()

        t1 = datetime.now()
        books = [b for b in Book.objects.using(db_engine_name).filter(Q(author__name__istartswith='author') & Q(title__contains='book') &
                                                Q(page_count__gte=200) & Q(cost__range=(200.00, 400.00)), exists__isnull=False)]
        t2 = datetime.now()
        book_q_lookups = str((t2-t1).total_seconds())
        test_result['Book'] = book_q_lookups

        pprint('==========book_q_lookups==========', file)
        pprint(db.connections[db_engine_name].queries, file)
        file.close()

        return test_result

    def run(self, clean=True, tests=[]):
        if clean:
            self.clean_db(self.db_engine_names)
            print('DB cleaned')

        if tests:
            all_tests = [(tn, getattr(GeneratePerfomanceSql, tn)) for tn in tests]
        else:
            all_tests = [(tn,to) for tn, to in GeneratePerfomanceSql.__dict__.items() if tn.startswith('test')]
            all_tests.sort()

        for test_name, test in all_tests:
            print('='*50)
            print(test_name)
            for name in self.db_engine_names:
                test_result = test(self, name)
                pprint(test_result)
        return


def main():
    gps = GeneratePerfomanceSql(db_engine_names=['SQLITE'])
    #gps.run(clean=False, tests=['test20_q_lookups'])
    gps.run()

if __name__ == '__main__':
    main()