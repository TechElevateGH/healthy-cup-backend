
run:
		flask run

clean:
	find . | grep -E "(/__pycache__)" | xargs rm -rf