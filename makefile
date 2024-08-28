
PROJECT_NAME = team-hyper-accelerated-dragon
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python-related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)



# SET-UP

## Install bandit - scans the project code and reports on any issues
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety - checks for security issues in Python libraries
#safety:
#	$(call execute_in_env, $(PIP) install safety)

## Install black/flake8 - linter to check files for style issues + fix many problems in place

# Flake8 had been temporarily commented out as this was being flagged for security vulnerabilities, black as possible alternative?
flake8:
	$(call execute_in_env, $(PIP) install flake8)

## Install coverage - checks how much of code is tested by our unit and integration tests (aiming for 90+%)
coverage:
	$(call execute_in_env, $(PIP) install pytest-cov)

## Set up dev requirements (bandit, safety, flake8)
dev-setup: bandit coverage flake8 #safety



# BUILD/RUN

## Run the security test (bandit + safety)
security-test:
#	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the flake8 code check
run-flake8:
	$(call execute_in_env, flake8  ./src/*/*.py ./test/*/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} AWS_DEFAULT_REGION=eu-west-2 pytest -v)

## Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov)

## Run all checks
run-checks: security-test check-coverage unit-test 

## Run linter
run-linter: run-flake8

