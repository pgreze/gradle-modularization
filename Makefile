generate: clean
	python3 -m generator
gradle-profiler:
	git submodule update --init --recursive
	cd gradle-profiler && ./gradlew installDist
clean:
	rm -rf build
	rm -rf generator/__pycache__
.PHONY: clean, generate
