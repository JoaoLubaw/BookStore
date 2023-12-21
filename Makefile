# Set this to ~use it everywhere in the project setup
PYTHON_VERSION ?= 3.8.10
# the directories containing the library modules this repo builds
LIBRARY_DIRS = mylibrary
# build artifacts organized in this Makefile
BUILD_DIR ?= build

# PyTest options
PYTEST_HTML_OPTIONS = --html=$(BUILD_DIR)/report.html --self-contained-html
PYTEST_TAP_OPTIONS = --tap-combined --tap-outdir $(BUILD_DIR)
PYTEST_COVERAGE_OPTIONS = --cov=$(LIBRARY_DIRS)
PYTEST_OPTIONS ?= $(PYTEST_HTML_OPTIONS) $(PYTEST_TAP_OPTIONS) $(PYTEST_COVERAGE_OPTIONS)

# MyPy typechecking options
MYPY_OPTS ?= --python-version $(basename $(PYTHON_VERSION)) --show-column-numbers --pretty --html-report $(BUILD_DIR)/mypy
# Python installation artifacts
PYTHON_VERSION_FILE=.python-version
PIP ?= pip3

COLOR_ORANGE = \033[33m
COLOR_RESET = \033[0m



##@ Utility

.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: version-python
version-python: ## Echos the version of Python in use
	@echo $(PYTHON_VERSION)

##@ Testing

.PHONY: test
test: ## Runs tests
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		pytest
	pytest $(PYTEST_OPTIONS) tests/*.py

##@ Building and Publishing

.PHONY: build
build: ## Runs a build
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		setuptools wheel
	python setup.py sdist bdist_wheel

.PHONY: publish
publish: ## Publish a build to the configured repo
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		twine
	twine upload dist/*

.PHONY: deps-py-update
deps-py-update: pyproject.toml ## Update Python dependencies, e.g., after adding a new one manually
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		poetry
	poetry update

##@ Setup
# dynamic-ish detection of Python installation directory with pyenv
$(PYENV_VERSION_DIR):
	pyenv install --skip-existing $(PYTHON_VERSION)
$(PYTHON_VERSION_FILE): $(PYENV_VERSION_DIR)
	pyenv local $(PYTHON_VERSION)

.PHONY: deps
deps: deps-brew deps-py  ## Installs all dependencies

.PHONY: deps-brew
deps-brew: Brewfile ## Installs development dependencies from Homebrew
	brew bundle --file=Brewfile
	@echo "$(COLOR_ORANGE)Ensure that pyenv is set up in your shell.$(COLOR_RESET)"
	@echo "$(COLOR_ORANGE)It should have something like 'eval \$$(pyenv init -)'$(COLOR_RESET)"

.PHONY: deps-py
deps-py: $(PYTHON_VERSION_FILE) ## Installs Python development and runtime dependencies
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		poetry
	poetry install

##@ Code Quality

.PHONY: check
check: check-py ## Runs linters and other important tools

.PHONY: check-py
check-py: check-py-flake8 check-py-black check-py-mypy ## Checks only Python files

.PHONY: check-py-flake8
check-py-flake8: ## Runs flake8 linter
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		flake8
	flake8 .

.PHONY: check-py-black
check-py-black: ## Runs black in check mode (no changes)
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		black
	black --check --line-length 118 --fast .

.PHONY: check-py-mypy
check-py-mypy: ## Runs mypy
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		mypy
	mypy $(MYPY_OPTS) $(LIBRARY_DIRS)

.PHONY: format-py
format-py: ## Runs black, makes changes where necessary
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		black
	black .

.PHONY: format-autopep8
format-autopep8:
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		autopep8
	autopep8 --in-place --recursive .

.PHONY: format-isort
format-isort:
	$(PIP) install --upgrade \
		--index-url $(PYPI_PROXY) \
		isort
	isort --recursive .
