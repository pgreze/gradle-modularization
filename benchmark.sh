#!/usr/bin/env bash -x

gprofiler="gradle-profiler/build/install/gradle-profiler/bin/gradle-profiler"
function benchmark {
    $gprofiler --gradle-version 4.1 --benchmark --warmups 1 --iterations 10 \
        --output-dir "$1/benchmark/" --project-dir $*
}
function benchmark_scenario {
    $gprofiler --benchmark --output-dir "$1/benchmark/" --project-dir $*
}

# No apply-abi-change for Kotlin now

PROJECT_NAME=$1
SCENARIO_NAME=$2

benchmark_scenario build/$PROJECT_NAME --scenario-file build/$SCENARIO_NAME.scenario
