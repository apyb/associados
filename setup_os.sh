#!/bin/bash

if [[ $OSTYPE == 'linux-gnu' ]]; then
    echo 'Linux: Instalando dependencias...'
    sleep 3
    [ $(which apt-get) ] && sudo apt-get install -y libpq-dev python-lxml libxml2-dev libxslt1-dev
    pip install -r requirements_test.txt

elif [[ $OSTYPE == darwin* ]]; then
    echo 'OSX: Instalando dependencias...'
    sleep 3
    pip install -r requirements_test_osx.txt
fi

FILE="./associados/settings_local.py"

if [ ! -f $FILE ]; then
   cp "./associados/settings_local_model.py" $FILE
fi
