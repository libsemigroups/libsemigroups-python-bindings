pip-install:
	pip3 install --user . --upgrade
	pip install --user . --upgrade

clean:
	rm -f tests/*.pyc *.pyc

tests:
	python3 -m unittest discover
	python -m unittest discover
	
coverage: pip-install
	coverage run -m unittest discover
	coverage html
	@echo "See: htmlcov/index.html" 

lint:
	@command -v pylint >/dev/null 2>&1 || { echo >&2 "pylint is required but is not installed.  Aborting."; exit 1; }
	pylint -rn semigroups/*.py
	pylint -rn tests/test_*.py
	@command -v flake8 >/dev/null 2>&1 || { echo >&2 "flake8 is required but is not installed.  Aborting."; exit 1; }
	flake8 semigroups/*.py 
	flake8  tests/test_*.py

doc: 
	cd docs ; make html; cd ..
	@echo "See: docs/_build/html/index.html" 

doc-clean: 
	cd docs ; make clean; cd ..

.PHONY: coverage tests lint
