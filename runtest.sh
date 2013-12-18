#!/bin/bash

source `which virtualenvwrapper.sh`

connectors=('psycopg2' 'pypostgresql' 'pg8000' 'mysqldb' 'oursql' 'mysqlconnector')
packages=('psycopg2' 'pypostgresql' 'pg8000' 'mysql-python' 'oursql' 'mysqlconnector')

#py2
for i in 0 #1 2 3 4 5
do

    echo 'Testing '${connectors[$i]}
    venv="alchemy-${connectors[$i]}"
    log=$venv.log
    mkvirtualenv $venv
    pip install --upgrade sqlalchemy ${packages[$i]}
    echo 'Python version: 2.7.5' > $log
    python --version
    echo '>>>>>>>>>' >> $log
    echo 'pip freeze' >> $log
    pip freeze >> $log
    echo '>>>>>>>>>' >> $log
    python run.py ${connectors[$i]} 100 >> $log
    deactivate
    echo 'Clearing after'
    rmvirtualenv $venv

done

echo 'Python 3'

#py3
for i in 0 #1 2 3 4 5
do

    echo 'Testing '${connectors[$i]}
    venv="alchemy-${connectors[$i]}-py3"
    log=$venv.log
    mkvirtualenv -p `which python3` $venv
    pip install --upgrade sqlalchemy ${packages[$i]}
    echo 'Python version: 3.3.2' > $log
    python3 --version
    echo '>>>>>>>>>' >> $log
    echo 'pip freeze' >> $log
    pip freeze >> $log
    echo '>>>>>>>>>' >> $log
    python3 run.py ${connectors[$i]} 100 >> $log
    deactivate
    echo 'Clearing after'
    rmvirtualenv $venv

done
