
run:
		flask run

clean:
	find . | grep -E "(/__pycache__)" | xargs rm -rf

install:
	pip install -r requirements.txt

sort:
	isort .