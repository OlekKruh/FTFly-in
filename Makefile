.PHONY: install run debug clean lint lint-strict

install:
	uv venv
	uv pip install -r requirements.txt

run:
	uv run python3 -m src.main

debug:
	uv run python3 -m pdb src.main

lint:
	uv run flake8 src/
	uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src/
	uv run mypy src/ --strict --ignore-missing-imports

clean:
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__
	rm -rf .mypy_cache