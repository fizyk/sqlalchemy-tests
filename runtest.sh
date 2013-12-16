#!/bin/bash

echo 'test psycopg2'
workon alchemy-psycopg2
python run.py psycopg2 100 > alchemy-psycopg2.log

# python3.1 only
# echo 'test pypostgresql'
# workon alchemy-pypostgresql
# python run.py pypostgresql 100 > alchemy-pypostgresql

echo 'test pg8000'
workon alchemy-pg8000
#python run.py pg8000 100 > alchemy-pg8000.log

echo 'test mysqldb'
workon alchemy-mysqldb
#python run.py mysqldb 100 > alchemy-mysqldb.log

echo 'test oursql'
workon alchemy-oursql
#python run.py oursql 100 > alchemy-oursql.log

echo 'test mysqlconnector'
workon alchemy-mysqlconnector
#python run.py mysqlconnector 100 > alchemy-mysqlconnector.log
