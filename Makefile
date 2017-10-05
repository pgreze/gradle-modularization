.DEFAULT_GOAL := benchmark
clean:
	rm -rf build
	rm -rf generator/__pycache__
generate: clean
	python3 ./gen-projects.py
	python3 ./gen-scenarios.py
benchmark: generate gradle-profiler
	./benchmark.sh sample sample
gradle-profiler:
	git submodule update --init --recursive
	cd gradle-profiler && ./gradlew installDist
.PHONY: clean, generate, benchmark, gradle-profiler
