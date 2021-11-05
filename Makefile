SHELL := /bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

run:
	source ~/.virtualenvs/mandelbrot-set/bin/activate && \
	python3 ./main.py

requirements:
	pip3 install -r requirements.txt
