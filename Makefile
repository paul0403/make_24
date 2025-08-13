clean:
	rm -rf */__pycache__
	rm -rf */*/__pycache__

pytest:
	pytest test/
	make clean