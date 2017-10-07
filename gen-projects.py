#!/usr/bin/env python3

import sys
from pathlib import Path
import generator

multi_dex_properties = [
    "org.gradle.jvmargs=-Xmx4G",
    "org.gradle.parallel=true",
]

CLASSES = 1000 * 10
METHODS = CLASSES * 20

multi_10_dependencies = (
    (3, 5), # 1
    (4, 6),
    (7,), # 3
    (7,),
    (8,), # 5
    (8,),
    (9,), # 7
    (9,),
    (), # 9
)
def multi_dependencies(current_project, project_count):
    '''Resolve dependencies for the Nth lib in project number benchs.
    Example: multi_100 but also possible for others.

    Example: n=11 is in 1th group. It's depending on group 3 and 4
    In other words, 23-33 + 34-44 = 23-44 libraries.
    '''
    group = current_project // 10
    if (current_project % 10) > group: # For 12,13... or 89
        group += 1
    deps = []

    start = (group - 1) * 10 + group
    idx = current_project - start
    if idx < len(multi_10_dependencies):
        deps += [start + i for i in multi_10_dependencies[idx]]

    for dep_group in multi_10_dependencies[group - 1]:
        deps += [i for i in range(
            (dep_group - 1) * 10 + dep_group,
            dep_group * 10 + dep_group + 1
        )]

    return [i for i in deps if i < project_count]

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
        [generator.AndroidProject('app', CLASSES, METHODS, library=False)],
    )

def multi(path, project_count):
    libs = ['lib%s' % i for i in range(1, project_count)]
    return (
        generator.GradleRootProject('multi_%s' % project_count,
            projects=['app'] + libs,
            properties=multi_dex_properties
        ), [
            generator.AndroidProject('lib%s' % i,
                CLASSES/project_count, METHODS/project_count,
                dependencies=['lib%s' % dep for dep in multi_dependencies(i, project_count)],
                library=True)
            for i in range(1, project_count)
        ] + [
            generator.AndroidProject('app',
                CLASSES/project_count, METHODS/project_count,
                dependencies=libs,
                library=False),
        ],
    )

if __name__ == '__main__':
    path = Path('build/')
    scenarios = [
        sample(path),
        single_app(path),
        multi(path, 3),
        multi(path, 5),
        multi(path, 8),
        multi(path, 10),
        multi(path, 30),
        multi(path, 50),
        multi(path, 80),
        multi(path, 100),
    ]

    if len(sys.argv) > 1:
        # Filter names provided in args
        scenarios = [s for s in scenarios if s[0].project_id in sys.argv[1:]]

    for root_project, sub_projects in scenarios:
        multi_project_path = root_project.generate(path)
        for project in sub_projects:
            project.generate(multi_project_path / 'projects/')
