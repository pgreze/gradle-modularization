#!/usr/bin/env python3

import sys
from pathlib import Path
import generator

multi_dex_properties = [
    "org.gradle.jvmargs=-Xmx4G",
    "org.gradle.parallel=true",
]

multi_10_dependencies = (
    (3, 4), # 1
    (5, 6),
    (7,), # 3
    (7,),
    (8,), # 5
    (8,),
    (9,), # 7
    (9,),
    (), # 9
)
def multi_100_dependencies(n):
    '''Resolve dependencies for the Nth lib in multi_100 project.

    Example: n=11 is in 1th group. It's depending on group 3 and 4
    In other words, 23-33 + 34-44 = 23-44 libraries.
    '''
    group = n // 10
    if (n % 10) > group: # For 12,13... or 89
        group += 1
    deps = []

    start = (group - 1) * 10 + group
    layers = (
        (start, start+1),
        (start+2, start+3, start+4, start+5),
        (start+6, start+7, start+8),
        (start+9, start+10),
    )
    for layer in layers:
        if n < layer[0]:
            deps += layer

    for dep_group in multi_10_dependencies[group - 1]:
        deps += [i for i in range(
            (dep_group - 1) * 10 + dep_group,
            dep_group * 10 + dep_group + 1
        )]

    return deps

def sample(path):
    projects = [
        generator.JavaProject('java', 2, 10),
        generator.KotlinProject('kotlin', 3, 15),
        generator.KotlinAndroidProject('kotlin_android', 4, 20, library=False),
        generator.AndroidProject('android_lib', 3, 15, library=True),
        generator.AndroidProject('app', 3, 15, library=False, dependencies=[
            'java', 'kotlin', 'kotlin_android', 'android_lib',
        ]),
    ]
    return (
        generator.GradleRootProject('sample', projects=[p.project_id for p in projects]),
        projects,
    )

def single_app(path):
    return (
        generator.GradleRootProject('single_app', projects=['app'], properties=multi_dex_properties),
        [generator.AndroidProject('app', 10000, 100000, library=False)],
    )

def multi_3(path):
    return (
        generator.GradleRootProject('multi_3',
            projects=['app', 'lib1', 'lib2'],
            properties=multi_dex_properties
        ), [
            generator.AndroidProject('lib1', 3333, 33333, library=True),
            generator.AndroidProject('lib2', 3333, 33333, library=True),
            generator.AndroidProject(
                'app', 3333, 33333, library=False,
                dependencies=['lib1', 'lib2']
            ),
        ],
    )

def multi_10(path):
    return (
        generator.GradleRootProject('multi_10',
            projects=['app'] + ['lib%s' % i for i in range(1, 10)],
            properties=multi_dex_properties
        ), [
            generator.AndroidProject('lib%s' % i, 1000, 10000, library=True,
                dependencies=['lib%s' % dep for dep in multi_10_dependencies[i-1]])
            for i in range(1, 10)
        ] + [
            generator.AndroidProject(
                'app', 1000, 10000, library=False,
                dependencies=['lib%s' % i for i in range(1, 10)]
            )
        ],
    )

def multi_100(path):
    return (
        generator.GradleRootProject('multi_100',
            projects=['app'] + ['lib%s' % i for i in range(1, 100)],
            properties=multi_dex_properties
        ), [
            generator.AndroidProject('lib%s' % i, 100, 1000, library=True,
                dependencies=['lib%s' % dep for dep in multi_100_dependencies(i)])
            for i in range(1, 100)
        ] + [
            generator.AndroidProject(
                'app', 100, 1000, library=False,
                dependencies=['lib%s' % i for i in range(1, 100)]
            )
        ],
    )

if __name__ == '__main__':
    path = Path('build/')
    scenarios = [
        sample(path),
        single_app(path),
        multi_3(path),
        multi_10(path),
        multi_100(path),
    ]

    if len(sys.argv) > 1:
        # Filter names provided in args
        scenarios = [s for s in scenarios if s[0].project_id in sys.argv[1:]]

    for root_project, sub_projects in scenarios:
        multi_project_path = root_project.generate(path)
        for project in sub_projects:
            project.generate(multi_project_path / 'projects/')
