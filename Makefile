deps:
	@bash -c "./setup_os.sh"

setup: deps
	@python manage.py migrate --settings associados.settings
	@python manage.py loaddata --settings associados.settings app/core/fixtures/site_init.json

run:
	@python manage.py runserver 0.0.0.0:8000 --settings associados.settings

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python manage.py test --settings associados.settings_test --verbosity=2

shell:
	@python manage.py shell --settings=associados.settings

help:
	@grep '^[^#[:space:]].*:' Makefile | awk -F ":" '{print $$1}'

makemessages:
	@python manage.py makemessages -l pt_BR

compilemessages:
	@python manage.py compilemessages
