pip-install:
	pip3 install --user . --upgrade
	pip install --user . --upgrade

tests:
	python3 -m unittest discover
	python -m unittest discover
	
# http://blog.behnel.de/posts/coverage-analysis-for-cython-modules.html
coverage: 
	python setup.py build_ext --inplace
	coverage run tests/*.test.py
	coverage html
	@echo "See: htmlcov/index.html" 

.PHONY: coverage, tests
