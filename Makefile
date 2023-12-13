all:
	poetry install --no-root
	poetry shell

run:
	python chatapi/server.py