#!/bin/bash

if [[ $OSTYPE == 'linux-gnu' ]]; then
    echo 'Linux: Instalando dependencias...'
    [ $(which apt-get) ] && sudo apt-get install -y libpq-dev python-lxml libxml2-dev libxslt1-dev
    pip install -r requirements_test.txt

elif [[ $OSTYPE == darwin* ]]; then
    echo 'macOS: Instalando dependencias...'
    pip install -r requirements_test.txt
fi

FILE="settings.ini"
if [ ! -f $FILE ]; then
   cp "example_settings.ini" $FILE
fi
