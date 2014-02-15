import sys
import os
from pprint import pprint
from datetime import datetime
from io import StringIO

# import pymysql
# pymysql.install_as_MySQLdb()
sys.path.append(r'D:\SCRIPTS\WORK\test_django_db_backends')
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_django_db_backends.settings'

from app_main.models import Author, Book, Publisher
from django import db
from django.core.management import call_command
from django.db.models import Count, Avg, Max, Min, Variance, Sum, StdDev, Q
from django.utils.timezone import now


class GeneratePerfomanceSql:

    def __init__(self, db_engine_names=[], write_sql=False, records_count=10000):
        self.db_engine_names = db_engine_names
        self.records_count = records_count
        self.write_sql = write_sql

    def clean_db(self, db_engine_names):
        """Для sqlite вываливается ошибка при массовом удалении: Too many SQL vatiables,
           поэтому записи удаляются порциями"""
        for name in db_engine_names:
            if 'SQLITE' in name:
                while Author.objects.using(name).count():
                    ids = Author.objects.using(name).values_list('id', flat=True)[:400]
                    Author.objects.using(name).filter(pk__in=ids).delete()
                    ids = Book.objects.using(name).values_list('id', flat=True)[:400]
                    Book.objects.using(name).filter(pk__in=ids).delete()
                    ids = Publisher.objects.using(name).values_list('id', flat=True)[:400]
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

        db.reset_queries()

    def common_work(self, dbe, tn, start, end):
        """end содержит списки из 2х элементов:
           0й - имя модели, от которой выполняется метод
           1й - время завершения выполнения метода"""
        test_result = {'db_engine_name': dbe}
        for s, e in zip(start, end):
            test_result[e[0]] = str((e[1]-s).total_seconds())

        if self.write_sql:
            file = open(dbe+'.sql', 'a')
            pprint('============{}==========='.format(tn), file)
            pprint(db.connections[dbe].queries, file)
            db.reset_queries()

        return test_result

    def mock(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).defer('author', 'title')]
        end.append(['books', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).defer('name', 'book')]
        end.append(['publishers', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end, )

    def test01_bulk_create(self, db_engine_name, test_name):
        objs_list, start, end = [], [], []

        for i in range(self.records_count):
            obj = Author(name='author_'+str(i), mail='author_'+str(i)+'@djangomail.de')
            objs_list.append(obj)
        start.append(datetime.now())
        Author.objects.using(db_engine_name).bulk_create(objs_list)
        end.append(['Author', datetime.now()])

        objs_list.clear()
        authors = [a for a in Author.objects.using(db_engine_name).iterator()]
        for i in range(self.records_count):
            obj = Book(author=authors[i], title='book_'+str(i), page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
            objs_list.append(obj)
        start.append(datetime.now())
        Book.objects.using(db_engine_name).bulk_create(objs_list)
        end.append(['Book', datetime.now()])

        objs_list.clear()
        for i in range(self.records_count):
            obj = Publisher(name='publisher_'+str(i))
            objs_list.append(obj)
        start.append(datetime.now())
        Publisher.objects.using(db_engine_name).bulk_create(objs_list)
        end.append(['Publisher', datetime.now()])

        con = db.connections[db_engine_name]
        cur = con.cursor()
        start.append(datetime.now())
        cur.execute('''insert into app_main_publisher_book (publisher_id, book_id) select p.id, b.id
                    from app_main_publisher p, app_main_book b where p.id = b.id;''')
        end.append(['Publisher.raw', datetime.now()])
        con.close()

        return self.common_work(db_engine_name, test_name, start, end)

    def test02_filter_exclude(self, db_engine_name, test_name):
        start, end =[], []

        start.append(datetime.now())
        authors = [a for a in Author.objects.using(db_engine_name).filter(name__startswith='aut').exclude(mail__contains='&')]
        end.append(['Author', datetime.now()])

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).filter(title__startswith='book').exclude(author__mail__contains='&')]
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).filter(name__startswith='publisher').exclude(book__title__contains='&')]
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test03_order_by(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        authors = [a for a in Author.objects.using(db_engine_name).order_by('-mail')]
        end.append(['Author', datetime.now()])

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).order_by('-title')]
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).order_by('-name')]
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test04_reverse(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        authors = [a for a in Author.objects.using(db_engine_name).reverse()]
        end.append(['Author', datetime.now()])

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).reverse()]
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).reverse()]
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test05_distinct(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        authors = [a for a in Author.objects.using(db_engine_name).distinct()]
        end.append(['Author', datetime.now()])

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).distinct()]
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).distinct()]
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test06_all(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        authors = [a for a in Author.objects.using(db_engine_name).all()]
        end.append(['Author', datetime.now()])

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).all()]
        end.append(['Book', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test07_select_related(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).select_related()]
        end.append(['Book', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test08_prefetch_related(self, db_engine_name, test_name):
        if not 'SQLITE' in db_engine_name:
            start, end = [], []

            start.append(datetime.now())
            publishers = [p for p in Publisher.objects.using(db_engine_name).prefetch_related('book').all()]
            end.append(['Publisher', datetime.now()])

            return self.common_work(db_engine_name, test_name, start, end)
        else: pass

    def test09_defer(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).defer('author', 'title')]
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).defer('name', 'book')]
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test10_only(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).only('author', 'title')]
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        publishers = [p for p in Publisher.objects.using(db_engine_name).only('book')]
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test11_get(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).get(title='book_1')
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        Publisher.objects.using(db_engine_name).get(name='publisher_1')
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test12_create(self, db_engine_name, test_name):
        start, end = [], []

        author = Author.objects.using(db_engine_name).first()
        start.append(datetime.now())
        Book.objects.using(db_engine_name).create(author=author, title='book_manual', page_count=300, exists=True, chars_count=300000, cost=347.77, sale_cost=244.07)
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        Publisher.objects.using(db_engine_name).create(name='publisher_created')
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test13_in_bulk(self, db_engine_name, test_name):
        books_id = Book.objects.using(db_engine_name).values_list('id', flat=True)
        publishers_id = Publisher.objects.using(db_engine_name).values_list('id', flat=True)
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).in_bulk(books_id)
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        Publisher.objects.using(db_engine_name).in_bulk(publishers_id)
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test14_first(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).first()
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        Publisher.objects.using(db_engine_name).first()
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test15_last(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).first()
        end.append(['Book', datetime.now()])

        start.append(datetime.now())
        Publisher.objects.using(db_engine_name).first()
        end.append(['Publisher', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test16_earliest(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).earliest('wrote')
        end.append(['Book', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test17_latest(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).latest('wrote')
        end.append(['Book', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test18_aggregate(self, db_engine_name, test_name):
        if not 'SQLITE' in db_engine_name:
            start, end = [], []

            start.append(datetime.now())
            Book.objects.using(db_engine_name).aggregate(Count('author'), Max('published'),
                                                        Min('published'), Avg('cost'), Sum('chars_count'),
                                                        Variance('cost'), StdDev('sale_cost'))
            end.append(['Book', datetime.now()])

            return self.common_work(db_engine_name, test_name, start, end)

        else: pass

    def test19_update(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        Book.objects.using(db_engine_name).update(wrote=now().date(), published=now())
        end.append(['Book', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

    def test20_q_lookups(self, db_engine_name, test_name):
        start, end = [], []

        start.append(datetime.now())
        books = [b for b in Book.objects.using(db_engine_name).filter(Q(author__name__istartswith='author') & Q(title__contains='book') &
                                                Q(page_count__gte=200) & Q(cost__range=(200.00, 400.00)), exists__isnull=False)]
        end.append(['Book', datetime.now()])

        return self.common_work(db_engine_name, test_name, start, end)

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
            for den in self.db_engine_names:
                test_result = test(self, den, test_name)
                pprint(test_result)
        return


def main():
    """Пример параметров создания экземпляра и его запуска:
       gps = GeneratePerfomanceSql(db_engine_names=['MYSQL', 'POSTGRES'], records_count=9000, write_sql=True)
       gps.run(clean=True, tests=['test01_bulk_create', 'test15_last'])"""
    gps = GeneratePerfomanceSql(db_engine_names=['SQLITE'])
    gps.run()

if __name__ == '__main__':
    main()