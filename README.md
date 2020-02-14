<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![CircleCI](https://circleci.com/gh/jeffshek/open.svg?style=svg)](https://circleci.com/gh/jeffshek/open) [![Python 3
.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![codebeat badge](https://codebeat.co/badges/11be282f-cbaa-4c8f-bfb9-539e1c7e2366)](https://codebeat.co/projects/github-com-jeffshek-open-master)
![CookieCutter](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)
[![Coverage Status](https://coveralls.io/repos/github/jeffshek/open/badge.svg?branch=master)](https://coveralls.io/github/jeffshek/open?branch=master)

Hi. This my personal repo I'm using to contain all my open source ideas. It serves as my justification to try out new
ideas, but with an overengineered infrastructure and libraries to support scaling and doing things "my way".

If you're familiar with Django, this will be very similar. Unfortunately due to time constraints, I can't offer free
 support.

In the future, I'm expecting to move a lot of machine learning projects about health into this repo.

In the upcoming month, as I move things over bit by bit, this will be home to

* [BetterSelf](https://www.betterself.io)
* A drug discovery generator
* A clinical trial analytics engine
* More applied machine learning projects in health and medicine

## writeup.ai
### Lots of Credit To ....
* [OpenAI](https://openai.com/blog/better-language-models/) for generating and releasing GPT-2 Medium
* [HuggingFace](https://github.com/huggingface/pytorch-transformers) for making PyTorch extensions
* [Google Cloud Platform](https://cloud.google.com/) it's been a pleasure using GCP to host this
* This is mostly open-sourced, but there is a separate private repo that handles all the deployments and the ML services. That was too hard to open-source without making my life too hard. But it's probably the easiest one to code - it only consists of a microservice and a web app hosting models.
* I'll be releasing a huge writeup about how this was built on my [blog](https://senrigan.io/blog/).

## Development

### To start a local web server
~~~bash
1) mkdir -p .envs/local && touch .django
2) Add some random env_varibles in there
3) Run docker-compose -f local.ym up
4) Profit
~~~

### To install pre-commit hooks
~~~bash
# probably be on a virtualenv where calling python results in py3+

1. pip install pre-commit
2. pre-commit install
~~~
