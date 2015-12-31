Arquitetura do Projeto
======================

O projeto foi construído em cima das ferramentas `Python <https://www.python.org>`_, `Django <http://www.djangoproject.com>`_ e `PostgreSQL <http://postgresql.org>`_. Além disso, foram usadas algumas bibliotecas para auxiliar no desenvolvimento do projeto, que são descritas abaixo.

Bibliotecas usadas
------------------

Aqui descrevemos uma visão geral de cada biblioteca usado no projeto, e que estão listados com suas versões no arquivo `requirements.txt`.

Django Extensions
*****************

Foi idealizado para armazenar uma coleção de extensões customizadas, que inclui comandos de gerenciamento por meio do manage.py, campos de models adicionais, extensões para o django-admin e muito mais.

Link do Projeto: `https://github.com/django-extensions/django-extensions <https://github.com/django-extensions/django-extensions>`_

Sorl Thumbnail
**************

Ele é usado para fazer tratamentos de imagens, em projetos Django. Ele é comumente usado para thumbnails, e pode usar como suporte o `Pillow <http://pillow.readthedocs.org/en/latest/>`_, `ImageMagick <http://www.imagemagick.org/script/index.php>`_, `PIL <http://www.pythonware.com/products/pil/>`_, `Wand <http://docs.wand-py.org/>`_ e `pgmagick <http://pgmagick.readthedocs.org/en/latest/>`_. Traz varias funcionalidades como:

 - Suporte a partir do Django 1.4 em diante;
 - Suporte ao Python 3;
 - Suporte ao uso de banco de cache no modelo chave-valor como Redis;
 - Integração do admin do Django;
 - Geração de placeholder;
 - Dentre vários.

Link do Projeto: `https://github.com/mariocesar/sorl-thumbnail <https://github.com/mariocesar/sorl-thumbnail>`_

Django Gravatar
***************

Traz funções e template tags auxiliares para trazer suporte do Gravatar ao projeto Django.

Link do Projeto: `https://github.com/twaddington/django-gravatar <https://github.com/twaddington/django-gravatar>`_

Django Pipeline
***************

Oferece o mecanismo de concatenação e compressão de arquivos estáticos como Javascript e CSS.

Link do Projeto: `https://github.com/cyberdelia/django-pipeline <https://github.com/cyberdelia/django-pipeline>`_

Django Bootstrap Toolkit
************************

Ele foi idealizado para tornar mais simples a integração do `Twitter Bootstrap <https://getbootstrap.com>`_ ao projeto Django, oferecendo template tags para renderizar formulário, além de outras funcionalidades.

Link do Projeto: `https://github.com/dyve/django-bootstrap-toolkit <https://github.com/dyve/django-bootstrap-toolkit>`_
Fork do Projeto: `https://github.com/pythonbrasil/django-bootstrap-toolkit <https://github.com/pythonbrasil/django-bootstrap-toolkit>`_

DJ Database Url
***************

É um pequeno utilitário para usar as boas práticas definidas no `12factor <http://www.12factor.net/backing-services>`_, inspirado na variável de ambiente `DATABASE_URL`, para configurar a conexão com o banco de dados em projetos Django.

Link do Projeto: `https://github.com/kennethreitz/dj-database-url <https://github.com/kennethreitz/dj-database-url>`_

Gunicorn
********

Ele é um servidor que implementa o padrão WSGI, para ambientes Unix.

Link do Projeto: `http://gunicorn.org/ <http://gunicorn.org/>`_

Django Storages
***************

Uma aplicação Django, criado para auxiliar no procedimento de coleta de arquivos estáticos por meio do `collectstatic <https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/>`_ do Django. O que ele faz é dar a opção de escolhar o storage que esses arquivos vão ser reunidos, que normalmente é armazenado na Amazon S3, que nesse projeto usa juntamente com a Heroku.

Link do Projeto: `https://github.com/jschneier/django-storages <https://github.com/jschneier/django-storages>`_

Six
***

Biblioteca que auxilia na compatibilização de projetos que precisam rodar nas versões Python 2.x e 3.x.

Link do Projeto: `https://pypi.python.org/pypi/six <https://pypi.python.org/pypi/six>`_


Estrutura do Projeto
====================

Abaixo mostra a organização do projeto, na questão do seu código-fonte:

.. code-block:: bash

    ├── app
    ├── associados
    ├── cover.sh
    ├── doc
    ├── docker-compose.yml
    ├── Dockerfile
    ├── lista_associados.py
    ├── locale
    ├── Makefile
    ├── manage.py
    ├── Procfile
    ├── README.md
    ├── requirements_test_osx.txt
    ├── requirements_test.txt
    ├── requirements.txt
    ├── setup.sh

Agora vamos explicar cada parte dessa estrutura.

Raiz do Projeto
---------------

Vamos descrever os arquivos na raiz do projeto:

 - **cover.sh**: Script shell que automatiza a geração de relatório de cobertura de testes do projeto.
 - **docker-compose.yml**: Arquivo que configura e orquestra as imagens dos containers docker do projeto. Veja mais na documentação do `docker-compose <http://docs.docker.com/compose/>`_.
 - **Dockerfile**: Configura a imagem que vai rodar o projeto.
 - **Makefile**: Automatiza tarefas comuns no projeto.
 - **manage.py**: Arquivo de gerenciamento do projeto Django.
 - **Procfile**: Configuração para o deploy do projeto na Heroku.
 - **README.md**: Informações gerais do projeto.
 - **requirements_test_osx.txt**: Lista de bibliotecas necessárias para rodar os testes do projeto no OSX.
 - **requirements-text.txt**: Lista de bibliotecas necessárias para rodar os testes do projeto.
 - **requirements.txt**: Lista de bibliotecas que são essenciais para o funcionamento do projeto.
 - **setup.sh**: Script shell que automatiza a configuração do ambiente local do projeto.


Pasta app
---------

É aqui que as aplicações do projeto estarão armazenadas, com isso cada nova funcionalidade que seja criada e que precise de uma nova app, deve ser armazenada aqui. Segue sua estrutura interna:

.. code-block:: bash

    app
    ├── authemail
    ├── core
    ├── __init__.py
    ├── members
    └── payment

O que é cada funcionalidade está sendo explicada na seção :doc:`funcionalidades`.

Pasta associados
----------------

Nessa pasta fica armazenada as configurações do projeto, de como será implantado por meio do WSGI, como também os templates base. Segue sua estrutura:

.. code-block:: bash

    associados
    ├── __init__.py
    ├── settings_local_model.py
    ├── settings.py
    ├── settings_test.py
    ├── static
    │   ├── css
    │   ├── ico
    │   ├── img
    │   ├── js
    │   ├── less
    │   ├── LICENSE
    │   ├── Makefile
    │   └── package.json
    ├── templates
    │   ├── 404.html
    │   ├── 500.html
    │   ├── base.html
    │   ├── flatpages
    │   ├── pagination.html
    │   └── registration
    ├── urls.py
    ├── wsgi.py

Vamos descrever os principais arquivos e pastas:

 - **settings.py**: Arquivo que possui as configurações base do projeto.
 - **settings_local_model.py**: Arquivo de modelo, para sobrescrever configurações  do arquivo `settings.py`, para sua necessidade.
 - **settings_test.py**: Arquivo que define configurações específicas para rodar os testes.
 - **404.html**: Template que implementa a página quando retornar um código de status 404.
 - **500.html**: Template que implementa a página quando retornar um código de status 500.
 - **base.html**: Template que define o "esqueleto" de toda página implementada no sistema.
 - **flatpages**: Pasta que contém templates que são usados para conteúdos estáticos, usando o `contrib.flatpages <https://docs.djangoproject.com/en/1.8/ref/contrib/flatpages/>`_ do Django.
 - **registration**: Pasta que contém templates que sobrescrevem páginas usadas pelo `contrib.auth <https://docs.djangoproject.com/en/1.8/ref/contrib/auth>`_ do Django.
 - **pagination.html**: Template que contem a estrutura básica de uma paginação de dados.
 - **urls.py**: Contêm o mapeamento de todas as rotas do projeto.
 - **wsgi.py**: Configura o projeto para ser servido usando qualquer servidor com suporte ao WSGI.
