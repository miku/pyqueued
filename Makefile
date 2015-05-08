clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf build/ dist/ pyqueued.egg-info/ __pycache__

coverage:
	nosetests --with-coverage --cover-package=pyqueued

dist:
	python setup.py sdist
