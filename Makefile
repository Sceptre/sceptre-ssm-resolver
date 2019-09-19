coverage-all:
		coverage erase
		coverage run --source resolver -m unittest
		coverage xml

coverage: coverage-all
		coverage report --show-missing

test:
	    pytest --junitxml=test-reports/junit.xml

lint:
	    flake8 .

acceptance-test:
	    behave acceptance-tests/

sonar:
	    @sonar-scanner \
            -Dsonar.projectKey=Sceptre_${CIRCLE_PROJECT_REPONAME} \
            -Dsonar.organization=sceptre \
			-Dsonar.projectName=${CIRCLE_PROJECT_REPONAME} \
            -Dsonar.pullrequest.provider=GitHub\
			-Dsonar.branch.name=${CIRCLE_BRANCH}\
            -Dsonar.sources=. \
            -Dsonar.host.url=https://sonarcloud.io \
            -Dsonar.login=${SONAR_LOGIN}


dist: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	twine check dist/*
	ls -l dist

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .cache/
	rm -f .coverage.xml
	rm -f test-results/
