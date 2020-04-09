# Carrot Box

[![](https://secure.travis-ci.org/vicalloy/carrot-box.svg?branch=master)](http://travis-ci.org/vicalloy/carrot-box)
[![](https://coveralls.io/repos/github/vicalloy/carrot-box/badge.svg?branch=master)](https://coveralls.io/github/vicalloy/carrot-box?branch=master)

Carrot box is a workflow platform, it also an example of using [django-lb-workflow](https://github.com/vicalloy/django-lb-workflow/).

<img src="screenshots/main.png" alt="Main">

<img src="screenshots/detail.png" alt="Detail">

<img src="screenshots/flowchart.png" alt="Flowchart">

Demo site
---------

Demo site: http://wf.haoluobo.com/

username: ``admin`` password: ``password``

Switch to another user: http://wf.haoluobo.com/impersonate/search

Stop switch: http://wf.haoluobo.com/impersonate/stop

Running locally
---------------

Run the following commands:

    make init-pyenv
    make init
    make run

Creating Custom Workflows
-------------------------

You should read the documentation of [django-lb-workflow](https://github.com/vicalloy/django-lb-workflow/).
