multi:
	rm -rf build/multi
	python3 -m generator
clean:
	rm -rf build
	rm -rf generator/__pycache__
.PHONY: clean, multi
