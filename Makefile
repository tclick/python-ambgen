.PHONY: clean conda conda-dev conda-test virtualenv virtualenv-dev test docker dist dist-upload

SHELL = /bin/bash
BASENAME = python-ambgen
CONDA_DIR = ${HOME}/.conda/envs/${BASENAME}
clean:
	find . -name '*.py[co]' -delete

conda:
	@conda create -y -c conda-forge -p ${CONDA_DIR} --file environments/prod.yml
	@source activate ${BASENAME} && pip install .

conda-test: conda
	@conda install -y -c conda-forge -n ${BASENAME} --file environments/test.yml
	@source activate ${BASENAME} && pip install .

conda-dev: conda-test
	@conda install -y -c conda-forge -n ${BASENAME} --file environments/dev.yml
	@source activate ${BASENAME} && pip install -e .[dev]

virtualenv:
	@virtualenv --prompt '|> python-fluctmatch <| ' env
	@env/bin/pip install -r requirements.txt
	@env/bin/pip install -e .
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

virtualenv-dev: virtualenv
	@virtualenv --prompt '|> python-fluctmatch <| ' env
	@env/bin/pip install -r requirements.txt
	@env/bin/pip install -r requirements/test.txt
	@env/bin/pip install -e .[dev]
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=${BASENAME} \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t ${BASENAME}:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
