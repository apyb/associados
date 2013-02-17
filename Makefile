deps:
	@bash -c "./setup_os.sh"

setup: deps
	@python manage.py syncdb --settings associados.settings_local
	@python manage.py migrate --settings associados.settings_local

run:
	@python manage.py runserver 0.0.0.0:8000 --settings associados.settings_local

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python manage.py test --settings associados.settings_test --verbosity=2

shell:
	@python manage.py shell --settings=associados.settings_local

help:
	@grep '^[^#[:space:]].*:' Makefile | awk -F ":" '{print $$1}'

makemessages:
	@python manage.py makemessages -l pt_BR

compilemessages:
	@python manage.py compilemessages
