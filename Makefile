
deps:
	@pip install -r requirements.txt
	@pip install -r requirements_test.txt

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
