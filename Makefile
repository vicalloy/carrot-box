run:
	cd carrot_box;python manage.py runserver 0.0.0.0:9000

pyenv:
	pip install pipenv --upgrade
	pipenv --python 3
	pipenv install -d --skip-lock
	pipenv shell

init:
	cd carrot_box;python manage.py migrate
	cd carrot_box;python manage.py bower install

isort:
	isort --recursive lbworkflow
