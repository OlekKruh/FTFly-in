.PHONY: install run debug clean lint lint-strict

install:
	uv pip install -r requirements.txt

run:
	python3 src/main.py

debug:
	python3 -m pdb src/main.py

lint:
	flake8 src/
	mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 src/
	mypy src/ --strict --ignore-missing-imports

clean:
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__
	rm -rf .mypy_cache