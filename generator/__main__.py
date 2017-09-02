from pathlib import Path
import generator

multi_dex_properties = [
    "org.gradle.jvmargs=-Xmx4G",
    "org.gradle.parallel=true",
]

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
        [generator.AndroidProject('app', 10000, 1000000, library=False)],
    )

def app_2libs(path):
    return (
        generator.GradleRootProject('app_2libs',
            projects=['app', 'lib1', 'lib2'],
            properties=multi_dex_properties
        ), [
            generator.AndroidProject('lib1', 333, 33333, library=True),
            generator.AndroidProject('lib2', 333, 33333, library=True),
            generator.AndroidProject(
                'app', 333, 33333, library=False,
                dependencies=['lib1', 'lib2']
            ),
        ],
    )

def app_10libs(path):
    return (
        generator.GradleRootProject('app_10libs',
            projects=['app'] + ['lib%s' % i for i in range(1, 10)],
            properties=multi_dex_properties
        ), [
            generator.AndroidProject('lib%s' % i, 1000, 10000, library=True)
            for i in range(1, 10)
        ] + [
            generator.AndroidProject(
                'app', 1000, 10000, library=False,
                dependencies=['lib%s' % i for i in range(1, 10)]
            )
        ],
    )

if __name__ == '__main__':
    path = Path('build/')
    scenarios = [
        sample(path),
        single_app(path),
        app_2libs(path),
        app_10libs(path),
    ]

    for root_project, sub_projects in scenarios:
        multi_project_path = root_project.generate(path)
        for project in sub_projects:
            project.generate(multi_project_path / 'projects/')

    # Configure Composite build
    #with open(path / 'settings.gradle', mode='w') as f:
    #    f.write("\n".join("includeBuild '%s'" % p.project_id for p, _ in scenarios))
