# -*- coding: utf-8 -*
'''
Created on 12-08-2012

@author: fizyk
'''
import sys
import timeit
import types

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# 238 characters length
title = u'Here, the Object Relational Mapper is introduced and fully described. If you want to work with higher-level SQL which is constructed automatically for you, as well as automated persistence of Python objects, proceed first to the tutorial.{0}'
# 1912 characters length
text = u'''
The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with database tables, and instances of those classes (objects) with rows in their corresponding tables. It includes a system that transparently synchronizes all changes in state between objects and their related rows, called a unit of work, as well as a system for expressing database queries in terms of the user defined classes and their defined relationships between each other.

The ORM is in contrast to the SQLAlchemy Expression Language, upon which the ORM is constructed. Whereas the SQL Expression Language, introduced in SQL Expression Language Tutorial, presents a system of representing the primitive constructs of the relational database directly without opinion, the ORM presents a high level and abstracted pattern of usage, which itself is an example of applied usage of the Expression Language.

While there is overlap among the usage patterns of the ORM and the Expression Language, the similarities are more superficial than they may at first appear. One approaches the structure and content of data from the perspective of a user-defined domain model which is transparently persisted and refreshed from its underlying storage model. The other approaches it from the perspective of literal schema and SQL expression representations which are explicitly composed into messages consumed individually by the database.

A successful application may be constructed using the Object Relational Mapper exclusively. In advanced situations, an application constructed with the ORM may make occasional usage of the Expression Language directly in certain areas where specific database interactions are required.

The following tutorial is in doctest format, meaning each >>> line represents something you can type at a Python command prompt, and the following text represents the expected return value.{0}
'''


class Test(Base):

    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    text = Column(UnicodeText, nullable=False)


dialect = str(sys.argv[1])

if dialect in ['psycopg2', 'pypostgresql', 'pg8000']:
    connection_string = 'postgresql+{0}://'
elif dialect in ['mysqldb', 'oursql', 'mysqlconnector']:
    connection_string = 'mysql+{0}://'


engine = create_engine(connection_string.format(dialect))

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def _create_test_objects(counter):
    tests = []
    for i in xrange(counter):
        tests.append(Test(title=title.format(i),
                     text=text.format(i)))
    return tests


def _read_ids(session, limit):
    ids = session.query(Test.id).offset(0).limit(limit).all()

    return [id[0] for id in ids]


def sqltest_add_rollback(session, tests):
    'Insert rollback test'
    session.add_all(tests)
    session.flush()
    session.rollback()

sqltest_add_rollback.__arg__ = 'list'


def sqltest_add_commit(session, tests):
    'Insert commit test'
    session.add_all(tests)
    session.flush()
    session.commit()

sqltest_add_commit.__arg__ = 'list'


def sqltest_select(session, number):
    'Select test'
    elements = session.query(Test)[:number]

sqltest_select.__arg__ = 'int'


def sqltest_delete_rollback(session, ids):
    'Delete test rollback'
    session.query(Test).filter(Test.id.in_(ids)).delete(synchronize_session=False)
    session.rollback()

sqltest_delete_rollback.__arg__ = 'del'


def sqltest_delete_commit(session, ids):
    'Delete test commit'
    session.query(Test).filter(Test.id.in_(ids)).delete(synchronize_session=False)
    session.commit()

sqltest_delete_commit.__arg__ = 'del'


if __name__ == '__main__':
    test_repeat = int(sys.argv[2])
    counters = [1, 10, 100]

    # module = sys.modules[__name__]
#    alchemy_tests = [module.__dict__.get(test) for test in dir(module)
#                     if isinstance(module.__dict__.get(test), types.FunctionType)
#                        and test.startswith('sqltest_')]

    # alchemy_tests = []
    # for test in dir(module):
    #     if isinstance(module.__dict__.get(test), types.FunctionType) \
    #             and test.startswith('sqltest_'):
    #         alchemy_tests.append(module.__dict__.get(test))

    alchemy_tests = [
        sqltest_add_rollback,
        sqltest_add_commit,
        sqltest_select,
        sqltest_delete_rollback,
        sqltest_delete_commit
    ]

    print '=' * 20
    print '{dialect} dialect test'.format(dialect=dialect)

    for alchemy_test in alchemy_tests:
        print '-' * 20
        print alchemy_test.__doc__

        for c in counters:
            print 'Objects: {0} ({1} tests)'.format(c, test_repeat)
            t_avg = 0
            t_max = 0
            t_min = 0
            for i in xrange(test_repeat):
                if alchemy_test.__arg__ == 'list':
                    tests = _create_test_objects(c)
                elif alchemy_test.__arg__ == 'del':
                    tests = _read_ids(session, c)
                else:
                    tests = c

                timer = timeit.Timer(lambda: alchemy_test(session, tests))
                try:
                    current = timer.timeit(number=1)
                    if not t_min or t_min > current:
                        t_min = current
                    if t_max < current:
                        t_max = current
                    t_avg += current
                except:
                    timer.print_exc()
                    raise

            print "{0:.3f} s/run. t_min: {1:.3f}, t_max: {2:.3f}, object_average: {3:.3f}".format((t_avg / test_repeat), t_min, t_max, (t_avg / (test_repeat * c)))
