Configuração
============

Para configurar o projeto você precisa seguir os seguintes procedimentos.

Instalando localmente
---------------------

Para fazer uma instalação local na sua máquina, precisa seguir alguns requisitos básicos:

 - Python 2.7;
 - Pip;
 - Virtualenv;
 - PostgreSQL;


 Esses itens são obrigatórios para iniciarmos a configuração do projeto. Então vamos lá.


1. Baixe o projeto:

.. code-block:: bash

    $ git clone https://github.com/pythonbrasil/associados.git

2. Crie o ambiente virtual:

.. code-block:: bash

    $ cd associados
    $ virtualenv venv
    Using base prefix '/usr'
    New python executable in venv/bin/python
    Installing setuptools, pip, wheel...done.

3. Ative o ambiente virtual:

.. code-block:: bash

    $ source venv/bin/activate

4. Instale as dependências do projeto:

.. code-block:: bash

    $ make setup

Ele vai instalar as depedências do arquivo `requirements.txt` para que possa rodar localmente, além de rodar as migrações do projeto para definir o esquema do banco. Agora
é só rodar.

.. code-block:: bash

    $ make run


