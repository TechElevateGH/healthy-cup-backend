.PHONY: clean run

all: run

run:
		docker-compose run

clean:
	find . | grep -E "(/__pycache__)" | xargs rm -rf
	find . -name "*.pyc" -exec rm -f {} \;

install:
	pip install -r requirements.txt

sort:
	isort .

deps:
    pip install -r requirements.txt

freeze:
    pip freeze > requirements.txt

build:
	docker-compose build




