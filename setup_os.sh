#!/bin/bash

if [[ $OSTYPE == 'linux-gnu' ]]; then
    echo 'Linux: Instalando dependencias...'
    sleep 3
    pip install -r requirements.txt
    pip install -r requirements_test.txt

elif [[ $OSTYPE == darwin* ]]; then
    echo 'OSX: Instalando dependencias...'
    sleep 3
    pip install -r requirements.txt
    pip install -r requirements_test_osx.txt
fi

FILE="./associados/settings_local.py"

if [ ! -f $FILE ]; then
   cp "./associados/settings_local_model.py" $FILE
fi
