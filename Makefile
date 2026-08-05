.PHONY: all deps run test clean
all: deps
deps:
	pip install -r requirements.txt 2>/dev/null || true
run:
	python3 -m src.main
test:
	python3 -m unittest discover -s tests -v
clean:
	rm -rf __pycache__ .venv dist
