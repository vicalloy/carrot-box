run:
	python manage.py runserver 0.0.0.0:9000

test:
	coverage run manage.py test carrot_box
	coverage html

init:
	pip install pipenv --upgrade
	pipenv --python 3
	pipenv install -d --skip-lock
	pipenv shell
	python manage.py migrate
	python manage.py bower install --allow-root
	python manage.py callfunc lbworkflow.wfdata.load_data
	python manage.py callfunc carrot_box.wfdata.load_data
	python manage.py callfunc carrot_box.wfapp.leave.wfdata.load_data
	python wfgen.py

load_data:
	python manage.py callfunc lbworkflow.wfdata.load_data

load_sample_data:
	python manage.py callfunc lbworkflow.wfdata.load_data
	python manage.py callfunc carrot_box.wfdata.load_data
	python manage.py callfunc carrot_box.wfapp.leave.wfdata.load_data

isort:
	isort --recursive carrot_box

wfgen:
	python wfgen.py

wfgen_clean:
	python wfgen.py clean


build_docker_image:
	docker build -t carrot-box:0.9 .

create_docker_container:
	docker run -d -p 9000:9000 --name carrot-box carrot-box:0.9
