.PHONY: setup validate-deps format lint test verify check help docker-build docker-run test-wizard test-immutability

ifeq ($(OS),Windows_NT)
    VENV_BIN := $(CURDIR)/.venv/Scripts/python
    PYTHON_SYS := python
else
    VENV_BIN := $(CURDIR)/.venv/bin/python
    PYTHON_SYS := python3
endif

# Prioritiza o interpretador do virtualenv se ele existir
PYTHON := $(shell if [ -f $(VENV_BIN) ]; then echo $(VENV_BIN); else echo $(PYTHON_SYS); fi)

DOCKER_IMAGE := sdd-architecture-check
ENFORCEMENT ?= strict
TRIVY_SEVERITY ?= HIGH,CRITICAL

CORE_DIR := _core

help:
	@echo "🏗️ SDD Architecture - Quality Tools"
	@echo "=================================="
	@echo "setup   : Install dependencies from pyproject.toml"
	@echo "format  : Auto-format code with Black and Ruff"
	@echo "lint    : Run static analysis (Ruff, MyPy, Pylint)"
	@echo "test    : Run all test layers"
	@echo "verify  : Check governance compliance"
	@echo "check   : Run all checks (format + lint + verify + test)"
	@echo "docker-build : Build optimized Docker image"
	@echo "docker-scan  : Scan image for vulnerabilities"
	@echo "docker-run   : Run checks inside Docker container"

setup:
	./setup.sh

validate-deps:
	@echo "🔍 Validating environment and dependencies..."
	@$(PYTHON) -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" || (echo "❌ Python 3.10 or higher is required." && exit 1)
	@$(PYTHON) -m pip show sdd-architecture-core > /dev/null 2>&1 || (echo "❌ Dependencies not installed. Run 'make setup' first." && exit 1)

format: validate-deps
	$(PYTHON) -m ruff check $(CORE_DIR) --fix
	$(PYTHON) -m black $(CORE_DIR)

lint: validate-deps
	$(PYTHON) -m ruff check $(CORE_DIR)
	$(PYTHON) -m mypy --config-file $(CORE_DIR)/pyproject.toml --explicit-package-bases $(CORE_DIR)
	PYTHONPATH="$(CURDIR)/$(CORE_DIR):$(CURDIR)/$(CORE_DIR)/build_scripts:$(CURDIR)/$(CORE_DIR)/core:$(CURDIR)/$(CORE_DIR)/compiler:$(CURDIR)/$(CORE_DIR)/compiler/src:$(CURDIR)/$(CORE_DIR)/compiler/src/runtime_telemetry_kit:$(CURDIR)/$(CORE_DIR)/wizard:$(CURDIR)/$(CORE_DIR)/wizard/src:$(CURDIR)/$(CORE_DIR)/wizard/.sdd-runtime:$(CURDIR)/$(CORE_DIR)/migration/tooling:$(CURDIR)/$(CORE_DIR)/cli/extensions/framework" \
		$(PYTHON) -m pylint --rcfile $(CORE_DIR)/pyproject.toml $(CORE_DIR) --fail-under=9.0

test: validate-deps
	cd $(CORE_DIR) && $(PYTHON) tools/run-all-tests.py --fail-fast

test-wizard: validate-deps
	$(PYTHON) $(CORE_DIR)/tools/run-all-tests.py --layer "Wizard" --fail-fast

test-immutability: validate-deps
	$(PYTHON) _core/tests/test_governance_immutability.py $(ENFORCEMENT)

verify: validate-deps
	$(PYTHON) $(CORE_DIR)/tools/governance_compliance.py --verify --check-integrity .

check: validate-deps format lint verify test test-wizard test-immutability
	@echo "✅ All quality and governance checks passed!"

docker-scan:
	docker build --target security-scan -t $(DOCKER_IMAGE)-security .

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-run:
	docker run --rm -v $(shell pwd):/app -e ENFORCEMENT=$(ENFORCEMENT) $(DOCKER_IMAGE)