<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![CircleCI](https://circleci.com/gh/jeffshek/open.svg?style=svg)](https://circleci.com/gh/jeffshek/open) [![Python 3
.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) 
[![codebeat badge](https://codebeat.co/badges/11be282f-cbaa-4c8f-bfb9-539e1c7e2366)](https://codebeat.co/projects/github-com-jeffshek-open-master) [![Coverage Status](https://coveralls.io/repos/github/jeffshek/open/badge.svg?branch=master)](https://coveralls.io/github/jeffshek/open?branch=master)
![CookieCutter](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)

Hi. This is a fun repo that I use to contain all my open source ideas. It serves as my justification to try out new 
ideas, but with an overengineered infrastructure just to do things "my way".

If you're familiar with Django, this will probably be very similar to repos you've previously seen. 

Unfortunately due to time constraints, I can't offer support.  

In the future, I'm expecting to move a lot of machine learning projects about health into this repo.

### To start a local web server
~~~bash
1) mkdir -p .envs/local && touch .django
2) Add some random env_varibles in there
3) Run docker-compose -f local.ym up
4) Profit
~~~ 

### To install pre-commit
> pre-commit install

