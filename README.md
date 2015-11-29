Associados PythonBrasil
=======================

Projeto open source para o controle de associados da associação PythonBrasil

O projeto é desenvolvido por voluntários, utilizando principamente Python e Django e Twitter Bootstrap

Preparando o ambiente
---------------------

Você precisa instalar o postgresql em sua máquina.

No Ubuntu:

   $ sudo apt-get install postgresql

No Mac OS X com Homebrew:

   $ brew install postgresql

Consulte sua distribuição para saber como preparar o postgres.

Exemplo, para instalar o banco de dados em /tmp/pgdata (temporário):

   $ pg_ctl initdb -D /tmp/pgdata
   $ pc_ctl start -D /tmp/pgdata
   $ psql -d postgres
   # create user associados createdb createuser password 'assocdev';
   # create database associados owner associados;
   # \q

Você pode mudar os parâmetros de acesso ao banco de dados, modificando o arquivo:
associados/settings_local_model.py antes de realizar o setup ou editando o arquivo
associados/settings_local.py, após o setup.

Instalar
--------

    $ make setup


Rodando a aplicação localmente
------------------------------

    $ make run


Rodando os testes
-----------------

    $ make test


Como contribuir?
----------------

Reporte os bugs e compartilhe o patches baseada nas nossas [Issues](https://github.com/pythonbrasil/associados/issues>) ou simplesmente faça um fork do projeto, contribua com o que achar necessário e mande pra gente! :)



[![Build Status](https://secure.travis-ci.org/pythonbrasil/associados.png?branch=master)](http://travis-ci.org/pythonbrasil/associados)

[![Coverage Status](https://coveralls.io/repos/pythonbrasil/associados/badge.png)](https://coveralls.io/r/pythonbrasil/associados)
