SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	mypy typecasts tests/**/*.py
	flakehell lint typecasts tests

.PHONY: unit
unit:
	pytest

.PHONY: package
package:
	poetry check
	pip check
	# Ignoring sphinx@2 security issue for now, see:
  # https://github.com/miyakogi/m2r/issues/51
	safety check --full-report -i 38330

.PHONY: test
test: lint package unit
