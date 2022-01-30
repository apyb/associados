deps:
	@bash -c "./setup_os.sh"

setup: deps
	@python manage.py migrate
	@python manage.py loaddata app/core/fixtures/site_init.json

run:
	@python manage.py runserver 0.0.0.0:8000

clean:
	@find . -name "*.pyc" -delete

test: clean
	@python manage.py test --verbosity=2

shell:
	@python manage.py shell

help:
	@grep '^[^#[:space:]].*:' Makefile | awk -F ":" '{print $$1}'

makemessages:
	@python manage.py makemessages -l pt_BR

compilemessages:
	@python manage.py compilemessages

run-with-docker:
	docker-compose run --service-ports --rm web
