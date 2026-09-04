.PHONY: install run test clean

install:
	python -m pip install -r requirements.txt

run:
	python run_pipeline.py

test:
	python -m unittest discover -s tests -v

clean:
	python scripts/clean_outputs.py

