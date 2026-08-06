.PHONY: all deps run test clean format lint doc

all: deps

deps:
	pip install -r requirements.txt 2>/dev/null || true

run:
	python3 -m src.main

test:
	python3 -m unittest discover -s tests -v

format:
	@clang-format -i proto/*.proto 2>/dev/null || true

lint:
	@python3 -m py_compile src/*.py src/**/*.py 2>/dev/null || true
	@pylint --disable=C src/ 2>/dev/null || true

doc:
	@doxygen docs/Doxyfile 2>/dev/null || echo "doxygen not available"

clean:
	rm -rf __pycache__ .venv dist
