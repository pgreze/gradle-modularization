.DEFAULT_GOAL := benchmark
clean:
	rm -rf build
	rm -rf generator/__pycache__
generate: clean
	python3 -m generator
benchmark: generate
	./benchmark.sh
gradle-profiler:
	git submodule update --init --recursive
	cd gradle-profiler && ./gradlew installDist
.PHONY: clean, generate, benchmark, gradle-profiler
