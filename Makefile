all:
	@echo Nothing to do.

release:
	python setup.py sdist upload

clean:
	- rm -rf build/ dist/ pysolr4.egg-info/
