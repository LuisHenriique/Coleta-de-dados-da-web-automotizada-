all: run

run:
	python3 usp.py subject.py course.py unit.py


clean:
	rm -f *.pyc __pycache__/*
