run:
	python manage.py runserver 0.0.0.0:9000

test:
	;python manage.py test carrot_box

init:
	pip install pipenv --upgrade
	pipenv --python 3
	pipenv install -d --skip-lock
	pipenv shell
	python manage.py migrate
	python manage.py bower install
	python manage.py callfunc lbworkflow.wfdata.load_data

load_data:
	python manage.py callfunc lbworkflow.wfdata.load_data

isort:
	isort --recursive carrot_box
