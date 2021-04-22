docker_serve:
	docker-compose up --build
container:
	docker-compose run --rm app python3 manage.py migrate
install:
	pip3 install -r requirements.txt
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
superuser:
	python manage.py createsuperuser
collectstatic:
	python manage.py collectstatic
set_env_vars:
	@[ -f .env ] && source .env
serve:
	python3 manage.py runserver
test:
	pytest --cov-report term-missing --cov=apps -p no:warnings

.PHONY: set_env_vars
