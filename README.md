Associados PythonBrasil
=======================

Projeto open source para o controle de associados da associação PythonBrasil

O projeto é desenvolvido por voluntários, utilizando principamente Python e Django e Twitter Bootstrap

Preparando o ambiente
---------------------

Recomenda-se utilizar o [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) para manter o ambiente isolado de suas aplicações. Testado com Python 3.5.2, Postgresql 9.5.4 e Django 1.10.1.


Você precisa instalar o postgresql em sua máquina antes de continuar.

No Ubuntu:

    $ sudo apt-get install postgresql

No Mac OS X com Homebrew:

    $ brew install postgresql

Consulte sua distribuição para saber como preparar o postgres.

Exemplo, para instalar o banco de dados em /tmp/pgdata (temporário):

    $ sudo apt-get install python-psycopg2
    $ pg_ctl initdb -D /tmp/pgdata
    $ pg_ctl start -D /tmp/pgdata
    $ su postgres psql -U postgres # para roots: psql -d postgres 
    postgres=# create user associados createdb createuser password 'assocdev';
    postgres=# create database associados owner associados;
    postgres=# \q

Você pode mudar os parâmetros locais, como banco de dados, copiando o arquivo:
`associados/example_settings.ini` para `associados/settings.ini` e editando o arquivo
com suas preferências. Os settings primeiro verificam variáveis de ambiente e
depois as definições do `settings.ini`.

Ou seja, se você definir `$ export DEBUG=True`, o valor do DEBUG em settings.ini não
será avaliado.

Instalar
--------

    $ make setup


Rodando a aplicação localmente
------------------------------

    $ make run


Rodando os testes
-----------------

    $ make test


Ambiente com Docker
---------------------------

Caso queira subir o ambiente com Docker, temos um `docker-compose.yml` com o PostgreSQL e o Django. No arquivo, também é possível alterar as informações de acesso do PostgreSQL.

Instalar o [Docker/Docker-Compose](https://docs.docker.com/engine/installation/).

Copiar o arquivo `associados/example_settings.ini` para `associados/settings.ini` e configurar as variáveis locais.

Subir o ambiente com o comando `docker-compose.yml`.

Caso queria realizar os testes, usar o comando `docker-compose run web python manage.py test --settings associados.settings.test --verbosity=2`.


Como contribuir?
----------------

Reporte os bugs e compartilhe o patches baseada nas nossas [Issues](https://github.com/pythonbrasil/associados/issues>) ou simplesmente faça um fork do projeto, contribua com o que achar necessário e mande pra gente! :)



[![Build Status](https://secure.travis-ci.org/pythonbrasil/associados.png?branch=master)](http://travis-ci.org/pythonbrasil/associados)

[![Coverage Status](https://coveralls.io/repos/pythonbrasil/associados/badge.png)](https://coveralls.io/r/pythonbrasil/associados)

[![Code Climate](https://codeclimate.com/github/pythonbrasil/associados/badges/gpa.svg)](https://codeclimate.com/github/pythonbrasil/associados)

[![Issue Count](https://codeclimate.com/github/pythonbrasil/associados/badges/issue_count.svg)](https://codeclimate.com/github/pythonbrasil/associados)
