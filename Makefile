.DEFAULT_GOAL := benchmark
clean:
	rm -rf build
	rm -rf generator/__pycache__
generate: clean
	python3 -m generator
	./gen-scenarios.py
benchmark: generate
	./benchmark.sh sample sample
	./benchmark.sh single_app single_app
	./benchmark.sh app_2libs app_lib
	./benchmark.sh app_10libs app_lib
gradle-profiler:
	git submodule update --init --recursive
	cd gradle-profiler && ./gradlew installDist
.PHONY: clean, generate, benchmark, gradle-profiler
