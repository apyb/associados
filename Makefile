deps:
	@bash -c "./setup_os.sh"

setup: deps
	@python manage.py syncdb --settings associados.settings_local

run:
	@python manage.py runserver 0.0.0.0:8000 --settings associados.settings_local

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python manage.py test --settings associados.settings_test --verbosity=2


help:
	@grep '^[^#[:space:]].*:' Makefile | awk -F ":" '{print $$1}'

makemessages:
	@python manage.py makemessages --settings associados.settings_test -l pt_BR

compilemessages:
	@python manage.py compilemessages --settings associados.settings_test 
