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

benchmark_scenario build/sample --scenario-file scenarios/sample
benchmark_scenario build/single_app --scenario-file scenarios/single_app
benchmark_scenario build/app_2libs --scenario-file scenarios/app_lib
benchmark_scenario build/app_10libs --scenario-file scenarios/app_lib
